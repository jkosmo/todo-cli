from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

DB: Path = Path(__file__).with_name("todo.json")


def load() -> List[Dict[str, Any]]:
    if DB.exists():
        text = DB.read_text(encoding="utf-8")
        if text.strip():
            return json.loads(text)
    return []


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


def remove(idx: int) -> None:
    items = load()
    if idx < 0 or idx >= len(items):
        raise IndexError("Ugyldig indeks.")
    items.pop(idx)
    save(items)


def edit(idx: int, new_title: str) -> None:
    items = load()
    if idx < 0 or idx >= len(items):
        raise IndexError("Ugyldig indeks.")
    title = new_title.strip()
    if not title:
        raise ValueError("Tittel kan ikke være tom.")
    items[idx]["title"] = title
    save(items)


def list_items(*, as_json: bool | None = None, json_mode: bool | None = None) -> None:
    items = load()
    flag = as_json if as_json is not None else bool(json_mode)
    if flag:
        import json

        print(json.dumps(items, ensure_ascii=False, indent=2))
        return
    if not items:
        print("(ingen oppgaver)")
        return
    for i, it in enumerate(items):
        mark = "[x]" if it.get("done") else "[ ]"
        print(f"{i}: {mark} {it.get('title','')}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="todo", description="En enkel Todo CLI")
    parser.add_argument(
        "--db", type=str, default=None, help="Sti til JSON-database (valgfritt)"
    )
    parser.add_argument("--json", action="store_true", help="Skriv ut JSON ved 'list'")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="Legg til en oppgave")
    p_add.add_argument("title", nargs="+", help="Tittel på oppgaven")

    p_done = sub.add_parser("done", help="Marker som utført")
    p_done.add_argument("index", type=int, help="Indeks (se 'list')")

    p_remove = sub.add_parser("remove", help="Fjern en oppgave")
    p_remove.add_argument("index", type=int, help="Indeks (se 'list')")

    p_edit = sub.add_parser("edit", help="Rediger en oppgave")
    p_edit.add_argument("index", type=int, help="Indeks (se 'list')")
    p_edit.add_argument("title", nargs="+", help="Ny tittel")

    sub.add_parser("list", help="Vis oppgaver")

    try:
        ns = parser.parse_args(argv)
        if ns.db:
            global DB
            DB = Path(ns.db)

        if ns.cmd == "add":
            add(" ".join(ns.title))
        elif ns.cmd == "done":
            done(ns.index)
        elif ns.cmd == "remove":
            remove(ns.index)
        elif ns.cmd == "edit":
            edit(ns.index, " ".join(ns.title))
        else:
            list_items(as_json=bool(getattr(ns, "json", False)))
    except (ValueError, IndexError) as e:
        print(f"Feil: {e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
