"""Command-line interface for tracked-ignored."""

import argparse
import json
import sys

from .core import run


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="tracked-ignored",
        description="Find git-tracked files that should be ignored.",
    )
    parser.add_argument("path", nargs="?", default=".", help="repository path")
    parser.add_argument("--json", action="store_true", help="output JSON")
    args = parser.parse_args(argv)

    result = run(args.path)
    problems = (
        result["ignored_tracked"]
        + result["dangerous"]
        + result["artifacts"]
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Scanned {result['total_tracked']} tracked files in {result['root']}")
        if result["ignored_tracked"]:
            print("\nIgnored but tracked:")
            for f in result["ignored_tracked"]:
                print(f"  {f}")
        if result["dangerous"]:
            print("\nPossibly sensitive:")
            for f in result["dangerous"]:
                print(f"  {f}")
        if result["artifacts"]:
            print("\nBuild/dependency artifacts:")
            for f in result["artifacts"]:
                print(f"  {f}")
        if not problems:
            print("\nNo problems found.")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
