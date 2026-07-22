#!/usr/bin/env python3
"""Focused, CPU-only checks for the anonymous AAAI-27 manuscript."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


MANUSCRIPT = Path(__file__).resolve().parent
ROOT = MANUSCRIPT.parent
TEX = MANUSCRIPT / "main.tex"
BIB = MANUSCRIPT / "references.bib"
PDF = MANUSCRIPT / "build" / "main.pdf"
CHECKLIST_TEX = MANUSCRIPT / "reproducibility_checklist.tex"
CHECKLIST_PDF = MANUSCRIPT / "build" / "reproducibility_checklist.pdf"
FIGURE = MANUSCRIPT / "figures" / "verifier_cost_sign_map.png"
FIGURE_SCRIPT = MANUSCRIPT / "figures" / "make_economics_figure.py"
FIGURE_MANIFEST = MANUSCRIPT / "FIGURE_MANIFEST.json"
SUBMISSION = ROOT / "docs" / "AAAI27_ABSTRACT_SUBMISSION.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalize_prose(value: str) -> str:
    value = value.replace("---", "-").replace("—", "-")
    value = value.replace("\\%", "%")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def submitted_block(markdown: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
    require(match is not None, f"missing submission heading: {heading}")
    lines = []
    for line in match.group("body").splitlines():
        if line.startswith(">"):
            lines.append(line[1:].strip())
    return " ".join(lines).replace("**", "")


def command_output(*args: str) -> str:
    return subprocess.run(
        args,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).stdout


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    tex = TEX.read_text(encoding="utf-8")
    bib = BIB.read_text(encoding="utf-8")
    submission = SUBMISSION.read_text(encoding="utf-8")
    checklist = CHECKLIST_TEX.read_text(encoding="utf-8")
    figure_script = FIGURE_SCRIPT.read_text(encoding="utf-8")
    figure_manifest = json.loads(FIGURE_MANIFEST.read_text(encoding="utf-8"))

    title_match = re.search(r"\\title\{([^}]*)\}", tex)
    abstract_match = re.search(
        r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.DOTALL
    )
    require(title_match is not None, "main.tex has no title")
    require(abstract_match is not None, "main.tex has no abstract")
    require(
        normalize_prose(title_match.group(1))
        == normalize_prose(submitted_block(submission, "Title")),
        "title differs from the authoritative OpenReview text",
    )
    require(
        normalize_prose(abstract_match.group(1))
        == normalize_prose(submitted_block(submission, "Abstract")),
        "abstract differs from the authoritative OpenReview text",
    )

    require(
        "\\documentclass[letterpaper]{article}" in tex,
        "official letterpaper document class missing",
    )
    require(
        "\\usepackage[submission]{aaai2027}" in tex,
        "AAAI anonymous submission style missing",
    )
    require("\\author{Anonymous Submission}" in tex, "anonymous author missing")
    require("\\affiliations{}" in tex, "affiliations must be empty")
    require("/TemplateVersion (2027.1)" in tex, "template version missing")
    require("\\input{" not in tex, "main paper must remain a single TeX source")

    forbidden_packages = {
        "authblk",
        "balance",
        "CJK",
        "float",
        "flushend",
        "fullpage",
        "geometry",
        "hyperref",
        "navigator",
        "indentfirst",
        "layout",
        "multicol",
        "nameref",
        "savetrees",
        "setspace",
        "stfloats",
        "tabu",
        "titlesec",
        "tocbibind",
        "ulem",
        "wrapfig",
    }
    packages = set(
        re.findall(r"\\usepackage(?:\[[^]]*\])?\{([^}]*)\}", tex)
    )
    require(
        not (packages & forbidden_packages),
        f"forbidden package(s): {sorted(packages & forbidden_packages)}",
    )
    forbidden_commands = (
        r"\nocopyright",
        r"\addtolength",
        r"\balance",
        r"\baselinestretch",
        r"\clearpage",
        r"\columnsep",
        r"\newpage",
        r"\pagebreak",
        r"\pagestyle",
        r"\vspace{-",
        r"\vskip{-",
    )
    for command in forbidden_commands:
        require(command not in tex, f"forbidden command present: {command}")

    citation_groups = re.findall(r"\\cite[a-zA-Z]*\{([^}]*)\}", tex)
    citation_keys = {
        key.strip() for group in citation_groups for key in group.split(",")
    }
    bib_keys = set(re.findall(r"^@\w+\{([^,]+),", bib, flags=re.MULTILINE))
    require(citation_keys <= bib_keys, f"missing BibTeX keys: {citation_keys - bib_keys}")

    checklist_questions = checklist.split("% The questions start here", 1)[-1]
    require(
        "Type your response here" not in checklist_questions,
        "reproducibility checklist has unanswered questions",
    )
    require("#D55E00" not in figure_script, "figure uses low-contrast orange")
    require("#777777" not in figure_script, "figure uses low-contrast gray")
    require("#A33F00" in figure_script, "approved high-contrast curve color missing")
    require("#666666" in figure_script, "approved guide color missing")
    require(
        sha256(ROOT / "gates" / "C3" / "v2_1" / "results_v2_1.json")
        == figure_manifest["input"]["sha256"],
        "Figure 2 input hash differs from manifest",
    )
    require(
        sha256(FIGURE_SCRIPT) == figure_manifest["generator"]["sha256"],
        "Figure 2 generator hash differs from manifest",
    )
    require(
        sha256(FIGURE) == figure_manifest["output"]["sha256"],
        "Figure 2 output hash differs from manifest",
    )

    if PDF.exists():
        newest_source = max(
            path.stat().st_mtime for path in (TEX, BIB, FIGURE, FIGURE_SCRIPT)
        )
        require(
            PDF.stat().st_mtime >= newest_source,
            "main PDF is older than a manuscript source or figure",
        )
        info = command_output("pdfinfo", str(PDF))
        pages_match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
        require(pages_match is not None, "pdfinfo did not report page count")
        pages = int(pages_match.group(1))
        require(pages <= 9, f"main PDF has {pages} pages; limit is 9")
        require(
            "Page size:       612 x 792 pts (letter)" in info,
            "main PDF is not US Letter",
        )
        require(not re.search(r"^Author:\s+\S", info, re.MULTILINE), "PDF leaks author")

        fonts = command_output("pdffonts", str(PDF))
        font_lines = [line for line in fonts.splitlines()[2:] if line.strip()]
        require(font_lines, "no PDF fonts detected")
        for line in font_lines:
            require("Type 3" not in line, f"Type 3 font detected: {line}")
            columns = line.split()
            require("yes" in columns, f"font may not be embedded: {line}")

        pdf_text = command_output("pdftotext", "-layout", str(PDF), "-")
        require("/Users/" not in pdf_text, "PDF leaks a local filesystem path")
        pages_text = pdf_text.split("\f")
        reference_page = next(
            (index + 1 for index, page in enumerate(pages_text) if "References" in page),
            None,
        )
        require(reference_page == 8, f"references begin on page {reference_page}, not 8")
        page_eight = command_output(
            "pdftotext", "-f", "8", "-l", "8", "-layout", str(PDF), "-"
        ).lstrip()
        require(
            page_eight.startswith("References"),
            "page 8 contains non-reference content before the References heading",
        )

        images = command_output("pdfimages", "-list", str(PDF))
        image_rows = [line.split() for line in images.splitlines() if line.strip()]
        raster_ppi = []
        for columns in image_rows:
            if len(columns) >= 14 and columns[2] == "image":
                try:
                    raster_ppi.append((int(columns[12]), int(columns[13])))
                except ValueError:
                    continue
        require(raster_ppi, "no raster figure found in main PDF")
        require(
            all(x_ppi >= 295 and y_ppi >= 295 for x_ppi, y_ppi in raster_ppi),
            f"raster figure below approximately 300 ppi: {raster_ppi}",
        )

    require(CHECKLIST_PDF.exists(), "standalone checklist PDF is missing")
    require(
        CHECKLIST_PDF.stat().st_mtime >= CHECKLIST_TEX.stat().st_mtime,
        "checklist PDF is older than checklist source",
    )
    checklist_info = command_output("pdfinfo", str(CHECKLIST_PDF))
    require(
        "Page size:       612 x 792 pts (letter)" in checklist_info,
        "checklist PDF is not US Letter",
    )
    checklist_fonts = command_output("pdffonts", str(CHECKLIST_PDF))
    require("Type 3" not in checklist_fonts, "Type 3 font detected in checklist")

    print("PASS title and abstract lock")
    print("PASS AAAI anonymous source constraints")
    print(f"PASS {len(citation_keys)} cited keys resolved")
    print("PASS completed standalone reproducibility checklist")
    print("PASS Figure 2 source, generator, and output hashes")
    if PDF.exists():
        print(
            f"PASS PDF: {pages} pages, reference-only page 8, US Letter, "
            "embedded non-Type-3 fonts, approximately 300-ppi raster figure"
        )


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, subprocess.CalledProcessError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
