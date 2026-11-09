import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionInfo:
    name: str
    line_number: int
    end_line_number: int | None
    is_async: bool
    parent_class: str | None = None


@dataclass(frozen=True)
class ClassInfo:
    name: str
    line_number: int
    end_line_number: int | None


@dataclass(frozen=True)
class ImportInfo:
    module: str
    imported_name: str | None
    alias: str | None
    line_number: int
    level: int = 0


@dataclass
class ExtractionResult:
    functions: list[FunctionInfo]
    classes: list[ClassInfo]
    imports: list[ImportInfo]
    syntax_error: str | None = None

class StructureVisitor(ast.NodeVisitor):

    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []

        self.class_stack = []
        self.scope_stack = []


    def visit_FunctionDef(self, node):
        self._visit_function(node, is_async=False)

    def visit_AsyncFunctionDef(self, node):
        self._visit_function(node, is_async=True)

    def _visit_function(self, node, is_async):
        parent_class = None

        if self.scope_stack and self.scope_stack[-1] == "class":
            parent_class = self.class_stack[-1]

        self.functions.append(
            FunctionInfo(
                name=node.name,
                line_number=node.lineno,
                end_line_number=node.end_lineno,
                is_async=is_async,
                parent_class=parent_class,
            )
        )

        self.scope_stack.append("function")
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_ClassDef(self, node):
        self.classes.append(
            ClassInfo(
                name=node.name,
                line_number=node.lineno,
                end_line_number=node.end_lineno,
            )
        )

        self.class_stack.append(node.name)
        self.scope_stack.append("class")

        self.generic_visit(node)

        self.scope_stack.pop()
        self.class_stack.pop()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(
                ImportInfo(
                    module=alias.name,
                    imported_name=None,
                    alias=alias.asname,
                    line_number=node.lineno,
                )
            )

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.append(
                ImportInfo(
                    module=node.module or "",
                    imported_name=alias.name,
                    alias=alias.asname,
                    line_number=node.lineno,
                    level=node.level,
                )
            )
def extract_python_structure(source_code: str) -> ExtractionResult:

    try:
        tree = ast.parse(source_code)

    except SyntaxError as error:
        message = f"Line {error.lineno}: {error.msg}"

        return ExtractionResult(
            functions=[],
            classes=[],
            imports=[],
            syntax_error=message,
        )

    visitor = StructureVisitor()
    visitor.visit(tree)

    return ExtractionResult(
        functions=visitor.functions,
        classes=visitor.classes,
        imports=visitor.imports,
    )