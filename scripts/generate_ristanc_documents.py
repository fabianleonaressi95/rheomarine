#!/usr/bin/env python3
"""Generate private RISTANC application documents from repository drafts.

Outputs are written to dist/ristanc-private and must never be committed.
The bank sheet intentionally contains placeholders: never store an IBAN or
other banking credentials in this public repository or in GitHub Actions logs.
"""
from pathlib import Path
import re
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "ristanc" / "application-support"
OUT = ROOT / "dist" / "ristanc-private"

CV_SOURCE = SOURCE / "APPLICANT_CV_RESEARCH_ADDENDUM_DRAFT.md"
ANNEX_SOURCE = SOURCE / "APPLICANT_COMPETENCE_EVIDENCE_ANNEX_DRAFT.md"


def configure(doc):
    sec = doc.sections[0]
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.8)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)
    styles = doc.styles
    styles["Normal"].font.name = "Aptos"
    styles["Normal"].font.size = Pt(9.5)
    for name, size in (("Title", 19), ("Heading 1", 14), ("Heading 2", 11)):
        styles[name].font.name = "Aptos Display"
        styles[name].font.size = Pt(size)


def add_markdown_body(doc, text):
    """Small, dependency-light Markdown-to-DOCX converter for headings/lists."""
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            p = doc.add_heading(line[2:].strip(), level=0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=1)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=2)
        elif re.match(r"^[-*] ", line):
            doc.add_paragraph(re.sub(r"^[-*] ", "", line), style="List Bullet")
        elif re.match(r"^\d+[.)] ", line):
            doc.add_paragraph(re.sub(r"^\d+[.)] ", "", line), style="List Number")
        elif line in ("---", "***"):
            doc.add_paragraph("—" * 36)
        else:
            p = doc.add_paragraph()
            # Preserve text while removing common Markdown emphasis markers.
            p.add_run(re.sub(r"[*_]{1,2}", "", line))


def build_from_markdown(source, destination, title):
    if not source.exists():
        raise FileNotFoundError(f"Missing source draft: {source}")
    doc = Document()
    configure(doc)
    doc.add_heading(title, level=0)
    doc.add_paragraph(
        "RISTANC application support document — verify all facts, dates, "
        "references and claims before submission."
    )
    add_markdown_body(doc, source.read_text(encoding="utf-8"))
    doc.save(destination)


def build_bank_sheet(destination):
    doc = Document()
    configure(doc)
    doc.add_heading("BANK DETAILS — PAYMENT INFORMATION", level=0)
    p = doc.add_paragraph(
        "Supplementary payment sheet for the RISTANC application. "
        "Complete privately and send only through the official submission channel "
        "if requested by the programme."
    )
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph("")
    rows = [
        ("Account holder", "[TO COMPLETE PRIVATELY]"),
        ("Bank", "Vivibanca"),
        ("IBAN", "[TO COMPLETE PRIVATELY — DO NOT COMMIT TO GITHUB]"),
        ("BIC / SWIFT", "[IF REQUIRED BY THE PROGRAMME / BANK]"),
        ("Country", "Italy"),
        ("Account currency", "EUR"),
    ]
    table = doc.add_table(rows=0, cols=2)
    table.style = "Table Grid"
    for label, value in rows:
        cells = table.add_row().cells
        cells[0].text = label
        cells[1].text = value
    doc.add_paragraph("")
    doc.add_paragraph(
        "Security note: this file contains banking data once completed. "
        "Keep it outside the public repository, do not upload it as a GitHub "
        "artifact, and transmit it only if the RISTANC administrator confirms "
        "that it is required and provides an appropriate channel."
    )
    doc.save(destination)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    build_from_markdown(
        CV_SOURCE, OUT / "RISTANC_CV.docx",
        "CURRICULUM VITAE — RISTANC"
    )
    build_from_markdown(
        ANNEX_SOURCE, OUT / "RISTANC_COMPETENCE_EVIDENCE_ANNEX.docx",
        "COMPETENCE EVIDENCE ANNEX — RISTANC"
    )
    build_bank_sheet(OUT / "RISTANC_BANK_DETAILS_TEMPLATE.docx")
    print(f"Created documents in: {OUT}")
    print("Bank details are placeholders; complete the bank sheet locally only.")


if __name__ == "__main__":
    main()
