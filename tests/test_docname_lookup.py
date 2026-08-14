"""Tests for MarkdownGenerator docname lookup."""
from pathlib import Path
import unittest

from sphinx_llm.txt import MarkdownGenerator


class _FakeApp:
    def __init__(self):
        self.config = {}


class TestGetDocnameFromMdFile(unittest.TestCase):
    def setUp(self):
        self.generator = MarkdownGenerator(_FakeApp())
        self.generator.md_build_dir = Path("/build/_markdown_build")

    def test_html_md_suffix(self):
        result = self.generator._get_docname_from_md_file(
            Path("/build/_markdown_build/foo.html.md")
        )
        self.assertEqual(result, "foo")

    def test_plain_md_suffix(self):
        result = self.generator._get_docname_from_md_file(
            Path("/build/_markdown_build/foo.md")
        )
        self.assertEqual(result, "foo")

    def test_nested_html_md(self):
        result = self.generator._get_docname_from_md_file(
            Path("/build/_markdown_build/subdir/index.html.md")
        )
        self.assertEqual(result, "subdir/index")

    def test_preserves_version_dots(self):
        # A source like release-1.0.rst must not lose the '.0' suffix.
        result = self.generator._get_docname_from_md_file(
            Path("/build/_markdown_build/release-1.0.md")
        )
        self.assertEqual(result, "release-1.0")


