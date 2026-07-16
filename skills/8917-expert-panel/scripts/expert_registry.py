#!/usr/bin/env python3
"""Discover host-native expert cards without assuming they are invocable."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_ROOTS = {
    "claude-code": Path.home() / ".claude" / "agents",
    "codex": Path.home() / ".codex" / "agents",
}


@dataclass(frozen=True)
class ExpertCard:
    canonical_id: str
    native_id: str
    display_name: str
    description: str
    host: str
    card_path: str
    sha256: str
    instructions: str

    def payload(self, include_instructions: bool = False) -> dict[str, str]:
        data = asdict(self)
        if not include_instructions:
            data.pop("instructions")
        return data


def canonical_id(name: str) -> str:
    normalized = unicodedata.normalize("NFKC", name).casefold()
    value = re.sub(r"[\W_]+", "-", normalized, flags=re.UNICODE).strip("-")
    if not value:
        raise ValueError("expert card name cannot produce a canonical id")
    return value


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_claude_card(path: Path) -> ExpertCard:
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")

    metadata: dict[str, str] = {}
    lines = match.group(1).splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        key, separator, value = line.partition(":")
        if separator and key.strip() in {"name", "description"}:
            field = key.strip()
            scalar = value.strip()
            if scalar.startswith(("|", ">")):
                parent_indent = len(line) - len(line.lstrip(" "))
                block_lines: list[str] = []
                block_indent: int | None = None
                index += 1
                while index < len(lines):
                    block_line = lines[index]
                    indent = len(block_line) - len(block_line.lstrip(" "))
                    if block_line.strip() and indent <= parent_indent:
                        break
                    if block_line.strip():
                        if block_indent is None:
                            block_indent = indent
                        block_lines.append(block_line[block_indent:])
                    else:
                        block_lines.append("")
                    index += 1
                if scalar.startswith(">"):
                    metadata[field] = " ".join(
                        part.strip() for part in block_lines
                    ).strip()
                else:
                    metadata[field] = "\n".join(block_lines).strip()
                continue
            metadata[field] = parse_scalar(value)
        index += 1

    name = metadata.get("name", "").strip()
    if not name:
        raise ValueError("missing name")

    return ExpertCard(
        canonical_id=canonical_id(name),
        native_id=path.stem,
        display_name=name,
        description=metadata.get("description", "").strip(),
        host="claude-code",
        card_path=str(path.resolve()),
        sha256=file_hash(path),
        instructions=match.group(2).strip(),
    )


def parse_codex_card(path: Path) -> ExpertCard:
    with path.open("rb") as handle:
        metadata = tomllib.load(handle)

    name = str(metadata.get("name", "")).strip()
    if not name:
        raise ValueError("missing name")

    return ExpertCard(
        canonical_id=canonical_id(name),
        native_id=path.stem,
        display_name=name,
        description=str(metadata.get("description", "")).strip(),
        host="codex",
        card_path=str(path.resolve()),
        sha256=file_hash(path),
        instructions=str(metadata.get("developer_instructions", "")).strip(),
    )


def discover(host: str, root: Path) -> tuple[list[ExpertCard], list[dict[str, str]]]:
    parser = parse_codex_card if host == "codex" else parse_claude_card
    pattern = "*.toml" if host == "codex" else "*.md"
    cards: list[ExpertCard] = []
    invalid: list[dict[str, str]] = []

    if not root.is_dir():
        return cards, invalid

    for path in sorted(root.glob(pattern)):
        try:
            cards.append(parser(path))
        except (OSError, UnicodeError, ValueError, tomllib.TOMLDecodeError) as error:
            invalid.append({"card_path": str(path.resolve()), "error": str(error)})
    return cards, invalid


def matches_query(card: ExpertCard, query: str) -> bool:
    terms = [term for term in query.casefold().split() if term]
    haystack = " ".join(
        (card.display_name, card.description, card.native_id, card.canonical_id)
    ).casefold()
    return all(term in haystack for term in terms)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover Claude Code or Codex native expert cards."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("list", "resolve"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument(
            "--host", choices=("claude-code", "codex"), required=True
        )
        subparser.add_argument("--root", type=Path)
        subparser.add_argument("--include-instructions", action="store_true")

    list_parser = subparsers.choices["list"]
    list_parser.add_argument("--query", default="")
    list_parser.add_argument("--limit", type=int, default=30)

    resolve_parser = subparsers.choices["resolve"]
    resolve_parser.add_argument("--name", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = (args.root or DEFAULT_ROOTS[args.host]).expanduser().resolve()
    cards, invalid = discover(args.host, root)

    if args.command == "list":
        filtered = [card for card in cards if matches_query(card, args.query)]
        limit = max(args.limit, 0)
        payload = {
            "host": args.host,
            "root": str(root),
            "count": len(filtered),
            "returned": min(len(filtered), limit),
            "invalid": invalid,
            "experts": [
                card.payload(args.include_instructions) for card in filtered[:limit]
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    wanted = args.name.casefold().strip()
    matches = [
        card
        for card in cards
        if wanted
        in {
            card.display_name.casefold(),
            card.canonical_id,
            card.native_id.casefold(),
        }
    ]
    if len(matches) != 1:
        print(
            json.dumps(
                {
                    "error": "expert_not_unique",
                    "query": args.name,
                    "matches": [card.payload(False) for card in matches],
                    "invalid": invalid,
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 2

    print(
        json.dumps(
            matches[0].payload(args.include_instructions),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
