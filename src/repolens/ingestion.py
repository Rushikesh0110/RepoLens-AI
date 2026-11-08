
import os
from dataclasses import dataclass
from pathlib import Path

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
}

IGNORED_FILES = {
    ".DS_Store",
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
}

MAX_FILE_SIZE = 1_000_000


@dataclass(frozen=True)
class FileRecord:
    path: str
    extension: str
    size_bytes: int
    line_count: int | None
    is_python: bool
    is_binary: bool
    skipped_reason: str | None = None


@dataclass
class ScanResult:
    root: Path
    files: list[FileRecord]
    errors: list[str]

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_size_bytes(self) -> int:
        return sum(file.size_bytes for file in self.files)

    @property
    def python_files(self) -> int:
        return sum(file.is_python for file in self.files)


def inspect_file(path: Path, relative_path: str,
                 max_file_size: int) -> tuple[FileRecord | None, str | None]:

    try:
        size = path.stat().st_size
        extension = path.suffix.lower()

        if size > max_file_size:
            return (
                FileRecord(
                    relative_path, extension, size, None,
                    extension == ".py", False, "File exceeds size limit"
                ),
                None,
            )

        with path.open("rb") as file:
            content = file.read()

        if b"\0" in content[:8192]:
            return (
                FileRecord(
                    relative_path, extension, size, None,
                    extension == ".py", True, "Binary file"
                ),
                None,
            )
        line_count = content.count(b"\n")

        if content and not content.endswith(b"\n"):
            line_count += 1

        return (
            FileRecord(
                relative_path, extension, size, line_count,
                extension == ".py", False
            ),
            None,
        )

    except OSError as error:
        return None, f"{relative_path}: {error}"


def scan_repository(
    root: str | Path,
    max_file_size: int = MAX_FILE_SIZE,
) -> ScanResult:

    root = Path(root).expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(f"Repository does not exist: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    if max_file_size <= 0:
        raise ValueError("max_file_size must be positive")

    records = []
    errors = []

    for current_root, directories, filenames in os.walk(
        root, topdown=True, followlinks=False
    ):
        current_path = Path(current_root)

        directories[:] = sorted(
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
            and not (current_path / directory).is_symlink()
        )

        for filename in sorted(filenames):
            if filename in IGNORED_FILES:
                continue

            if filename.startswith(".env."):
                continue

            file_path = current_path / filename

            if file_path.is_symlink() or not file_path.is_file():
                continue

            relative_path = file_path.relative_to(root).as_posix()

            record, error = inspect_file(
                file_path, relative_path, max_file_size
            )

            if record is not None:
                records.append(record)

            if error is not None:
                errors.append(error)

    records.sort(key=lambda record: record.path)

    return ScanResult(
        root=root,
        files=records,
        errors=errors,
    )
