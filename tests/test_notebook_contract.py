"""Fast repository checks that do not require the private sales dataset or ML packages."""

import json
import re
import unittest
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "demand_forecasting.ipynb"


class NotebookContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

    def test_notebook_is_v4_with_markdown_and_code(self):
        self.assertEqual(self.notebook.get("nbformat"), 4)
        cells = self.notebook.get("cells", [])
        self.assertTrue(cells)
        self.assertTrue(any(cell.get("cell_type") == "markdown" for cell in cells))
        self.assertTrue(any(cell.get("cell_type") == "code" for cell in cells))

    def test_primary_notebook_sections_are_unique(self):
        headings = [
            line.strip()
            for cell in self.notebook.get("cells", [])
            if cell.get("cell_type") == "markdown"
            for line in "".join(cell.get("source", [])).splitlines()
            if line.startswith("## ")
        ]
        duplicates = sorted(heading for heading, count in Counter(headings).items() if count > 1)
        self.assertFalse(duplicates, f"Duplicate primary section headings: {duplicates}")

    def test_code_cells_are_valid_python_and_outputs_are_cleared(self):
        code_cells = [cell for cell in self.notebook["cells"] if cell.get("cell_type") == "code"]
        self.assertTrue(code_cells)
        for index, cell in enumerate(code_cells):
            source = "".join(cell.get("source", []))
            with self.subTest(code_cell=index):
                compile(source, f"{NOTEBOOK.name}:cell-{index}", "exec")
                self.assertFalse(cell.get("outputs", []), "Clear outputs before committing")
                self.assertIsNone(cell.get("execution_count"), "Clear execution counts before committing")

    def test_readme_local_markdown_links_resolve(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        targets = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", readme)
        local_targets = [
            target.split("#", 1)[0]
            for target in targets
            if target and not target.startswith(("https://", "http://", "mailto:"))
        ]
        self.assertTrue(local_targets)
        for target in local_targets:
            with self.subTest(target=target):
                self.assertTrue((ROOT / target).exists(), f"Missing README link target: {target}")

    def test_repository_svg_assets_are_well_formed(self):
        assets = sorted((ROOT / "assets").glob("*.svg"))
        self.assertTrue(assets)
        for asset in assets:
            with self.subTest(asset=asset.name):
                ElementTree.parse(asset)


if __name__ == "__main__":
    unittest.main()
