"""
Sync tropes.json with tropes found in books.json.

Loads books.json, extracts all unique trope names, and ensures each one
exists in tropes.json. Missing tropes are appended with featured=false,
canonical=false, and an empty description.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS_PATH = ROOT / "src" / "data" / "books.json"
TROPES_PATH = ROOT / "src" / "data" / "tropes.json"


def name_to_slug(name: str) -> str:
    return re.sub(r"[/]+", "-", name.lower().strip()).replace(" ", "-")


def load_json(path: Path) -> list:
    # Return an empty list if the file doesn't exist yet
    if not path.exists():
        return []
        
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Handle the case where the file exists but is completely empty (0 bytes)
            return []


def save_json(path: Path, data: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> None:
    books = load_json(BOOKS_PATH)
    tropes = load_json(TROPES_PATH)

    existing_slugs = {t["slug"] for t in tropes}

    book_trope_names: set[str] = set()
    for book in books:
        for trope_name in book.get("tropes", []):
            book_trope_names.add(trope_name)

    added = 0
    for name in sorted(book_trope_names):
        slug = name_to_slug(name)
        if slug not in existing_slugs:
            tropes.append({
                "slug": slug,
                "name": name,
                "description": "",
                "featured": False,
                "canonical": False,
            })
            existing_slugs.add(slug)
            added += 1

    if added:
        save_json(TROPES_PATH, tropes)
        print(f"Added {added} new trope(s) to {TROPES_PATH}")
    else:
        print("All tropes already in sync.")


if __name__ == "__main__":
    main()
