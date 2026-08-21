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
        labels = doc.get_page_labels()

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            lbl = labels[page_idx] if labels and page_idx < len(labels) else str(page_idx + 1)
            is_arabic = lbl.isdigit()
            if not is_arabic:
                continue

            book_page_num = int(lbl)
            is_recto = (book_page_num % 2 != 0)

            # Geometry definitions (pt)
            # Recto: Main Text = [54.0, 403.2], Margin Notes = [414.0, 485.0]
            # Verso: Margin Notes = [20.0, 92.0], Main Text = [100.8, 450.0]
            blocks = page.get_text("blocks")
            for b in blocks:
                bx0, by0, bx1, by1, text, block_no, block_type = b
                # Skip running headers and footers
                if by0 < 45.0 or by1 > 685.0:
                    continue

                if is_recto:
                    # Ignore intentional margin notes on right
                    if bx0 >= 408.0:
                        continue
                    # Check text block right overflow (> 2pt tolerance)
                    if bx1 > 405.2:
                        excess = bx1 - 403.2
                        snippet = text.replace("\n", " ").strip()[:45]
                        report.add_issue(LintIssue(
                            category="overflow",
                            severity="ERROR",
                            file="Physical-AI.pdf",
                            line=None,
                            page=book_page_num,
                            message=f"Text block exceeds right margin by {excess:.1f}pt ({excess*0.3527:.2f}mm)",
                            context=f"Book Page {book_page_num} (Recto) | '{snippet}...'"
                        ))
                else:
                    # Verso: Ignore intentional margin notes on left
                    if bx1 <= 96.0:
                        continue
                    # Check text block left overflow (> 2pt tolerance)
                    if bx0 < 98.8:
                        excess = 100.8 - bx0
                        snippet = text.replace("\n", " ").strip()[:45]
                        report.add_issue(LintIssue(
                            category="overflow",
                            severity="ERROR",
                            file="Physical-AI.pdf",
                            line=None,
                            page=book_page_num,
                            message=f"Text block exceeds left margin by {excess:.1f}pt ({excess*0.3527:.2f}mm)",
                            context=f"Book Page {book_page_num} (Verso) | '{snippet}...'"
                        ))

        doc.close()
