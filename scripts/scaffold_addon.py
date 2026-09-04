#!/usr/bin/env python3
"""Create a minimal linked Minecraft Bedrock behavior/resource pack project."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from pathlib import Path


IDENTIFIER_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")


def dotted_version(value: str, flag: str) -> list[int]:
    parts = value.split(".")
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        raise argparse.ArgumentTypeError(f"{flag} must be MAJOR.MINOR.PATCH")
    return [int(part) for part in parts]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "bedrock_addon"


def new_uuid() -> str:
    return str(uuid.uuid4())


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a minimal Minecraft Bedrock behavior/resource pack pair."
    )
    parser.add_argument("name", help="Player-facing add-on name")
    parser.add_argument("--output", required=True, type=Path, help="New project directory")
    parser.add_argument("--namespace", help="Lowercase content namespace (defaults from name)")
    parser.add_argument(
        "--min-engine-version",
        required=True,
        metavar="X.Y.Z",
        help="Verified Bedrock minimum engine version",
    )
    parser.add_argument("--version", default="1.0.0", metavar="X.Y.Z", help="Pack version")
    parser.add_argument("--author", default="Add-on Studio", help="Manifest author metadata")
    parser.add_argument("--script", action="store_true", help="Add a JavaScript module")
    parser.add_argument(
        "--server-version",
        help="Verified stable @minecraft/server module version; required with --script",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    namespace = args.namespace or slugify(args.name)[:32]
    if not IDENTIFIER_RE.fullmatch(namespace):
        print(
            "error: --namespace must be 2-32 lowercase letters, numbers, or underscores "
            "and start with a letter",
            file=sys.stderr,
        )
        return 2
    if namespace == "minecraft":
        print("error: the reserved 'minecraft' namespace cannot identify custom content", file=sys.stderr)
        return 2
    if args.script and not args.server_version:
        print("error: --server-version is required with --script", file=sys.stderr)
        return 2
    if args.server_version and not args.script:
        print("error: --server-version is only valid with --script", file=sys.stderr)
        return 2

    try:
        min_engine = dotted_version(args.min_engine_version, "--min-engine-version")
        pack_version = dotted_version(args.version, "--version")
    except argparse.ArgumentTypeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    output = args.output.expanduser().resolve()
    if output.exists():
        print(f"error: refusing to overwrite existing path: {output}", file=sys.stderr)
        return 2

    bp = output / "behavior_pack"
    rp = output / "resource_pack"
    bp_header, bp_data, rp_header, rp_resources = (new_uuid() for _ in range(4))

    rp_manifest = {
        "format_version": 2,
        "header": {
            "name": f"{args.name} Resources",
            "description": f"Resource pack for {args.name}",
            "uuid": rp_header,
            "version": pack_version,
            "min_engine_version": min_engine,
        },
        "modules": [
            {
                "type": "resources",
                "uuid": rp_resources,
                "version": pack_version,
            }
        ],
        "metadata": {"authors": [args.author]},
    }

    modules: list[dict[str, object]] = [
        {"type": "data", "uuid": bp_data, "version": pack_version}
    ]
    dependencies: list[dict[str, object]] = [
        {"uuid": rp_header, "version": pack_version}
    ]
    if args.script:
        modules.append(
            {
                "type": "script",
                "language": "javascript",
                "uuid": new_uuid(),
                "version": pack_version,
                "entry": "scripts/main.js",
            }
        )
        dependencies.append(
            {"module_name": "@minecraft/server", "version": args.server_version}
        )

    bp_manifest = {
        "format_version": 2,
        "header": {
            "name": f"{args.name} Behavior",
            "description": f"Behavior pack for {args.name}",
            "uuid": bp_header,
            "version": pack_version,
            "min_engine_version": min_engine,
        },
        "modules": modules,
        "dependencies": dependencies,
        "metadata": {"authors": [args.author]},
    }

    output.mkdir(parents=True)
    write_json(bp / "manifest.json", bp_manifest)
    write_json(rp / "manifest.json", rp_manifest)
    write_json(bp / "texts" / "languages.json", ["en_US"])
    write_json(rp / "texts" / "languages.json", ["en_US"])
    (bp / "texts" / "en_US.lang").write_text(
        f"pack.name={args.name} Behavior\npack.description=Behavior pack for {args.name}\n",
        encoding="utf-8",
    )
    (rp / "texts" / "en_US.lang").write_text(
        f"pack.name={args.name} Resources\npack.description=Resource pack for {args.name}\n",
        encoding="utf-8",
    )
    (output / ".gitignore").write_text(
        ".DS_Store\n.env\nnode_modules/\nbuild/\ndist/\ntemp/\n*.mcaddon\n*.mcpack\n",
        encoding="utf-8",
    )

    if args.script:
        script = (
            'import { system } from "@minecraft/server";\n\n'
            "system.run(() => {\n"
            f'  console.warn("[{namespace}] script initialized");\n'
            "});\n"
        )
        script_path = bp / "scripts" / "main.js"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(script, encoding="utf-8")

    print(f"Created Bedrock add-on scaffold: {output}")
    print(f"Namespace: {namespace}")
    print(f"Behavior pack header UUID: {bp_header}")
    print(f"Resource pack header UUID: {rp_header}")
    print("Next: add a vertical slice, validate it, then test it in a fresh Bedrock world.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
