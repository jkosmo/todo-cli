from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

DB: Path = Path(__file__).with_name("todo.json")

def load() -> List[Dict[str, Any]]:
    return json.loads(DB.read_text("utf-8")) if DB.exists() and DB.read_text().strip() else []

def save(items: List[Dict[str, Any]]) -> None:
    DB.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")

def add(title: str) -> None:
    title = title.strip()
    if not title:
        raise ValueError("Tittel kan ikke være tom.")
    items = load()
    items.append({"title": title, "done": False})
    save(items)

def done(idx: int) -> None:
    items = load()
    if idx < 0 or idx >= len(items):
        raise IndexError("Ugyldig indeks.")
    items[idx]["done"] = True
    save(items)

def list_items() -> None:
    items = load()
    if not items:
        print("(ingen oppgaver)")
        return
    for i, it in enumerate(items):
        mark = "[x]" if it.get("done") else "[ ]"
        print(f"{i}: {mark} {it.get('title','')}")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="todo", description="En enkel Todo CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="Legg til en oppgave")
    p_add.add_argument("title", nargs="+", help="Tittel på oppgaven")

    p_done = sub.add_parser("done", help="Marker som utført")
    p_done.add_argument("index", type=int, help="Indeks (se 'list')")

    sub.add_parser("list", help="Vis oppgaver")

    ns = parser.parse_args(argv)

    try:
        if ns.cmd == "add":
            add(" ".join(ns.title))
        elif ns.cmd == "done":
            done(ns.index)
        else:
            list_items()
    except (ValueError, IndexError) as e:
        print(f"Feil: {e}")
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
