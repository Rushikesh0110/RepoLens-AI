import argparse
from collections import Counter

from repolens.ingestion import scan_repository


def main():
    parser = argparse.ArgumentParser(
        description="Scan a local repository using RepoLens AI."
    )

    parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Path to the repository",
    )

    args = parser.parse_args()

    try:
        result = scan_repository(args.repository)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")

    extensions = Counter(
        file.extension or "(no extension)"
        for file in result.files
    )

    total_lines = sum(
        file.line_count or 0 for file in result.files
    )

    print("\n========== RepoLens AI ==========")
    print(f"Repository: {result.root}")
    print(f"Total files: {result.total_files}")
    print(f"Python files: {result.python_files}")
    print(f"Total size: {result.total_size_bytes:,} bytes")
    print(f"Total lines: {total_lines:,}")

    print("\n----- File Types -----")
    for extension, count in extensions.most_common():
        print(f"{extension}: {count}")

    if result.errors:
        print("\n----- Scan Errors -----")
        for error in result.errors:
            print(error)

    print("=================================")


if __name__ == "__main__":
    main()
