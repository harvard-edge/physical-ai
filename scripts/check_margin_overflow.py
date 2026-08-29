#!/usr/bin/env python3
"""
scripts/check_margin_overflow.py

Automated PDF Margin Overflow and Sidenote Clipping Validator for Physical AI.
Scans all pages of the compiled textbook PDF to detect any footnotes, sidenotes,
or margin text extending beyond printable page boundaries.
"""

import sys
import os
import fitz  # PyMuPDF

def scan_pdf_margin_overflow(pdf_path, bottom_threshold=675.0, top_threshold=35.0, right_margin_x=390.0):
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return 1

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"🔍 Scanning {total_pages} pages in {os.path.basename(pdf_path)} for margin overflows...")

    page_overflows = {}

    for page_idx in range(total_pages):
        page = doc[page_idx]
        rect = page.rect
        blocks = page.get_text("blocks")
        
        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            # In our 540x720 layout, the right margin starts around x0 >= 390
            if x0 >= right_margin_x:
                # Ignore top running header / folio
                if y0 < top_threshold or (y0 < 45 and ("Chapter" in text or "Part" in text or "Physical" in text)):
                    continue
                
                # Check for bottom overflow
                if y1 > bottom_threshold:
                    overflow_amount = y1 - bottom_threshold
                    if page_idx + 1 not in page_overflows:
                        page_overflows[page_idx + 1] = []
                    page_overflows[page_idx + 1].append({
                        "y0": y0,
                        "y1": y1,
                        "page_height": rect.height,
                        "overflow_pts": overflow_amount,
                        "text": text.strip().replace("\n", " ")
                    })

    if not page_overflows:
        print(f"✅ PASSED: Zero margin overflows detected across all {total_pages} pages.")
        return 0

    print(f"\n⚠️  WARNING: Detected margin overflows on {len(page_overflows)} pages:\n")
    max_overflow = 0.0
    for page_num, items in sorted(page_overflows.items()):
        worst_item = max(items, key=lambda x: x["overflow_pts"])
        max_overflow = max(max_overflow, worst_item["overflow_pts"])
        snippet = worst_item["text"]
        if len(snippet) > 85:
            snippet = snippet[:82] + "..."
        print(f"  • PDF Page {page_num:3d} | Overflow: {worst_item["overflow_pts"]:4.1f} pt (bottom: {worst_item["y1"]:.1f}/{worst_item["page_height"]:.1f} pt)")
        print(f"    Snippet: \"{snippet}\"\n")

    print(f"Total affected pages: {len(page_overflows)} | Max overflow: {max_overflow:.1f} pt")
    return 1 if max_overflow > 15.0 else 0

if __name__ == "__main__":
    default_pdf = "/Users/VJ/GitHub/PhysicalAI-vj-exp/book/_build/Physical-AI.pdf"
    target = sys.argv[1] if len(sys.argv) > 1 else default_pdf
    exit_code = scan_pdf_margin_overflow(target)
    sys.exit(exit_code)
