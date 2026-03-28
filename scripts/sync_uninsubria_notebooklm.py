#!/usr/bin/env python3
import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DOWNLOAD_DIR = DATA_DIR / "downloads"
STATE_PATH = DATA_DIR / "uninsubria_sync_state.json"
MAP_PATH = DATA_DIR / "course_notebook_map.json"

BASE_URL = os.getenv("UNINSUBRIA_BASE_URL", "https://elearning.uninsubria.it")
MY_URL = f"{BASE_URL}/my/"
COOKIE = os.getenv(
    "COOKIE_HEADER",
    "_shibsession_656c6561726e696e672e756e696e7375627269612e697468747470733a2f2f73702d656c6561726e696e672d756e696e7375627269612d70726f642e63696e6563612e69742f73686962626f6c657468=_c60e10d3e594c4bae5c9efedbe81d37d; MoodleSessioninsubriaprod=r4thbvfikpakfcpq2rl893ajd8",
)


def log(msg: str) -> None:
    print(msg, flush=True)


def read_state() -> dict:
    if not STATE_PATH.exists():
        return {"version": 1, "courses": {}, "files": {}, "ignored": {}}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"version": 1, "courses": {}, "files": {}, "ignored": {}}


def write_state(state: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def http_request_bytes(url: str, method: str = "GET", body: str | None = None) -> bytes:
    headers = {
        "Cookie": COOKIE,
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/html, */*",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": BASE_URL,
        "Referer": MY_URL,
    }
    if method == "POST":
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        url=url,
        data=(body.encode("utf-8") if body is not None else None),
        headers=headers,
        method=method,
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def http_request(url: str, method: str = "GET", body: str | None = None) -> str:
    return http_request_bytes(url=url, method=method, body=body).decode("utf-8", errors="replace")


def extract_sesskey() -> str:
    page = http_request(MY_URL, method="GET")
    m = re.search(r'"sesskey":"([^"]+)"', page)
    if not m:
        m = re.search(r"sesskey=([A-Za-z0-9]+)", page)
    if not m:
        raise RuntimeError("Sesskey non trovato. Cookie/sessione probabilmente scaduti.")
    return m.group(1)


def api_url(info: str, sesskey: str) -> str:
    return f"{BASE_URL}/lib/ajax/service.php?sesskey={sesskey}&info={info}"


def fetch_courses(sesskey: str) -> list[dict]:
    url = api_url("core_course_get_enrolled_courses_by_timeline_classification", sesskey)
    payload = json.dumps(
        [
            {
                "index": 0,
                "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
                "args": {"offset": 0, "limit": 0, "classification": "all", "sort": "fullname"},
            }
        ]
    )
    raw = http_request(url, method="POST", body=payload)
    data = json.loads(raw)
    if not isinstance(data, list) or not data:
        raise RuntimeError("Risposta corsi non valida.")
    if data[0].get("error"):
        raise RuntimeError(f"Errore API corsi: {data[0]}")
    return data[0]["data"]["courses"]


def fetch_course_state(sesskey: str, course_id: int) -> dict:
    url = api_url("core_courseformat_get_state", sesskey)
    payload = json.dumps(
        [{"index": 0, "methodname": "core_courseformat_get_state", "args": {"courseid": int(course_id)}}]
    )
    raw = http_request(url, method="POST", body=payload)
    data = json.loads(raw)
    if data[0].get("error"):
        raise RuntimeError(f"Errore API course state per corso {course_id}")
    inner = data[0]["data"]
    if isinstance(inner, str):
        inner = json.loads(inner)
    return inner


def extract_folder_links(folder_html: str) -> list[tuple[str, str]]:
    links = re.findall(
        r'<span class="fp-filename">\s*<a href="([^"]+)"[^>]*>(.*?)</a>',
        folder_html,
        flags=re.S,
    )
    out = []
    for href, name in links:
        out.append((html.unescape(href.strip()), html.unescape(name.strip())))
    return out


def normalize_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def safe_filename(name: str) -> str:
    name = name.replace("/", "_").replace("\\", "_").strip()
    return name[:220] if name else "file.bin"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_notebooklm(args: list[str]) -> dict:
    cmd = ["notebooklm"] + args + ["--json"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    if proc.returncode != 0:
        raise RuntimeError(f"Comando fallito: {' '.join(cmd)}\n{text[:800]}")
    # output may include warnings before JSON
    start = text.find("{")
    if start < 0:
        raise RuntimeError(f"Output JSON non trovato: {' '.join(cmd)}")
    return json.loads(text[start:])


def list_notebooks() -> list[dict]:
    return run_notebooklm(["list"]).get("notebooks", [])


def ensure_notebook_for_course(course: dict, state: dict, notebook_cache: list[dict]) -> tuple[str, str]:
    course_id = str(course["id"])
    fullname = course["fullname"].strip()
    title = f"UNINSUBRIA COURSE {course_id} - {fullname}"

    existing = state["courses"].get(course_id, {})
    if existing.get("notebook_id"):
        return existing["notebook_id"], existing.get("notebook_title", title)

    for nb in notebook_cache:
        nb_title = (nb.get("title") or "").strip()
        if f"UNINSUBRIA COURSE {course_id} -" in nb_title:
            return nb["id"], nb_title

    created = run_notebooklm(["create", title])
    nb = created["notebook"]
    notebook_cache.append({"id": nb["id"], "title": nb["title"]})
    return nb["id"], nb["title"]


def wait_source(notebook_id: str, source_id: str) -> bool:
    proc = subprocess.run(
        ["notebooklm", "source", "wait", source_id, "-n", notebook_id, "--timeout", "180", "--json"],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync corsi Uninsubria -> NotebookLM")
    parser.add_argument("--max-courses", type=int, default=0, help="Limita numero corsi (0 = tutti)")
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    state = read_state()
    notebook_cache = list_notebooks()

    log("Recupero sesskey...")
    sesskey = extract_sesskey()
    log(f"Sesskey OK: {sesskey}")

    log("Recupero corsi...")
    courses = fetch_courses(sesskey)
    if args.max_courses > 0:
        courses = courses[: args.max_courses]
    log(f"Corsi trovati: {len(courses)}")

    course_map = []
    uploaded_count = 0
    skipped_count = 0

    for idx, course in enumerate(courses, start=1):
        course_id = str(course["id"])
        log(f"[{idx}/{len(courses)}] Corso {course_id} - {course['fullname']}")

        nb_id, nb_title = ensure_notebook_for_course(course, state, notebook_cache)
        state["courses"][course_id] = {
            "course_id": course["id"],
            "fullname": course.get("fullname"),
            "shortname": course.get("shortname"),
            "viewurl": course.get("viewurl"),
            "notebook_id": nb_id,
            "notebook_title": nb_title,
            "updated_at": int(time.time()),
        }
        course_map.append(state["courses"][course_id])

        state.setdefault("files", {}).setdefault(course_id, {})
        state.setdefault("ignored", {}).setdefault(course_id, {})

        try:
            course_state = fetch_course_state(sesskey, int(course["id"]))
        except Exception as e:
            log(f"  ! Errore course state: {e}")
            continue

        cms = course_state.get("cm", [])
        folders = [
            cm
            for cm in cms
            if cm.get("module") == "folder"
            or cm.get("plugin") == "mod_folder"
            or cm.get("modname") == "Cartella"
        ]
        log(f"  Cartelle trovate: {len(folders)}")

        for folder in folders:
            folder_id = str(folder.get("id"))
            folder_url = folder.get("url") or f"{BASE_URL}/mod/folder/view.php?id={folder_id}"
            try:
                folder_html = http_request(folder_url, method="GET")
            except Exception as e:
                log(f"    - Skip folder {folder_id}: {e}")
                continue

            file_links = extract_folder_links(folder_html)
            if not file_links:
                continue

            for href, name in file_links:
                if href.startswith("/"):
                    href = BASE_URL + href
                file_url = normalize_url(href)
                file_key = f"{folder_id}:{file_url}"
                if file_key in state["ignored"][course_id]:
                    skipped_count += 1
                    continue

                parsed = urllib.parse.urlsplit(file_url)
                base_name = urllib.parse.unquote(Path(parsed.path).name) or name
                filename = safe_filename(base_name or name)
                local_dir = DOWNLOAD_DIR / course_id / folder_id
                local_dir.mkdir(parents=True, exist_ok=True)
                local_path = local_dir / filename

                # download file
                try:
                    local_path.write_bytes(http_request_bytes(href, method="GET"))
                except Exception as e:
                    log(f"    - Download fallito {filename}: {e}")
                    skipped_count += 1
                    continue

                file_hash = sha256_file(local_path)
                prev = state["files"][course_id].get(file_key, {})
                if prev.get("sha256") == file_hash:
                    skipped_count += 1
                    continue

                # upload source to NotebookLM
                try:
                    added = run_notebooklm(
                        ["source", "add", str(local_path), "-n", nb_id, "--type", "file"]
                    )
                    source_id = added["source"]["id"]
                    ready = wait_source(nb_id, source_id)
                    if not ready:
                        state["ignored"][course_id][file_key] = {
                            "reason": "source_processing_failed",
                            "filename": filename,
                        }
                        log(f"    - Ignorato (non processabile): {filename}")
                        skipped_count += 1
                        continue
                    state["files"][course_id][file_key] = {
                        "filename": filename,
                        "sha256": file_hash,
                        "source_id": source_id,
                        "uploaded_at": int(time.time()),
                    }
                    uploaded_count += 1
                    log(f"    + Upload OK: {filename}")
                except Exception as e:
                    state["ignored"][course_id][file_key] = {
                        "reason": "source_add_failed",
                        "filename": filename,
                        "error": str(e)[:300],
                    }
                    log(f"    - Ignorato (upload fallito): {filename}")
                    skipped_count += 1

            write_state(state)

    MAP_PATH.write_text(json.dumps({"updated_at": int(time.time()), "courses": course_map}, indent=2), encoding="utf-8")
    write_state(state)

    log(f"Sync completata. Upload nuovi: {uploaded_count}, saltati: {skipped_count}")
    log(f"Mappa corsi/notebook: {MAP_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
