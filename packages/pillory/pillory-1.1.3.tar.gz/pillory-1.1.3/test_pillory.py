import ast
import unittest
from inspect import cleandoc

import pillory


class PilloryTestCase(unittest.TestCase):
    def test_visitor_patches(self):
        visitor = pillory.MockImportVisitor()
        visitor.visit(ast.parse("""patch("builtins.print")"""))
        self.assertEqual(
            [ast.dump(patch) for patch in visitor.patches],
            [
                ast.dump(
                    ast.Call(
                        func=ast.Name(id="patch", ctx=ast.Load()),
                        args=[ast.Constant(value="builtins.print")],
                        lineno=1,
                        col_offset=0,
                        keywords=[],
                    )
                )
            ],
        )

    def test_find_errors(self):
        self.assertEqual(
            list(
                pillory.find_errors(
                    [
                        ast.Call(
                            func=ast.Name(id="patch", ctx=ast.Load()),
                            args=[ast.Constant(value="builtins.open")],
                            lineno=1,
                            col_offset=0,
                        )
                    ],
                    "hey.py",
                )
            ),
            [("PM103", 1, 0, "builtins.open")],
        )

    def test_find_importable(self):
        self.assertEqual(
            pillory.find_importable("example.use.Hey", (".",)),
            ("example/use.py", "Hey"),
        )

    def test_find_importable_empty(self):
        self.assertEqual(
            pillory.find_importable("example.empty", (".",)), ("example", "empty")
        )

    def test_find_importable_missing(self):
        self.assertEqual(
            pillory.find_importable("example.missing", (".",)),
            ("example/__init__.py", "missing"),
        )

    def test_find_importable_module(self):
        self.assertEqual(
            pillory.find_importable("use.do_something", ("example",)),
            ("example/use.py", "do_something"),
        )

    def test_find_module_definitions(self):
        self.assertEqual(
            pillory.find_module_definitions(
                cleandoc(
                    """
                    def hey():
                        pass

                    class Yo:
                        pass

                    WOT = 1
                    """
                )
            ),
            ["hey", "Yo", "WOT"],
        )

    def test_find_package_definitions(self):
        self.assertEqual(
            sorted(pillory.find_package_definitions("example")),
            [
                "definition",
                "empty",
                "test_use",
                "use",
            ],
        )


if __name__ == "__main__":
    unittest.main()
