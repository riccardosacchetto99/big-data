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
COURSE_DOCS_ROOT = ROOT / "materiali_studio_notebooklm" / "courses"

BASE_URL = os.getenv("UNINSUBRIA_BASE_URL", "https://elearning.uninsubria.it")
MY_URL = f"{BASE_URL}/my/"
COOKIE = os.getenv(
    "COOKIE_HEADER",
    "_shibsession_656c6561726e696e672e756e696e7375627269612e697468747470733a2f2f73702d656c6561726e696e672d756e696e7375627269612d70726f642e63696e6563612e69742f73686962626f6c657468=_c60e10d3e594c4bae5c9efedbe81d37d; MoodleSessioninsubriaprod=r4thbvfikpakfcpq2rl893ajd8",
)

SKIP_FILE_EXTENSIONS = {
    ".csv",
    ".tsv",
    ".xls",
    ".xlsx",
    ".ods",
    ".xlsm",
    ".xlsb",
}
SKIP_COURSE_KEYWORDS = {"machine learning"}


CHAPTER_SPECS = [
    (
        "cap_01_quadro_generale.md",
        "Capitolo 1 - Quadro generale del corso",
        "Obiettivi del corso, lessico tecnico, prerequisiti, mappa dei contenuti e collegamenti tra i temi.",
    ),
    (
        "cap_02_fondamenti_teorici.md",
        "Capitolo 2 - Fondamenti teorici",
        "Teoria completa con definizioni rigorose, assunzioni, modelli e proprietà formali quando presenti.",
    ),
    (
        "cap_03_metodi_e_procedure.md",
        "Capitolo 3 - Metodi e procedure operative",
        "Workflow, passi operativi, procedure e checklist applicative con attenzione agli errori comuni.",
    ),
    (
        "cap_04_casi_studio_e_esempi.md",
        "Capitolo 4 - Casi studio ed esempi concreti",
        "Esempi solidi e realistici, confronto tra alternative, trade-off, scelte progettuali motivate.",
    ),
    (
        "cap_05_esercizi_guidati.md",
        "Capitolo 5 - Esercizi guidati con soluzione",
        "Esercizi progressivi con svolgimento, ragionamento passo-passo e verifica finale.",
    ),
    (
        "cap_06_simulazione_esame.md",
        "Capitolo 6 - Simulazione d'esame",
        "Simulazione completa in stile parziale con criteri di valutazione e rubriche.",
    ),
    (
        "cap_07_errori_frequenti.md",
        "Capitolo 7 - Errori frequenti e ripasso",
        "Errori tipici, anti-pattern, domande trabocchetto e strategia di ripasso finale.",
    ),
]


def log(msg: str) -> None:
    print(msg, flush=True)


def read_state() -> dict:
    if not STATE_PATH.exists():
        return {"version": 2, "courses": {}, "files": {}, "ignored": {}}
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        state.setdefault("version", 2)
        state.setdefault("courses", {})
        state.setdefault("files", {})
        state.setdefault("ignored", {})
        return state
    except Exception:
        return {"version": 2, "courses": {}, "files": {}, "ignored": {}}


def write_state(state: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "corso"


def should_skip_course(course: dict) -> bool:
    name = (course.get("fullname") or "").lower()
    return any(k in name for k in SKIP_COURSE_KEYWORDS)


def should_skip_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in SKIP_FILE_EXTENSIONS


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


def parse_json_from_text(text: str) -> dict | list:
    text = (text or "").strip()
    if not text:
        raise RuntimeError("Output vuoto")
    start_obj = text.find("{")
    start_arr = text.find("[")
    starts = [x for x in (start_obj, start_arr) if x >= 0]
    if not starts:
        raise RuntimeError("Output JSON non trovato")
    start = min(starts)
    return json.loads(text[start:])


def run_notebooklm_json(args: list[str]) -> dict | list:
    cmd = ["notebooklm"] + args + ["--json"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    if proc.returncode != 0:
        raise RuntimeError(f"Comando fallito: {' '.join(cmd)}\n{text[:800]}")
    return parse_json_from_text(text)


def run_notebooklm_maybe_json(args: list[str]) -> tuple[bool, str]:
    cmd = ["notebooklm"] + args + ["--json"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode == 0, text


def run_notebooklm_plain(args: list[str]) -> str:
    proc = subprocess.run(["notebooklm"] + args, capture_output=True, text=True)
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    if proc.returncode != 0:
        raise RuntimeError(f"Comando fallito: notebooklm {' '.join(args)}\n{text[:800]}")
    return text


def use_notebook_context(notebook_id: str) -> None:
    proc = subprocess.run(["notebooklm", "use", notebook_id], capture_output=True, text=True)
    if proc.returncode != 0:
        text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        raise RuntimeError(f"Impossibile selezionare notebook {notebook_id}: {text[:400]}")


def find_first_artifact_id(payload: object) -> str | None:
    if isinstance(payload, dict):
        if isinstance(payload.get("artifact"), dict) and payload["artifact"].get("id"):
            return str(payload["artifact"]["id"])
        if payload.get("id") and any(k in payload for k in ("type", "status", "artifact")):
            return str(payload["id"])
        for v in payload.values():
            found = find_first_artifact_id(v)
            if found:
                return found
    elif isinstance(payload, list):
        for item in payload:
            found = find_first_artifact_id(item)
            if found:
                return found
    return None


def list_notebooks() -> list[dict]:
    out = run_notebooklm_json(["list"])
    return out.get("notebooks", []) if isinstance(out, dict) else []


def ensure_notebook_for_course(course: dict, state: dict, notebook_cache: list[dict]) -> tuple[str, str]:
    course_id = str(course["id"])
    fullname = (course["fullname"] or "").strip()
    title = f"UNINSUBRIA COURSE {course_id} - {fullname}"

    existing = state["courses"].get(course_id, {})
    if existing.get("notebook_id"):
        return existing["notebook_id"], existing.get("notebook_title", title)

    for nb in notebook_cache:
        nb_title = (nb.get("title") or "").strip()
        if f"UNINSUBRIA COURSE {course_id} -" in nb_title:
            return nb["id"], nb_title

    created = run_notebooklm_json(["create", title])
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


def generate_chapter_report(notebook_id: str, course_name: str, chapter_title: str, guidance: str, output_path: Path) -> bool:
    prompt = (
        f"Genera in italiano un documento molto lungo e approfondito per '{course_name}'. "
        f"Titolo obbligatorio: '{chapter_title}'. "
        f"Contenuto richiesto: {guidance} "
        "Includi: spiegazioni rigorose, esempi concreti, esercizi con soluzione, errori frequenti, "
        "domande di autovalutazione e mini-riepilogo finale. Usa struttura chiara con sezioni e sottosezioni."
    )

    generated = run_notebooklm_json(
        [
            "generate",
            "report",
            prompt,
            "--format",
            "custom",
            "--language",
            "it",
            "--wait",
        ]
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    run_notebooklm_plain(["download", "report", str(output_path), "--latest", "--force"])
    return True


def generate_mind_map(notebook_id: str, output_path: Path) -> bool:
    generated = run_notebooklm_json(["generate", "mind-map"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(generated, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def trigger_audio_overview(notebook_id: str, course_name: str) -> bool:
    ok, text = run_notebooklm_maybe_json(
        [
            "generate",
            "audio",
            f"Overview completa in italiano per {course_name}, con focus su concetti chiave, collegamenti tra capitoli e priorita di studio.",
            "--format",
            "deep-dive",
            "--length",
            "long",
            "--language",
            "it",
            "--no-wait",
        ]
    )
    if not ok:
        log(f"    - Avvio audio non riuscito: {text[:300]}")
    return ok


def regenerate_course_materials(course: dict, notebook_id: str, state: dict) -> None:
    course_id = str(course["id"])
    course_name = course.get("fullname") or f"Course {course_id}"
    course_slug = slugify(course_name)
    course_dir = COURSE_DOCS_ROOT / f"{course_id}-{course_slug}"
    course_dir.mkdir(parents=True, exist_ok=True)
    use_notebook_context(notebook_id)

    log("  Rigenerazione materiali studio (capitoli, mappa, audio)...")

    index_lines = [
        f"# Materiali studio - {course_name}",
        "",
        f"- Course ID: `{course_id}`",
        f"- Notebook ID: `{notebook_id}`",
        f"- Ultima rigenerazione: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Capitoli",
    ]

    for idx, (filename, chapter_title, guidance) in enumerate(CHAPTER_SPECS, start=1):
        chapter_path = course_dir / filename
        ok = generate_chapter_report(notebook_id, course_name, chapter_title, guidance, chapter_path)
        if ok:
            log(f"    + Capitolo {idx} aggiornato: {filename}")
        index_lines.append(f"- [Capitolo {idx}: {chapter_title}]({filename})")

    mind_map_path = course_dir / "mappa_concettuale.json"
    try:
        generate_mind_map(notebook_id, mind_map_path)
        log("    + Mappa concettuale aggiornata")
        index_lines.append("- [Mappa concettuale](mappa_concettuale.json)")
    except Exception as e:
        log(f"    - Mappa concettuale non generata: {e}")

    trigger_audio_overview(notebook_id, course_name)
    index_lines.append("- Overview audio avviata su NotebookLM (generazione asincrona)")

    index_path = course_dir / "index.md"
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    state["courses"].setdefault(course_id, {})
    state["courses"][course_id]["materials_dir"] = str(course_dir.relative_to(ROOT))
    state["courses"][course_id]["last_regeneration_at"] = int(time.time())


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync corsi Uninsubria -> NotebookLM + materiali studio")
    parser.add_argument("--max-courses", type=int, default=0, help="Limita numero corsi (0 = tutti)")
    parser.add_argument(
        "--regenerate-course-id",
        type=str,
        default="",
        help="Rigenera subito i materiali per un corso gia mappato (senza fare sync file)",
    )
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    COURSE_DOCS_ROOT.mkdir(parents=True, exist_ok=True)
    state = read_state()
    notebook_cache = list_notebooks()

    if args.regenerate_course_id:
        cid = str(args.regenerate_course_id).strip()
        course_state = state.get("courses", {}).get(cid)
        if not course_state or not course_state.get("notebook_id"):
            raise RuntimeError(f"Corso {cid} non trovato nello stato locale oppure notebook_id mancante.")
        course_obj = {"id": int(cid), "fullname": course_state.get("fullname") or f"Course {cid}"}
        regenerate_course_materials(course_obj, course_state["notebook_id"], state)
        write_state(state)
        log(f"Rigenerazione completata per corso {cid}")
        return 0

    log("Recupero sesskey...")
    sesskey = extract_sesskey()
    log(f"Sesskey OK: {sesskey}")

    log("Recupero corsi...")
    courses = fetch_courses(sesskey)
    courses = [c for c in courses if not should_skip_course(c)]
    if args.max_courses > 0:
        courses = courses[: args.max_courses]
    log(f"Corsi trovati (dopo filtri): {len(courses)}")

    course_map = []
    uploaded_count = 0
    skipped_count = 0
    regenerated_courses = 0

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
            "materials_dir": state["courses"].get(course_id, {}).get("materials_dir"),
            "last_regeneration_at": state["courses"].get(course_id, {}).get("last_regeneration_at"),
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

        new_uploads_for_course = 0

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

                if should_skip_file(filename):
                    state["ignored"][course_id][file_key] = {
                        "reason": "filetype_excluded",
                        "filename": filename,
                    }
                    skipped_count += 1
                    continue

                local_dir = DOWNLOAD_DIR / course_id / folder_id
                local_dir.mkdir(parents=True, exist_ok=True)
                local_path = local_dir / filename

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

                try:
                    added = run_notebooklm_json(["source", "add", str(local_path), "-n", nb_id, "--type", "file"])
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
                    new_uploads_for_course += 1
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

        if new_uploads_for_course > 0:
            regenerate_course_materials(course, nb_id, state)
            regenerated_courses += 1
        else:
            log("  Nessun nuovo file: materiali non rigenerati")

        write_state(state)

    MAP_PATH.write_text(json.dumps({"updated_at": int(time.time()), "courses": course_map}, indent=2), encoding="utf-8")
    write_state(state)

    log(
        "Sync completata. "
        f"Upload nuovi: {uploaded_count}, "
        f"saltati: {skipped_count}, "
        f"corsi rigenerati: {regenerated_courses}"
    )
    log(f"Mappa corsi/notebook: {MAP_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
