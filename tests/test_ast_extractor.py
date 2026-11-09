from repolens.ast_extractor import extract_python_structure


def test_extracts_functions_and_methods():
    source_code = """
def greet():
    return "Hello"

async def fetch_data():
    return None

class Student:
    def study(self):
        pass
"""

    result = extract_python_structure(source_code)

    assert len(result.functions) == 3

    assert result.functions[0].name == "greet"
    assert result.functions[0].is_async is False
    assert result.functions[0].parent_class is None

    assert result.functions[1].name == "fetch_data"
    assert result.functions[1].is_async is True

    assert result.functions[2].name == "study"
    assert result.functions[2].parent_class == "Student"

    assert len(result.classes) == 1
    assert result.classes[0].name == "Student"


def test_extracts_imports():
    source_code = """
import pandas as pd
import os
from pathlib import Path
from .utils import helper as helper_alias
"""

    result = extract_python_structure(source_code)

    assert len(result.imports) == 4

    assert result.imports[0].module == "pandas"
    assert result.imports[0].alias == "pd"

    assert result.imports[1].module == "os"
    assert result.imports[1].alias is None

    assert result.imports[2].module == "pathlib"
    assert result.imports[2].imported_name == "Path"

    assert result.imports[3].module == "utils"
    assert result.imports[3].imported_name == "helper"
    assert result.imports[3].alias == "helper_alias"
    assert result.imports[3].level == 1


def test_extracts_multiple_imports():
    source_code = """
import os, sys
from pathlib import Path, PurePath
"""

    result = extract_python_structure(source_code)

    assert len(result.imports) == 4

    assert result.imports[0].module == "os"
    assert result.imports[1].module == "sys"

    assert result.imports[2].imported_name == "Path"
    assert result.imports[3].imported_name == "PurePath"


def test_extracts_nested_functions():
    source_code = """
def outer():
    def inner():
        pass

class Example:
    def method(self):
        def nested():
            pass
"""

    result = extract_python_structure(source_code)

    assert len(result.functions) == 4

    assert result.functions[0].name == "outer"
    assert result.functions[0].parent_class is None

    assert result.functions[1].name == "inner"
    assert result.functions[1].parent_class is None

    assert result.functions[2].name == "method"
    assert result.functions[2].parent_class == "Example"

    assert result.functions[3].name == "nested"
    assert result.functions[3].parent_class is None


def test_handles_invalid_python_syntax():
    source_code = """
def greet(:
    print("Hello")
"""

    result = extract_python_structure(source_code)

    assert result.syntax_error is not None
    assert "Line" in result.syntax_error

    assert result.functions == []
    assert result.classes == []
    assert result.imports == []


def test_handles_empty_source_code():
    result = extract_python_structure("")

    assert result.syntax_error is None
    assert result.functions == []
    assert result.classes == []
    assert result.imports == []