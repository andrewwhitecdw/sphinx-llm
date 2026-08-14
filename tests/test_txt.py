# SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for sphinx_llm.txt."""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

from sphinx_llm.txt import MarkdownGenerator


def test_build_markdown_files_creates_nested_build_dir():
    """The markdown build dir should be created even when its parent outdir is absent."""
    generator = MarkdownGenerator.__new__(MarkdownGenerator)
    generator.parallel = True
    generator.md_build_logfile = tempfile.NamedTemporaryFile(
        mode="w", delete=False, prefix="sphinx_llm_test_", suffix=".log"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator.app = type("App", (), {"srcdir": Path(tmpdir) / "src"})()
        generator.md_build_dir = Path(tmpdir) / "missing_parent" / "out" / "_markdown_build"

        with patch.object(subprocess, "Popen"):
            generator.build_markdown_files()

        assert generator.md_build_dir.exists()
