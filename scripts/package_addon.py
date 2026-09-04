#!/usr/bin/env python3
"""Package Bedrock pack folders as .mcpack files nested in a .mcaddon archive."""

from __future__ import annotations

import argparse
import io
import json
import sys
import zipfile
from pathlib import Path


IGNORED_DIRS = {".git", ".venv", "__pycache__", "build", "dist", "node_modules", "temp"}
IGNORED_NAMES = {".DS_Store", ".env"}
IGNORED_SUFFIXES = {".map", ".ts", ".pem", ".key"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a distributable Bedrock .mcaddon archive.")
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    return parser.parse_args()


def manifest_is_pack(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    modules = data.get("modules", []) if isinstance(data, dict) else []
    return any(
        isinstance(module, dict)
        and module.get("type") in {"data", "resources", "script", "world_template"}
        for module in modules
    )


def should_ship(relative: Path) -> bool:
    if any(part in IGNORED_DIRS or part.startswith(".") for part in relative.parts):
        return False
    if relative.name in IGNORED_NAMES or relative.suffix.lower() in IGNORED_SUFFIXES:
        return False
    return True


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    return info


def build_mcpack(pack_root: Path) -> tuple[bytes, int]:
    stream = io.BytesIO()
    count = 0
    with zipfile.ZipFile(stream, "w") as archive:
        for path in sorted(pack_root.rglob("*")):
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(pack_root)
            if not should_ship(relative):
                continue
            archive.writestr(zip_info(relative.as_posix()), path.read_bytes())
            count += 1
    return stream.getvalue(), count


def main() -> int:
    args = parse_args()
    project = args.project.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not project.is_dir():
        print(f"error: project directory does not exist: {project}", file=sys.stderr)
        return 2
    if output.suffix.lower() != ".mcaddon":
        print("error: --output must end in .mcaddon", file=sys.stderr)
        return 2
    if output.exists() and not args.force:
        print(f"error: output exists; pass --force to replace it: {output}", file=sys.stderr)
        return 2

    manifests = sorted(
        path
        for path in project.rglob("manifest.json")
        if not any(part in IGNORED_DIRS for part in path.relative_to(project).parts)
        and manifest_is_pack(path)
    )
    pack_roots = [path.parent for path in manifests]
    if not pack_roots:
        print("error: no Bedrock behavior/resource pack manifests found", file=sys.stderr)
        return 1

    names: set[str] = set()
    packaged: list[tuple[str, bytes, int]] = []
    for pack_root in pack_roots:
        name = f"{pack_root.name}.mcpack"
        if name.casefold() in names:
            print(f"error: duplicate pack archive name: {name}", file=sys.stderr)
            return 1
        names.add(name.casefold())
        payload, count = build_mcpack(pack_root)
        if count == 0:
            print(f"error: pack has no shippable files: {pack_root}", file=sys.stderr)
            return 1
        packaged.append((name, payload, count))

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as addon:
        for name, payload, _ in packaged:
            addon.writestr(zip_info(name), payload)

    with zipfile.ZipFile(output) as addon:
        if addon.testzip() is not None:
            print("error: generated archive failed ZIP integrity check", file=sys.stderr)
            return 1

    print(f"Created {output} ({output.stat().st_size} bytes)")
    for name, _, count in packaged:
        print(f"  {name}: {count} files")
    print("Next: import this artifact into a clean Bedrock installation and run the smoke test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
