#!/usr/bin/env python3
"""Run dependency-free structural checks on a Minecraft Bedrock add-on project."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


IGNORED_DIRS = {".git", ".venv", "__pycache__", "build", "dist", "node_modules", "temp"}
FORBIDDEN_NAMES = {".env", ".DS_Store"}
FORBIDDEN_SUFFIXES = {".map", ".pem", ".key", ".ts"}
IDENTIFIER_RE = re.compile(r"^[a-z][a-z0-9_]{0,31}:[a-z0-9_./-]+$")
PACK_TYPES = {"data", "resources", "script", "world_template"}


@dataclass
class Results:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Bedrock add-on structure and links.")
    parser.add_argument("project", type=Path)
    parser.add_argument(
        "--allow-preview",
        action="store_true",
        help="Allow preview manifest formats; still requires official Preview validation",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    return parser.parse_args()


def ignored(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def load_json(path: Path, results: Results) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        results.error(f"{path}: invalid JSON ({exc})")
        return None


def valid_uuid(value: object) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError, AttributeError):
        return False


def valid_triplet(value: object) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 3
        and all(isinstance(part, int) and not isinstance(part, bool) and part >= 0 for part in value)
    )


def manifest_kind(data: dict[str, Any]) -> set[str]:
    kinds: set[str] = set()
    for module in data.get("modules", []):
        if isinstance(module, dict) and module.get("type") in PACK_TYPES:
            kinds.add(module["type"])
    return kinds


def validate_manifest(
    path: Path,
    data: Any,
    results: Results,
    all_uuids: dict[str, Path],
    allow_preview: bool,
) -> dict[str, Any] | None:
    if not isinstance(data, dict):
        results.error(f"{path}: manifest root must be an object")
        return None

    format_version = data.get("format_version")
    if format_version != 2:
        if allow_preview and format_version == 3:
            results.warn(f"{path}: manifest format 3 requires Preview-specific validation")
        else:
            results.error(f"{path}: stable behavior/resource packs require manifest format_version 2")

    header = data.get("header")
    if not isinstance(header, dict):
        results.error(f"{path}: missing object header")
        return data
    for key in ("name", "description"):
        if not isinstance(header.get(key), str) or not header[key].strip():
            results.error(f"{path}: header.{key} must be a non-empty string")

    header_uuid = header.get("uuid")
    if not valid_uuid(header_uuid):
        results.error(f"{path}: header.uuid is missing or invalid")
    else:
        normalized = str(uuid.UUID(str(header_uuid)))
        if normalized in all_uuids:
            results.error(f"{path}: UUID duplicates {all_uuids[normalized]}")
        else:
            all_uuids[normalized] = path

    if format_version == 2:
        if not valid_triplet(header.get("version")):
            results.error(f"{path}: header.version must be a three-integer array")
        if not valid_triplet(header.get("min_engine_version")):
            results.error(f"{path}: header.min_engine_version must be a three-integer array")

    modules = data.get("modules")
    if not isinstance(modules, list) or not modules:
        results.error(f"{path}: modules must be a non-empty array")
        return data
    for index, module in enumerate(modules):
        where = f"{path}: modules[{index}]"
        if not isinstance(module, dict):
            results.error(f"{where} must be an object")
            continue
        if module.get("type") not in PACK_TYPES:
            results.error(f"{where}.type is unsupported or missing")
        module_uuid = module.get("uuid")
        if not valid_uuid(module_uuid):
            results.error(f"{where}.uuid is missing or invalid")
        else:
            normalized = str(uuid.UUID(str(module_uuid)))
            if normalized in all_uuids:
                results.error(f"{where}.uuid duplicates {all_uuids[normalized]}")
            else:
                all_uuids[normalized] = path
        if format_version == 2 and not valid_triplet(module.get("version")):
            results.error(f"{where}.version must be a three-integer array")
        if module.get("type") == "script":
            entry = module.get("entry")
            if not isinstance(entry, str) or not entry:
                results.error(f"{where}: script module needs an entry path")
            elif not (path.parent / entry).is_file():
                results.error(f"{where}: script entry does not exist: {entry}")
            if module.get("language") != "javascript":
                results.error(f"{where}: script language must be 'javascript'")
    return data


def walk_identifiers(path: Path, data: Any, seen: dict[str, Path], results: Results) -> None:
    if not isinstance(data, dict):
        return
    for root_key, body in data.items():
        if not isinstance(root_key, str) or not root_key.startswith("minecraft:") or not isinstance(body, dict):
            continue
        description = body.get("description")
        if not isinstance(description, dict) or "identifier" not in description:
            continue
        identifier = description.get("identifier")
        if not isinstance(identifier, str) or not IDENTIFIER_RE.fullmatch(identifier):
            results.error(f"{path}: invalid or non-lowercase identifier {identifier!r}")
            continue
        if identifier.startswith("minecraft:"):
            results.warn(f"{path}: modifies the reserved minecraft namespace: {identifier}")
        if identifier in seen and seen[identifier] != path:
            results.error(f"{path}: identifier {identifier} duplicates {seen[identifier]}")
        else:
            seen[identifier] = path


def main() -> int:
    args = parse_args()
    root = args.project.expanduser().resolve()
    results = Results()
    if not root.is_dir():
        print(f"error: project directory does not exist: {root}", file=sys.stderr)
        return 2

    json_files = sorted(path for path in root.rglob("*.json") if not ignored(path.relative_to(root)))
    parsed: dict[Path, Any] = {}
    for path in json_files:
        parsed[path] = load_json(path, results)

    manifest_paths = sorted(path for path in json_files if path.name == "manifest.json")
    manifests: dict[Path, dict[str, Any]] = {}
    all_uuids: dict[str, Path] = {}
    for path in manifest_paths:
        data = validate_manifest(path, parsed[path], results, all_uuids, args.allow_preview)
        if data is not None and manifest_kind(data):
            manifests[path] = data
    if not manifests:
        results.error(f"{root}: no Bedrock pack manifest found")

    headers: dict[str, tuple[Path, object]] = {}
    for path, data in manifests.items():
        header = data.get("header", {})
        if valid_uuid(header.get("uuid")):
            headers[str(uuid.UUID(str(header["uuid"])))] = (path, header.get("version"))

    resource_headers = {
        str(uuid.UUID(str(data["header"]["uuid"])))
        for data in manifests.values()
        if "resources" in manifest_kind(data)
        and isinstance(data.get("header"), dict)
        and valid_uuid(data["header"].get("uuid"))
    }
    behavior_manifests: list[tuple[Path, dict[str, Any]]] = []
    for path, data in manifests.items():
        kinds = manifest_kind(data)
        if kinds & {"data", "script"}:
            behavior_manifests.append((path, data))
        script_modules = [m for m in data.get("modules", []) if isinstance(m, dict) and m.get("type") == "script"]
        dependencies = data.get("dependencies", [])
        if dependencies is not None and not isinstance(dependencies, list):
            results.error(f"{path}: dependencies must be an array")
            dependencies = []
        server_dependency = False
        for index, dependency in enumerate(dependencies or []):
            if not isinstance(dependency, dict):
                results.error(f"{path}: dependencies[{index}] must be an object")
                continue
            if dependency.get("module_name") == "@minecraft/server":
                server_dependency = True
                module_version = dependency.get("version")
                if not isinstance(module_version, str) and not valid_triplet(module_version):
                    results.error(
                        f"{path}: @minecraft/server dependency version must be a semver string "
                        "or three-integer array supported by the target manifest schema"
                    )
            if "uuid" in dependency:
                if not valid_uuid(dependency["uuid"]):
                    results.error(f"{path}: dependencies[{index}].uuid is invalid")
                    continue
                dependency_uuid = str(uuid.UUID(str(dependency["uuid"])))
                if dependency_uuid not in headers:
                    results.warn(f"{path}: pack dependency is not present in this project: {dependency_uuid}")
                elif dependency.get("version") != headers[dependency_uuid][1]:
                    results.error(
                        f"{path}: dependency version {dependency.get('version')} does not match "
                        f"{headers[dependency_uuid][0]} version {headers[dependency_uuid][1]}"
                    )
        if script_modules and not server_dependency:
            results.error(f"{path}: script module has no @minecraft/server dependency")

    if resource_headers:
        for path, data in behavior_manifests:
            linked = {
                str(uuid.UUID(str(dep["uuid"])))
                for dep in data.get("dependencies", [])
                if isinstance(dep, dict) and valid_uuid(dep.get("uuid"))
            }
            if not linked.intersection(resource_headers):
                results.warn(f"{path}: behavior pack does not depend on a resource pack in this project")

    identifiers: dict[str, Path] = {}
    for path, data in parsed.items():
        if data is not None and path.name != "manifest.json":
            walk_identifiers(path, data, identifiers, results)

    pack_roots = {path.parent for path in manifests}
    shipped_files: set[Path] = set()
    for pack_root in pack_roots:
        if not (pack_root / "pack_icon.png").is_file():
            results.warn(f"{pack_root}: pack_icon.png is missing")
        for path in pack_root.rglob("*"):
            if not path.is_file() or ignored(path.relative_to(root)):
                continue
            shipped_files.add(path)
            if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
                results.warn(f"{path}: development or sensitive file should not ship")

    total_bytes = sum(path.stat().st_size for path in shipped_files)
    if len(shipped_files) > 3500:
        results.warn(f"project has {len(shipped_files)} shipped files; cooperative target is at most 3500")
    if total_bytes > 25 * 1024 * 1024:
        results.warn(f"project is {total_bytes / 1024 / 1024:.1f} MiB uncompressed; investigate above 25 MiB")

    for message in results.errors:
        print(f"ERROR: {message}")
    for message in results.warnings:
        print(f"WARN: {message}")
    print(
        f"Checked {len(json_files)} JSON files, {len(manifests)} packs, "
        f"{len(identifiers)} content identifiers, and {len(shipped_files)} shipped files."
    )
    print(f"Result: {len(results.errors)} error(s), {len(results.warnings)} warning(s).")
    if results.errors or (args.strict and results.warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
