
from repolens.ingestion import scan_repository


def test_scans_python_files(tmp_path):
    (tmp_path / "main.py").write_text("print('Hello')\n")
    (tmp_path / "README.md").write_text("# Project\n")

    result = scan_repository(tmp_path)

    assert result.total_files == 2
    assert result.python_files == 1
    assert result.total_size_bytes > 0


def test_counts_lines_correctly(tmp_path):
    (tmp_path / "main.py").write_text("first\nsecond\nthird")

    result = scan_repository(tmp_path)

    assert result.files[0].line_count == 3


def test_ignores_excluded_directories(tmp_path):
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "ignored.py").write_text("print('ignored')")

    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("git config")

    (tmp_path / "main.py").write_text("print('included')")

    result = scan_repository(tmp_path)

    assert result.total_files == 1
    assert result.python_files == 1


def test_ignores_secret_files(tmp_path):
    (tmp_path / ".env").write_text("SECRET=123")
    (tmp_path / ".env.production").write_text("SECRET=456")
    (tmp_path / "main.py").write_text("print('Hello')")

    result = scan_repository(tmp_path)

    assert result.total_files == 1


def test_detects_binary_files(tmp_path):
    (tmp_path / "image.bin").write_bytes(b"\x00\x01\x02")

    result = scan_repository(tmp_path)

    assert result.files[0].is_binary is True


def test_rejects_missing_repository(tmp_path):
    missing = tmp_path / "missing"

    try:
        scan_repository(missing)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
