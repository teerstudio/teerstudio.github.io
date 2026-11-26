import re
import unittest
from pathlib import Path


def css_rule(stylesheet, selector):
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", stylesheet):
        if match.group(1).strip() == selector:
            declarations = {}
            for declaration in match.group(2).split(";"):
                if ":" in declaration:
                    name, value = declaration.split(":", 1)
                    declarations[name.strip()] = value.strip()
            return declarations
    return {}


class PageThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html = (Path(__file__).parents[1] / "index.html").read_text()
        style = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
        if style is None:
            raise AssertionError("index.html must contain an inline stylesheet")
        cls.stylesheet = style.group(1)

    def test_page_background_uses_light_blue(self):
        self.assertEqual(
            css_rule(self.stylesheet, "body").get("background-color"),
            "#eaf5ff",
        )

    def test_navigation_and_submit_button_use_blue(self):
        self.assertEqual(
            css_rule(self.stylesheet, ".navbar-inverse").get("background-color"),
            "#1976d2",
        )
        self.assertEqual(
            css_rule(self.stylesheet, ".btn-default").get("background-color"),
            "#1976d2",
        )

    def test_submit_button_hover_uses_darker_blue(self):
        self.assertEqual(
            css_rule(self.stylesheet, ".btn-default:hover,\n      .btn-default:focus").get(
                "background-color"
            ),
            "#1565c0",
        )


if __name__ == "__main__":
    unittest.main()
