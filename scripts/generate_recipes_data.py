#!/usr/bin/env python3
"""
Liest Cloud-Vault-Rezepte und erzeugt src/lib/recipesData.js
mit echten Einzelschritten (1 Schritt = 1 Screen), Zutaten-Checklist,
Timern und Parallel-Hinweisen.
"""
from __future__ import annotations

import glob
import json
import os
import re
from pathlib import Path

import yaml

VAULT = Path(
    "/Users/felix/Library/Mobile Documents/iCloud~md~obsidian/Documents/Cloud Vault/Rezepte"
)
OUT = Path(__file__).resolve().parents[1] / "src" / "lib" / "recipesData.js"

DEFAULT_IMAGE = (
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
    "?auto=format&fit=crop&w=600&q=80"
)

SKIP = {"Einkaufsliste.md", "Wochenplan.md", "Übersicht.md"}

# Menge am Zeilenanfang: 500g, 1,2 L, ½ EL, 1½ EL, ca. 90g, 2–3 EL, 4 × 60g …
QTY_RE = re.compile(
    r"^[-*]\s*"
    r"(?P<qty>"
    r"(?:ca\.\s*)?"
    r"(?:\d+[×x]\s*)?"
    r"(?:\d+(?:[.,]\d+)?|\d*½|\d*¼|\d*¾|½|¼|¾|1½|2½)"
    r"(?:\s*[–-]\s*(?:\d+(?:[.,]\d+)?|½|¼|¾))?"
    r")"
    r"\s*"
    r"(?P<unit>g|kg|ml|l|L|EL|TL|Stk|Stück|Bund|Dose|Dosen|Zehen?|Prise|Packung|x)?"
    r"\s*"
    r"(?P<name>.+)$",
    re.IGNORECASE,
)

# Mit Bold-Titel: 1. **Fleisch anbraten (7 Min):** Text…
STEP_BOLD_RE = re.compile(
    r"^\s*(\d+)\.\s+\*\*(.+?)\*\*:?\s*(.*)$",
    re.MULTILINE,
)
# Ohne Bold: 1. Zwiebel in Öl anschwitzen (3 min)
STEP_PLAIN_RE = re.compile(
    r"^\s*(\d+)\.\s+(.+)$",
    re.MULTILINE,
)

# Zeit im Header: (5 Min), (15–20 Min), (mind. 8 Std), (10 Min Ruhezeit)
TIME_IN_HEADER = re.compile(
    r"\((?:mind\.\s*)?(?:ca\.\s*)?(\d+)\s*(?:[–-]\s*(\d+))?\s*(Min|min|Minuten|Std|Stunden|h)[^)]*\)",
    re.IGNORECASE,
)

PARALLEL_MARKERS = re.compile(
    r"(?i)(in der zwischenzeit|währenddessen|parallel|separat kochen|"
    r"während .+? (?:köcheln|ruhen|ziehen|quellen|mariniert)|"
    r"beilage:.+separat)"
)


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[ä]", "ae", s)
    s = re.sub(r"[ö]", "oe", s)
    s = re.sub(r"[ü]", "ue", s)
    s = re.sub(r"[ß]", "ss", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "rezept"


def parse_fraction(tok: str) -> float:
    tok = tok.strip().replace(",", ".")
    mapping = {"½": 0.5, "¼": 0.25, "¾": 0.75, "1½": 1.5, "2½": 2.5}
    if tok in mapping:
        return mapping[tok]
    # 1×60 or 4x60
    if "×" in tok or "x" in tok.lower():
        parts = re.split(r"[×xX]", tok)
        try:
            return float(parts[0]) * float(parts[1])
        except Exception:
            return 1.0
    # 2–3 → take lower
    if "–" in tok or "-" in tok:
        parts = re.split(r"[–-]", tok)
        try:
            return float(parts[0])
        except Exception:
            return 1.0
    # 1½ style mixed
    m = re.match(r"^(\d+)(½|¼|¾)$", tok)
    if m:
        return float(m.group(1)) + {"½": 0.5, "¼": 0.25, "¾": 0.75}[m.group(2)]
    try:
        return float(tok)
    except Exception:
        return 1.0


def parse_ingredient_line(line: str) -> dict | None:
    line = line.strip()
    if not line.startswith(("-", "*")):
        return None
    m = QTY_RE.match(line)
    if not m:
        name = re.sub(r"^[-*]\s*", "", line).strip()
        if not name or name.startswith("**"):
            return None
        return {"name": name, "baseQty": 1, "unit": "x"}
    qty_raw = m.group("qty") or "1"
    unit = (m.group("unit") or "").strip() or "x"
    name = (m.group("name") or "").strip()
    # strip leading punctuation left on name
    name = re.sub(r"^[:\s]+", "", name)
    if not name:
        return None
    # "ca. 90g" already handled; "4 × 60g Reis" name may include rest
    qty = parse_fraction(qty_raw.replace("ca.", "").strip())
    return {"name": name, "baseQty": qty, "unit": unit}


def extract_section(body: str, *headers: str) -> str:
    """Return markdown section content under the first matching ## header."""
    for h in headers:
        pat = re.compile(
            rf"^##\s+{re.escape(h)}\s*$",
            re.IGNORECASE | re.MULTILINE,
        )
        m = pat.search(body)
        if not m:
            continue
        start = m.end()
        nxt = re.search(r"^##\s+", body[start:], re.MULTILINE)
        end = start + nxt.start() if nxt else len(body)
        return body[start:end].strip()
    return ""


def extract_ingredients(body: str) -> list[dict]:
    # Prefer batch / main list, fall back to any Zutaten section
    section = extract_section(
        body,
        "Zutaten Batch (4 Portionen)",
        "Zutaten Batch (3 Portionen)",
        "Zutaten (3 Portionen Sauce)",
        "Zutaten Teig (4 Portionen / 4 Pizzen à 200g)",
        "Zutaten für 1 Glas Würzpaste (reicht für ca. 12,5–15 Liter Brühe)",
    )
    if not section:
        # generic: first ## Zutaten… that is not "pro Portion"
        for m in re.finditer(r"^##\s+(Zutaten[^\n]*)$", body, re.MULTILINE | re.I):
            title = m.group(1)
            if "pro portion" in title.lower():
                continue
            start = m.end()
            nxt = re.search(r"^##\s+", body[start:], re.MULTILINE)
            end = start + nxt.start() if nxt else len(body)
            section = body[start:end].strip()
            break

    items = []
    for line in section.splitlines():
        ing = parse_ingredient_line(line)
        if ing:
            items.append(ing)
    return items


def timer_from_header(header: str) -> int | None:
    m = TIME_IN_HEADER.search(header)
    if not m:
        return None
    low = int(m.group(1))
    high = int(m.group(2)) if m.group(2) else low
    unit = m.group(3).lower()
    # use lower bound for active cooking feel; for ranges like 15-20 use high if idle words
    minutes = high if re.search(r"(?i)ruhe|köchel|quellen|ziehen|garen|simmer", header) else low
    if unit.startswith("std") or unit == "h":
        return minutes * 3600
    return minutes * 60


def clean_header(header: str) -> str:
    # strip trailing time for cleaner display title? keep time — useful
    return header.strip().rstrip(":")


def _build_step(header: str, body_text: str) -> dict:
    body_text, parallel = split_parallel_from_body(body_text)
    timer = timer_from_header(header)

    # long idle steps without timer in header — scan body
    if timer is None:
        m_idle = re.search(
            r"(?i)(\d+)\s*(?:[–-]\s*(\d+))?\s*(?:Min(?:uten?)?|min)\b",
            header + " " + body_text,
        )
        if m_idle:
            minutes = int(m_idle.group(2) or m_idle.group(1))
            # only set timer if looks like cooking wait (not "2 EL")
            context = (header + " " + body_text)[max(0, m_idle.start() - 20) : m_idle.end() + 40]
            if re.search(
                r"(?i)(min|köchel|braten|rösten|dämpfen|ziehen|ruhen|quellen|anschwitzen|garen|mixen|sek)",
                context,
            ) or "min" in header.lower():
                timer = minutes * 60
        # seconds: "30 Sekunden"
        m_sec = re.search(r"(?i)(\d+)\s*Sekunden?", header + " " + body_text)
        if timer is None and m_sec:
            timer = int(m_sec.group(1))

    return {
        "header": header,
        "body": body_text,
        "parallel": parallel,
        "timer": timer,
    }


def split_parallel_from_body(body: str) -> tuple[str, str | None]:
    """If body contains parallel markers, surface a parallel note."""
    parallel = None
    text = body.strip()

    # "In der Zwischenzeit X." → parallel = X
    m = re.search(
        r"(?i)(?:in der zwischenzeit|währenddessen)\s+(.+?)(?:\.|$)",
        text,
    )
    if m:
        parallel = m.group(0).strip()
        # keep full body — cook needs context — but also flag parallel

    # explicit "Beilage … separat"
    m2 = re.search(r"(?i)(beilage[^.]*separat[^.]*\.)", text)
    if m2 and not parallel:
        parallel = m2.group(1).strip()

    return text, parallel


def extract_steps(body: str) -> list[dict]:
    section = extract_section(body, "Zubereitung")
    if not section:
        # fallback: whole body after frontmatter-ish content
        section = body

    steps = []
    bold_matches = list(STEP_BOLD_RE.finditer(section))
    if bold_matches:
        for i, m in enumerate(bold_matches):
            header = clean_header(m.group(2))
            first = (m.group(3) or "").strip()
            start = m.end()
            end = bold_matches[i + 1].start() if i + 1 < len(bold_matches) else len(section)
            rest = section[start:end].strip()
            body_text = (first + ("\n" + rest if rest else "")).strip()
            body_text = re.split(r"\n##\s+", body_text)[0].strip()
            steps.append(_build_step(header, body_text))
    else:
        plain = list(STEP_PLAIN_RE.finditer(section))
        if not plain:
            clean = re.sub(r"^#+ .*$", "", section, flags=re.MULTILINE).strip()
            if clean:
                steps.append(
                    {
                        "header": "Zubereitung",
                        "body": clean[:2000],
                        "parallel": None,
                        "timer": None,
                    }
                )
            return steps

        for i, m in enumerate(plain):
            line = m.group(2).strip()
            # "Titel (3 min)" oder "Titel — Text" oder nur "Titel"
            header = line
            body_text = line
            # If line is short, header = full line as title, body repeats (one-liner steps)
            # Prefer: extract trailing time as part of header, body = same instruction
            tm = TIME_IN_HEADER.search(line)
            if tm:
                # "Zwiebel in Öl anschwitzen (3 min)" → header keeps time, body is instruction
                header = line
                body_text = line
            else:
                # bare: "Öl in Pfanne erhitzen"
                header = line[:80]
                body_text = line

            # multi-line continuation until next number
            start = m.end()
            end = plain[i + 1].start() if i + 1 < len(plain) else len(section)
            rest = section[start:end].strip()
            rest = re.split(r"\n##\s+", rest)[0].strip()
            if rest:
                body_text = (body_text + "\n" + rest).strip()

            steps.append(_build_step(header, body_text))

    # "In der Zwischenzeit" im Schritt → als Parallel am VORHERIGEN Warte-Schritt hängen
    for i, step in enumerate(steps):
        if not re.search(r"(?i)in der zwischenzeit|währenddessen", step["body"] or ""):
            continue
        # am aktuellen Schritt als Parallel-Badge
        if not step["parallel"]:
            step["parallel"] = "Während der Wartezeit des vorherigen Schritts erledigen"
        if i > 0:
            prev = steps[i - 1]
            preview = step["body"][:160].rstrip()
            if len(step["body"]) > 160:
                preview += "…"
            note = f"⚡ Parallel: {step['header']} — {preview}"
            if prev["parallel"]:
                if step["header"].lower() not in prev["parallel"].lower():
                    prev["parallel"] = prev["parallel"] + "\n" + note
            else:
                prev["parallel"] = note

    # Beilage separat / Pasta frisch — nur aus Aufzählungszeilen (nicht Intro-Fließtext)
    side_notes = []
    for line in body.splitlines():
        if not re.match(r"^\s*[-*]\s+", line):
            continue
        raw = re.sub(r"^[-*]\s*", "", line).strip()
        if re.search(
            r"(?i)(beilage:.*(separat|frisch|kochen)|pasta.*frisch kochen|nudeln.*frisch)",
            raw,
        ):
            side_notes.append(raw)
    if side_notes:
        target = next(
            (s for s in steps if s.get("timer") and s["timer"] >= 600),
            next((s for s in steps if s.get("timer")), steps[0] if steps else None),
        )
        if target:
            for side in side_notes:
                note = f"⚡ Parallel: {side}"
                if target["parallel"] and side.lower() in target["parallel"].lower():
                    continue
                target["parallel"] = (
                    (target["parallel"] + "\n" + note) if target["parallel"] else note
                )

    # Lange Wartezeit: konkrete Parallel-Tasks aus späteren Schritten ableiten
    for i, step in enumerate(steps[:-1]):
        if step.get("parallel"):
            continue
        if not step.get("timer") or step["timer"] < 900:
            continue
        if not re.search(
            r"(?i)köcheln|quellen lassen|ruhezeit|gehzeit|ziehen lassen",
            step["header"] + " " + (step["body"] or ""),
        ):
            continue
        later = " ".join(s["header"] + " " + (s["body"] or "") for s in steps[i + 1 :])
        now = step["header"] + " " + (step["body"] or "")
        hints = []
        if re.search(r"(?i)würstchen", later):
            hints.append("Würstchen schon in Scheiben schneiden")
        # Reis nur wenn separat erwähnt und nicht schon in diesem Schritt
        if re.search(r"(?i)beilage:.*\breis\b|\breis\b.*separat", body) and not re.search(
            r"(?i)\breis\b", now
        ):
            hints.append("Reis separat aufsetzen")
        # Pasta separat nur wenn Rezept sagt "frisch kochen" und dieser Schritt kein Nudel-Garen ist
        if (
            re.search(r"(?i)pasta.*frisch kochen|nudeln.*frisch", body)
            and not re.search(r"(?i)nudel|pasta|orecchiette|spaghetti", now)
        ):
            hints.append("Pasta-Wasser aufsetzen (Pasta erst zum Schluss kochen)")
        if re.search(r"(?i)portionieren|einfrieren", later):
            hints.append("Dosen/Behälter fürs Portionieren bereitstellen")
        if hints:
            step["parallel"] = "⚡ Parallel möglich: " + " · ".join(hints)

    return steps


def pick_base_ingredient(checklist: list[dict]) -> tuple[str, float, str]:
    if not checklist:
        return "Portion", 1.0, "x"
    # prefer protein-ish first item with grams
    for item in checklist:
        if item["unit"].lower() in ("g", "kg") and item["baseQty"] >= 100:
            return item["name"].split("(")[0].strip()[:40], float(item["baseQty"]), item["unit"]
    item = checklist[0]
    return item["name"].split("(")[0].strip()[:40], float(item["baseQty"]), item["unit"]


def category_from_path(rel: str) -> str:
    if "Frühstück" in rel:
        return "Frühstück"
    if "Snack" in rel or "Basics" in rel:
        return "Basics"
    return "Hauptmahlzeit"


def load_recipe(fpath: Path) -> dict | None:
    raw = fpath.read_text(encoding="utf-8")
    parts = raw.split("---")
    if len(parts) < 3:
        return None
    try:
        meta = yaml.safe_load(parts[1])
    except Exception:
        return None
    if not isinstance(meta, dict):
        return None

    body = "---".join(parts[2:]).strip()
    title = str(meta.get("titel") or fpath.stem)
    try:
        rating = int(str(meta.get("rating") or 5).strip("\"'"))
    except Exception:
        rating = 5
    if not meta.get("rating"):
        rating = 5

    portionen = int(meta.get("portionen") or 4)
    batch = bool(meta.get("batch", False))
    einfrierbar = bool(meta.get("einfrierbar", False))
    zeit = int(meta.get("zubereitungszeit_min") or 30)
    try:
        kcal = int(meta.get("kcal_portion") or 400)
    except Exception:
        kcal = 400
    try:
        protein = int(meta.get("protein_g_portion") or 20)
    except Exception:
        protein = 20

    checklist = extract_ingredients(body)
    steps = extract_steps(body)
    base_name, base_qty, unit = pick_base_ingredient(checklist)

    rel = str(fpath.relative_to(VAULT))
    cat = category_from_path(rel)

    tags = []
    if protein >= 25:
        tags.append("protein")
    if batch:
        tags.append("prep")
    if zeit <= 30:
        tags.append("quick")

    return {
        "id": slugify(title) + (f"-batch-x-{portionen}" if batch else ""),
        "title": title,
        "category": cat,
        "rating": rating,
        "prepTimeMin": zeit,
        "kcalPortion": kcal,
        "proteinPortion": protein,
        "batch": batch,
        "portionen": portionen,
        "einfrierbar": einfrierbar,
        "image": DEFAULT_IMAGE,
        "tags": tags,
        "baseIngredientName": base_name,
        "baseIngredientQty": base_qty,
        "unit": unit,
        "checklist": checklist
        or [{"name": "Zutaten nach Rezept", "baseQty": 1, "unit": "Portion"}],
        "steps": steps
        or [
            {
                "header": "Zubereitung",
                "body": body[:1500],
                "parallel": None,
                "timer": None,
            }
        ],
    }


def main() -> None:
    files = sorted(VAULT.rglob("*.md"))
    recipes = []
    for fpath in files:
        if fpath.name in SKIP:
            continue
        rec = load_recipe(fpath)
        if rec:
            recipes.append(rec)
            print(f"  ✓ {rec['title']}: {len(rec['steps'])} Schritte, {len(rec['checklist'])} Zutaten")
        else:
            print(f"  ✗ skip {fpath.name}")

    leftovers = [
        {
            "id": "rest-1",
            "title": "Omas Kartoffelsuppe",
            "qty": 2,
            "unit": "Portionen",
            "addedDate": "2026-07-24",
            "daysRemaining": 2,
        },
        {
            "id": "rest-2",
            "title": "Hähnchen süß-sauer",
            "qty": 1,
            "unit": "Portion",
            "addedDate": "2026-07-25",
            "daysRemaining": 3,
        },
    ]
    freezer = [
        {
            "id": "freezer-1",
            "title": "Hühnerfrikassee Batch",
            "qty": 3,
            "unit": "Dosen",
            "frozenDate": "2026-07-20",
            "mhd": "2026-10-20",
        },
        {
            "id": "freezer-2",
            "title": "Linsen-Bolognese",
            "qty": 2,
            "unit": "Dosen",
            "frozenDate": "2026-07-21",
            "mhd": "2026-10-21",
        },
        {
            "id": "freezer-3",
            "title": "Muffins Hafer (Batch x 4)",
            "qty": 4,
            "unit": "Stück",
            "frozenDate": "2026-07-22",
            "mhd": "2026-09-22",
        },
    ]

    js = (
        "/* AUTO-GENERATED by scripts/generate_recipes_data.py — nicht von Hand editieren */\n"
        f"export const initialRecipes = {json.dumps(recipes, ensure_ascii=False, indent=2)};\n\n"
        f"export const initialLeftovers = {json.dumps(leftovers, ensure_ascii=False, indent=2)};\n\n"
        f"export const initialFreezerItems = {json.dumps(freezer, ensure_ascii=False, indent=2)};\n"
    )
    OUT.write_text(js, encoding="utf-8")
    print(f"\n✅ {len(recipes)} Rezepte → {OUT}")


if __name__ == "__main__":
    main()
