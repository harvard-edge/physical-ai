"""Visual bounding box and margin overflow verification via PyMuPDF."""

from __future__ import annotations

from .base import BaseCheck, CheckRegistry
from ..context import BookContext
from ..report import LintIssue, LintReport

try:
    import fitz  # PyMuPDF
    HAVE_FITZ = True
except ImportError:
    HAVE_FITZ = False


@CheckRegistry.register
class VisualMarginBoundingBoxCheck(BaseCheck):
    name = "visual_margin_bounding_box"
    description = "Performs vector-level bounding box and margin analysis on compiled PDF"
    category = "layout"

    def run(self, ctx: BookContext, report: LintReport):
        if not HAVE_FITZ:
            report.add_issue(LintIssue(
                category="layout",
                severity="INFO",
                file="Physical-AI.pdf",
                line=None,
                page=None,
                message="PyMuPDF (fitz) is not installed; skipping vector bounding box analysis."
            ))
            return

        if not ctx.pdf_path.exists():
            report.add_issue(LintIssue(
                category="layout",
                severity="ERROR",
                file=str(ctx.pdf_path),
                line=None,
                page=None,
                message="PDF not found. Rebuild with 'pai build' first."
            ))
            return

        doc = fitz.open(str(ctx.pdf_path))
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            lbl = page.get_label() if hasattr(page, "get_label") else str(page_idx + 1)
            is_arabic = lbl.isdigit()
            if not is_arabic:
                continue

            book_page_num = int(lbl)
            is_recto = (book_page_num % 2 != 0)

            # Geometry definitions (pt)
            # Recto: Main Text = [54.0, 403.2], Margin Notes = [414.0, 485.0]
            # Verso: Margin Notes = [20.0, 92.0], Main Text = [100.8, 450.0]
            text_dict = page.get_text("dict")
            for b in text_dict.get("blocks", []):
                if "lines" not in b:
                    continue
                for line in b["lines"]:
                    lx0, ly0, lx1, ly1 = line["bbox"]
                    line_text = "".join(s["text"] for s in line.get("spans", [])).strip()
                    if not line_text:
                        continue

                    # Skip running headers and footers
                    if ly0 < 45.0 or ly1 > 685.0:
                        continue

                    if is_recto:
                        # Margin note region on Recto: [414.0, 485.0]
                        if lx0 >= 408.0:
                            if lx1 > 487.0:
                                excess = lx1 - 485.0
                                report.add_issue(LintIssue(
                                    category="overflow",
                                    severity="ERROR" if excess > 8.0 else "WARNING",
                                    file="Physical-AI.pdf",
                                    line=None,
                                    page=book_page_num,
                                    message=f"Margin note exceeds right page edge by {excess:.1f}pt ({excess*0.3527:.2f}mm)",
                                    context=f"Book Page {book_page_num} (Recto Margin) | '{line_text[:45]}...'"
                                ))
                            continue

                        # Main text on Recto: [54.0, 403.2]
                        if lx0 < 52.0:
                            excess = 54.0 - lx0
                            report.add_issue(LintIssue(
                                category="overflow",
                                severity="ERROR" if excess > 8.0 else "WARNING",
                                file="Physical-AI.pdf",
                                line=None,
                                page=book_page_num,
                                message=f"Text line exceeds left inner spine margin by {excess:.1f}pt ({excess*0.3527:.2f}mm)",
                                context=f"Book Page {book_page_num} (Recto) | '{line_text[:45]}...'"
                            ))
                        if lx1 > 405.2:
                            excess = lx1 - 403.2
                            report.add_issue(LintIssue(
                                category="overflow",
                                severity="ERROR" if excess > 8.0 else "WARNING",
                                file="Physical-AI.pdf",
                                line=None,
                                page=book_page_num,
                                message=f"Text line exceeds right margin into note gutter by {excess:.1f}pt ({excess*0.3527:.2f}mm)",
                                context=f"Book Page {book_page_num} (Recto) | '{line_text[:45]}...'"
                            ))
                    else:
                        # Margin note region on Verso: [20.0, 92.0]
                        if lx1 <= 96.0:
                            if lx0 < 18.0:
                                excess = 20.0 - lx0
                                report.add_issue(LintIssue(
                                    category="overflow",
                                    severity="ERROR" if excess > 8.0 else "WARNING",
                                    file="Physical-AI.pdf",
                                    line=None,
                                    page=book_page_num,
                                    message=f"Margin note exceeds left outer page edge by {excess:.1f}pt ({excess*0.3527:.2f}mm)",
                                    context=f"Book Page {book_page_num} (Verso Margin) | '{line_text[:45]}...'"
                                ))
                            continue

                        # Main text on Verso: [100.8, 450.0]
                        if lx0 < 98.8:
                            excess = 100.8 - lx0
                            report.add_issue(LintIssue(
                                category="overflow",
                                severity="ERROR" if excess > 8.0 else "WARNING",
                                file="Physical-AI.pdf",
                                line=None,
                                page=book_page_num,
                                message=f"Text line exceeds left margin into note gutter by {excess:.1f}pt ({excess*0.3527:.2f}mm)",
                                context=f"Book Page {book_page_num} (Verso) | '{line_text[:45]}...'"
                            ))
                        if lx1 > 452.0:
                            excess = lx1 - 450.0
                            report.add_issue(LintIssue(
                                category="overflow",
                                severity="ERROR" if excess > 8.0 else "WARNING",
                                file="Physical-AI.pdf",
                                line=None,
                                page=book_page_num,
                                message=f"Text line exceeds right inner spine margin by {excess:.1f}pt ({excess*0.3527:.2f}mm)",
                                context=f"Book Page {book_page_num} (Verso) | '{line_text[:45]}...'"
                            ))

        doc.close()
