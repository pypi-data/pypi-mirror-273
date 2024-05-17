"""A linter to scrutinize how you are using mocks in Python."""

__version__ = "1.1.3"

# pyright: strict

import ast
import functools
import logging
import pathlib
import sys
import typing
from collections.abc import Callable, Iterator

# Excludes taken from ruff.
EXCLUDE = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
]


def walk_path(path: pathlib.Path) -> Iterator[pathlib.Path]:
    """
    Find all files in a directory recursively.

    Only Python 3.12 includes pathlib.Path.walk.
    """
    if path.is_dir() and path.name not in EXCLUDE:
        for item in path.iterdir():
            yield from walk_path(item)
    else:
        yield path


class MockImportVisitor(ast.NodeVisitor):
    """
    Find all patch calls in a module.

    After calling visit on a module, find the patch calls in the patches attribute.
    """

    def __init__(self):
        self.patches: list[ast.Call] = []

    def visit_Call(self, node: ast.Call):
        """
        Add any call of a function or method named patch to the list.

        It's a wide net, but hopefully other functions called patch won't have a string
        as the first argument so will be skipped. Can revise later if this needs to be
        smarter.
        """
        if isinstance(node.func, ast.Name) and node.func.id == "patch":
            self.patches.append(node)
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "patch":
            self.patches.append(node)


RULE_MESSAGES = {
    "PM101": "patched implementation",
    "PM102": "patched is not a top level module attribute",
    "PM103": "patched builtins instead of module under test",
}


@functools.lru_cache
def find_importable(name: str, sys_path: tuple[str]) -> tuple[str, str]:
    """
    Split the full name of a Python object into importable file and remaining parts.

    The sys_path is a tuple of directories to search for the importable file, basically
    sys.path, but you have to pass it in to make testing easier. It must be a tuple
    instead of a list so the args work with lru_cache.

    For example the address for the method "wot" of the class "Hey" in the module "yo"
    would be "yo.Hey.wot". If "." is in sys_path and "yo.py" is in the working
    directory, then the return value is ("./yo.py", "Hey.wot").

    We use this function instead of importlib.util.find_spec because find_spec will
    import parent packages when finding an import, and we don't want to import anything.
    This means the logic is not identical to Python's import system becuase it doesn't
    take into account the __path__ attribute on packages.

    The file given could be an __init__.py file in a package, if that is what is found.
    It's also possible for the file to be a directory if the import is also a package /
    directory. You should always check if the file is a directory before handling it
    e.g. you can't ast.parse a directory.
    """
    first, rest = name.split(".", 1)
    if not rest:
        raise ValueError(
            "must be at least two parts in name, one to import and one to patch"
        )
    for path in sys_path:
        path = pathlib.Path(path)
        package_dir = path / first
        if package_dir.is_dir():
            break
        module_file = package_dir.with_suffix(".py")
        if module_file.exists():
            return (str(module_file), rest)
    else:  # no break
        raise LookupError(f"import {name} not found")
    parts = rest.split(".")
    for i, part in enumerate(parts):
        next_dir = package_dir / part
        if not next_dir.is_dir():
            break
        package_dir = next_dir
    else:  # no break
        # It's a bit weird but you can still patch package on its parent package.
        return (str(package_dir.parent), package_dir.name)
    module_file = next_dir.with_suffix(".py")
    if module_file.exists():
        return (str(module_file), ".".join(parts[i + 1 :]))
    init_file = package_dir / "__init__.py"
    if init_file.exists():
        return (str(init_file), ".".join(parts[i:]))
    raise LookupError(f"import {name} not found")


P = typing.ParamSpec("P")
T = typing.TypeVar("T")


def listify(f: Callable[P, Iterator[T]]) -> Callable[P, list[T]]:
    """
    Convert a generator function to one that returns a list.

    This is important when combined with lru_cache, as we don't want to cache a
    reference to the same generator that has already been consumed.
    """

    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        return list(f(*args, **kwargs))

    return wrapper


@functools.lru_cache
@listify
def find_module_definitions(source: str) -> Iterator[str]:
    """
    Find the names of objects defined in a module, not imported.

    This is done without importing the module itself.

    I'm sure it is possible to trick this function by messing around with globals() and
    things like that, but it will pick up top level classes, functions, and assigments.
    """
    module = ast.parse(source)
    for statement in module.body:
        if isinstance(statement, (ast.FunctionDef, ast.ClassDef)):
            yield statement.name
        elif isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Name):
                    yield target.id


@functools.lru_cache
@listify
def find_package_definitions(package_path: str):
    """
    Find the names of other modules and packages defined in a package.

    You need to give the path to the package directory on disk, not an import path with
    dots.

    This is done by listing the directory, not following the Python import system
    exactly, for example any __path__ attributes will not be respected.
    """
    path = pathlib.Path(package_path)
    for item in path.iterdir():
        if item.is_file() and item.suffix == ".py" and item.name != "__init__.py":
            yield item.stem
        elif item.is_dir() and item.name != "__pycache__":
            yield item.name


def find_errors(
    patches: list[ast.Call], file: str
) -> Iterator[tuple[str, int, int, str]]:
    """
    Decide whether each patch call has errors or not.

    The return value is a tuple that matches the input args for format_message.

    It is assumed that all the patches are in the same file.

    This function won't import any modules, but it will search the file system and
    ast.parse files to decide whether the right thing was patched or not.

    file is just used for logging.
    """
    tuple_sys_path = tuple(sys.path)
    logger = logging.getLogger(__name__)
    for node in patches:
        args = node.args
        if len(args) == 0:
            logger.debug(
                "%s:%s:%s: patch call with no args", file, node.lineno, node.col_offset
            )
            continue
        first_arg = args[0]
        if not isinstance(first_arg, ast.Constant):
            logger.debug(
                "%s:%s:%s: patch arg not a constant", file, node.lineno, node.col_offset
            )
            continue
        name = first_arg.value
        if not isinstance(name, str):
            logger.debug(
                "%s:%s:%s: patch arg not a str (%s)",
                file,
                node.lineno,
                node.col_offset,
                repr(name),
            )
            continue
        if "." not in name:
            logger.debug(
                "%s:%s:%s: patch arg not an import name (%s)",
                file,
                node.lineno,
                node.col_offset,
                repr(name),
            )
            continue
        if name.split(".", 1)[0] == "builtins":
            yield ("PM103", node.lineno, node.col_offset, name)
            # builtins isn't a normal module found in path, so even though it could be
            # possible for there to be more errors on the same line, we don't check for
            # them because it would need special handling.
            continue
        try:
            source_path, remaining = find_importable(name, tuple_sys_path)
        except (LookupError, ValueError):
            logger.debug(
                "%s:%s:%s: could not find %s in sys.path",
                file,
                node.lineno,
                node.col_offset,
                name,
            )
            continue
        if "." in remaining:
            yield ("PM102", node.lineno, node.col_offset, name)
        source_path = pathlib.Path(source_path)
        if source_path.is_dir():
            definitions = find_package_definitions(str(source_path))
        else:
            definitions = find_module_definitions(source_path.read_text())
        if remaining.split(".", 1)[0] in definitions:
            yield ("PM101", node.lineno, node.col_offset, name)


def format_message(path: str, lineno: int, col_offset: int, rule_code: str, arg: str):
    """
    Format the args into a rules error message.

    The input args match the tuple output from find_errors.

    This format follows a loose common standard giving the file name, starting position,
    and error code. For example vim's "make" command can populate the quickfix list from
    this output.
    """
    return f"{path}:{lineno}:{col_offset}: {rule_code} {RULE_MESSAGES[rule_code]} {arg}"


def main(argv: list[str]):
    """
    Find files, parse them, and print output.

    This should be used from an if __name__ == "__main__" block and passed sys.argv.
    """
    if len(argv) > 1 and argv[1] != ".":
        start_dir = argv[1]
    else:
        start_dir = "."
    for file in walk_path(pathlib.Path(start_dir)):
        try:
            source = file.read_text()
        except Exception:
            continue
        if "patch(" not in source:
            continue
        visitor = MockImportVisitor()
        try:
            parsed_module = ast.parse(source)
        except SyntaxError:
            continue
        visitor = MockImportVisitor()
        visitor.visit(parsed_module)
        errors = find_errors(visitor.patches, str(file))
        for rule_code, lineno, col_offset, arg in errors:
            print(format_message(str(file), lineno, col_offset, rule_code, arg))


if __name__ == "__main__":
    main(sys.argv)
