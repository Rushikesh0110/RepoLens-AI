import argparse
from collections import Counter

from repolens.ast_extractor import extract_python_structure
from repolens.ingestion import scan_repository


def extract_repository_structure(scan_result):
    extracted_files = []
    extraction_errors = []

    for file_record in scan_result.files:

        if (
            not file_record.is_python
            or file_record.is_binary
            or file_record.skipped_reason is not None
        ):
            continue

        file_path = scan_result.root / file_record.path

        try:
            source_code = file_path.read_text(encoding="utf-8")

        except (OSError, UnicodeError) as error:
            extraction_errors.append(
                f"{file_record.path}: Could not read file: {error}"
            )
            continue

        extraction = extract_python_structure(source_code)

        if extraction.syntax_error:
            extraction_errors.append(
                f"{file_record.path}: {extraction.syntax_error}"
            )
            continue

        extracted_files.append((file_record.path, extraction))

    return extracted_files, extraction_errors

def main():
    parser = argparse.ArgumentParser(
        description="Scan a local repository using RepoLens AI."
    )

    parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Path to the repository (default: current directory)",
    )

    args = parser.parse_args()

    try:
        result = scan_repository(args.repository)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")

    extracted_files, extraction_errors = extract_repository_structure(
        result
    )
    extensions = Counter(
        file.extension or "(no extension)"
        for file in result.files
    )

    total_lines = sum(
        file.line_count or 0 for file in result.files
    )

    binary_files = sum(file.is_binary for file in result.files)

    print("\n========== RepoLens AI ==========")
    print(f"Repository: {result.root}")
    print(f"Total files: {result.total_files}")
    print(f"Python files: {result.python_files}")
    print(f"Total size: {result.total_size_bytes:,} bytes")
    print(f"Total lines: {total_lines:,}")
    print(f"Binary files: {binary_files}")

    print("\n----- File Types -----")
    for extension, count in extensions.most_common():
        print(f"{extension}: {count}")

        total_functions = sum(
        len(extraction.functions)
        for _, extraction in extracted_files
    )

    total_classes = sum(
        len(extraction.classes)
        for _, extraction in extracted_files
    )

    total_imports = sum(
        len(extraction.imports)
        for _, extraction in extracted_files
    )

    print("\n----- Code Structure -----")
    print(f"Python files analysed: {len(extracted_files)}")
    print(f"Functions: {total_functions}")
    print(f"Classes: {total_classes}")
    print(f"Imports: {total_imports}")

    for path, extraction in extracted_files:
        print(f"\nFile: {path}")

        for item in extraction.classes:
            print(f"  Class: {item.name}")

        for item in extraction.functions:
            name = (
                f"{item.parent_class}.{item.name}"
                if item.parent_class
                else item.name
            )
            kind = "Async function" if item.is_async else "Function"
            print(f"  {kind}: {name}")

        for item in extraction.imports:
            if item.imported_name is None:
                name = f"import {item.module}"
            else:
                module = "." * item.level + item.module
                name = f"from {module} import {item.imported_name}"

            if item.alias:
                name += f" as {item.alias}"

            print(f"  Import: {name}")

    if result.errors:
        print("\n----- Scan Errors -----")
        for error in result.errors:
            print(error)

    if extraction_errors:
        print("\n----- AST Extraction Errors -----")
        for error in extraction_errors:
            print(error)
            print("\n=================================\n")


if __name__ == "__main__":
    main()
