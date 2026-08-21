#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

PROFILES = ("application", "library", "infrastructure")
DISPLAY_NAMES = {
    "application": "Example Application",
    "library": "Example Library",
    "infrastructure": "Example Infrastructure Repository",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create repository boilerplate from a golden reference profile."
    )
    parser.add_argument("profile", choices=PROFILES)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--repository-name", default="New Repository")
    return parser.parse_args()


def render(profile: str, destination: Path, repository_name: str) -> None:
    root = Path(__file__).resolve().parents[1]
    source = root / "reference" / profile

    if not source.is_dir():
        raise FileNotFoundError(f"Missing reference profile: {source}")
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"Destination is not empty: {destination}")

    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, dirs_exist_ok=True)

    readme = destination / "README.md"
    content = readme.read_text(encoding="utf-8")
    content = content.replace(DISPLAY_NAMES[profile], repository_name)
    readme.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    render(args.profile, args.destination, args.repository_name)


if __name__ == "__main__":
    main()
