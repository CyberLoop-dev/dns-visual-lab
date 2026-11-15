#!/usr/bin/env python3
"""Summarize common resource-record lines from a local zone text file."""

import argparse
from collections import Counter
from pathlib import Path

SUPPORTED = {"A", "AAAA", "CNAME", "MX", "TXT", "NS", "PTR"}


def parse_records(text: str) -> list[tuple[str, str, str]]:
    records = []
    for raw in text.splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or line.startswith("$"):
            continue
        fields = line.split()
        if len(fields) < 4:
            continue
        record_type = fields[-2].upper()
        if record_type in SUPPORTED:
            records.append((fields[0], record_type, " ".join(fields[-1:])))
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zone_file", type=Path)
    args = parser.parse_args()
    records = parse_records(args.zone_file.read_text(encoding="utf-8"))
    counts = Counter(kind for _, kind, _ in records)
    print(f"Parsed {len(records)} supported records")
    for kind, count in sorted(counts.items()):
        print(f"{kind:>6}: {count}")
    for name, kind, value in records:
        print(f"{name:<28} {kind:<6} {value}")


if __name__ == "__main__":
    main()
