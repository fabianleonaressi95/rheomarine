#!/usr/bin/env python3
"""Build a review-ready RISTANC application-form DOCX from repository drafts.

This is a newly laid-out working copy based on the extracted official form text,
not the original DOCX template. Applicant-only fields and signature remain blank.
"""
from pathlib import Path
import re
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ROOT / "docs" / "ristanc" / "application-support"
SECTION_C = SUPPORT / "SECTION_C_DRAFT_RHEOMARINE_SLO_EN.md"
OUT = ROOT / "dist" / "ristanc-private" / "RISTANC_APPLICATION_FORM_WORKING_COPY.docx"


def setup(doc):
    sec = doc.sections[0]
    sec.top_margin = Cm(1.5)
    sec.bottom_margin = Cm(1.5)
    sec.left_margin = Cm(1.7)
    sec.right_margin = Cm(1.7)
    doc.styles["Normal"].font.name = "Aptos"
    doc.styles["Normal"].font.size = Pt(9)
    for name, size in (("Title", 18), ("Heading 1", 13), ("Heading 2", 10)):
        doc.styles[name].font.name = "Aptos Display"
        doc.styles[name].font.size = Pt(size)


def field_table(doc, rows, headers=("Field", "Entry")):
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    for left, right in rows:
        cells = table.add_row().cells
        cells[0].text, cells[1].text = left, right
        for c in cells:
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    doc.add_paragraph()


def add_md(doc, text):
    in_table = False
    table_rows = []
    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        parsed = []
        for line in table_rows:
            cells = [x.strip() for x in line.strip().strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", x or "-") for x in cells):
                continue
            parsed.append(cells)
        if parsed:
            width = max(map(len, parsed))
            t = doc.add_table(rows=0, cols=width)
            t.style = "Table Grid"
            for row in parsed:
                cells = t.add_row().cells
                for i in range(width):
                    cells[i].text = re.sub(r"[*_]", "", row[i]) if i < len(row) else ""
        doc.add_paragraph()
        table_rows = []

    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("|") and line.endswith("|"):
            in_table = True
            table_rows.append(line)
            continue
        if in_table:
            flush_table()
            in_table = False
        if not line or line in ("---", "***"):
            continue
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            doc.add_heading(line[3:], level=1)
        elif line.startswith("### "):
            doc.add_heading(line[4:], level=2)
        elif line.startswith("- "):
            doc.add_paragraph(re.sub(r"[*_]", "", line[2:]), style="List Bullet")
        elif re.match(r"^\d+\. ", line):
            doc.add_paragraph(re.sub(r"[*_]", "", re.sub(r"^\d+\. ", "", line)), style="List Number")
        else:
            doc.add_paragraph(re.sub(r"[*_]", "", line))
    if in_table:
        flush_table()


def main():
    if not SECTION_C.exists():
        raise FileNotFoundError(SECTION_C)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    setup(doc)
    p = doc.add_heading("RISTANC — APPLICATION FORM", level=0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph("Working copy for applicant review — not the original official form.")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(
        "Prepared from the repository's full-text extraction of the official RISTANC "
        "application form and the current RheoMarine-SLO Section C draft. Transfer "
        "to the official form if the call requires its original template."
    )

    doc.add_heading("SECTION A — APPLICANT DETAILS", level=1)
    doc.add_heading("A.1 Legal entity", level=2)
    doc.add_paragraph("Not applicable. Application submitted by a natural person; leave the official A.1 section blank.")
    doc.add_heading("A.2 Natural person", level=2)
    field_table(doc, [
        ("First name and surname", "Fabian Leo Naressi"),
        ("Tax number", "[APPLICANT TO ENTER — Italian codice fiscale]"),
        ("Permanent residential address", "[APPLICANT TO ENTER]"),
        ("Telephone / mobile phone", "[APPLICANT TO ENTER]"),
        ("Email", "fabianleoatlas@gmail.com"),
    ])
    doc.add_heading("A.3 Contact person", level=2)
    doc.add_paragraph("Same person as the natural-person applicant. Leave blank unless the official DOCX requires repetition.")

    doc.add_heading("SECTION B — DECLARATIONS", level=1)
    field_table(doc, [
        ("Conflict of interest", "☒ No actual, potential or perceived conflict declared by applicant. Applicant to re-check scope includes any proposed subcontractors/partners."),
        ("Ethical aspects document read and commitments accepted", "☐ YES  ☐ NO — applicant must personally confirm before ticking."),
        ("No other European, national or local public funding for the project or any part", "☒ YES — based on applicant's confirmation; re-check before signature."),
    ], headers=("Declaration", "Working-copy entry"))
    doc.add_paragraph("The applicant undertakes to notify the coordinator without delay if a conflict arises after submission.")

    doc.add_heading("SECTION C — PROJECT IDEA", level=1)
    doc.add_paragraph("Project title: RheoMarine-SLO: Testing the role of biological aggregation and effective particle properties in microplastic transport and settling in the Slovenian territorial sea")
    doc.add_paragraph("Project duration: 8 months from the effective date of the signed funding agreement.")
    section_text = SECTION_C.read_text(encoding="utf-8")
    section_text = section_text.split("## Applicant review")[0]
    section_text = re.sub(r"^# RISTANC Application.*\n", "", section_text, count=1)
    section_text = re.sub(r"^\*\*Project:\*\*.*\n", "", section_text, count=1)
    section_text = re.sub(r"^\*\*Status:\*\*.*\n", "", section_text, count=1)
    section_text = re.sub(r"^\*\*Drafting basis:\*\*.*\n", "", section_text, count=1)
    section_text = re.sub(r"^\*\*Important:\*\*.*\n", "", section_text, count=1)
    add_md(doc, section_text)

    doc.add_heading("FINANCIAL PLAN", level=1)
    field_table(doc, [
        ("A.1 Employees / equivalent staff", "0.00"),
        ("A.2 Natural persons under direct contract", "0.00"),
        ("A.3 SME owners and natural persons recipients", "220 hours × EUR 30.00 = EUR 6,600.00"),
        ("B.1 Direct costs of subcontractors", "5 µFTIR samples + fee; EUR 2,047.00 before VAT; EUR 2,497.34 indicative incl. 22% Italian VAT"),
        ("C.1 Travel and subsistence", "EUR 240.00"),
        ("C.2 Equipment", "EUR 0.00"),
        ("C.3 Consumables", "EUR 0.00"),
        ("C.4 Meetings and seminars", "EUR 120.00"),
        ("C.5 Communication activities", "EUR 240.00"),
        ("C.6 Other", "EUR 0.00"),
        ("Total direct costs A+B+C", "EUR 9,697.34"),
        ("E. Indirect costs (25% × (A+C))", "EUR 1,800.00"),
        ("TOTAL FUNDING REQUESTED", "EUR 11,497.34"),
    ])
    doc.add_paragraph(
        "Budget qualification: Italian VAT is an indicative 22% planning assumption, "
        "not a final supplier tax determination. Confirm VAT and the tax/social-security "
        "treatment of the A.3 all-in amount before contracting."
    )

    doc.add_heading("INCOME AND OTHER SOURCES", level=1)
    field_table(doc, [
        ("Other income / contributions", "[APPLICANT TO CONFIRM; enter EUR 0.00 and None only if accurate]"),
        ("Funding requested (II)", "EUR 11,497.34"),
        ("Total (I + II)", "[COMPLETE AFTER CONFIRMING OTHER INCOME]"),
    ])

    doc.add_heading("STATEMENT OF ACCURACY, ANNEXES AND SIGNATURE", level=1)
    doc.add_paragraph(
        "Applicant must personally verify and accept the official statement of accuracy, "
        "eligibility conditions and GDPR notice before submission."
    )
    doc.add_paragraph("Annexes proposed under OTHER: CV; competence evidence annex; Measurlabs quotation M49249; residence certificate and English translation as supplementary documents if appropriate.")
    doc.add_paragraph("Legal-entity register extract and articles of association: not applicable to natural-person applicant. Power of attorney: not applicable if applicant signs and submits personally.")
    field_table(doc, [
        ("Date", "[APPLICANT TO ENTER]"),
        ("Applicant's handwritten / digital signature", "[SIGN HERE — DO NOT SUBMIT WITHOUT SIGNATURE]"),
    ])
    doc.add_paragraph(
        "Important status: this is a working-copy reconstruction based on the extracted "
        "official form text. It is not the official DOCX template and is not signed. "
        "Before submission, transfer/check all entries against the official form and "
        "call instructions. Do not treat placeholders as completed fields."
    )
    doc.save(OUT)
    print(f"Created: {OUT}")


if __name__ == "__main__":
    main()
