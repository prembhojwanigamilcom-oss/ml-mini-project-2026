# -*- coding: utf-8 -*-
"""
Full LaTeX-Identical PDF Report Builder for:
'Impact of Experimental Randomness on ML Model Stability and Reproducibility'
Department of Artificial Intelligence and Data Science (AI&DS)
VESIT, Chembur, Mumbai
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, Flowable
)
from reportlab.pdfgen import canvas

# =========================================================================
# BOOKMARK / PAGE TRACKER FLOWABLE
# =========================================================================
PAGE_MAP = {}

class TrackPage(Flowable):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.width = 0
        self.height = 0

    def draw(self):
        PAGE_MAP[self.key] = self.canv._pageNumber


# =========================================================================
# LATEX NUMBERED CANVAS: FANCYHDR RUNNING HEADERS & ROMAN/ARABIC NUMERALS
# =========================================================================
class LaTeXNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        # Determine the page where Chapter 1 starts
        ch1_abs_page = PAGE_MAP.get('ch1', 11)
        
        for i, page_dict in enumerate(self.pages):
            self.__dict__.update(page_dict)
            page_num = i + 1
            self.draw_latex_header_footer(page_num, ch1_abs_page, num_pages)
            super().showPage()
        super().save()

    def draw_latex_header_footer(self, page_num, ch1_page, total_pages):
        # Page 1 is Title Page: NO header, NO footer
        if page_num == 1:
            return

        # LaTeX standard geometry:
        # A4: 595.28 pt wide, 841.89 pt high
        # Left margin = 108.0 pt (1.5 in), Right margin = 72.0 pt (1.0 in)
        # Text width = 595.28 - 108.0 - 72.0 = 415.28 pt
        left = 108.0
        right = 595.28 - 72.0
        top_header_y = 841.89 - 50.0
        header_rule_y = 841.89 - 56.0
        footer_y = 38.0

        self.saveState()

        # Running Header (fancyhdr style: \small\bfseries)
        self.setFont("Times-Bold", 10)
        self.setFillColor(colors.black)
        self.drawString(left, top_header_y, "Department of AI&DS")
        self.drawRightString(right, top_header_y, "Mini Project - 2B Report")

        # Header Rule (0.5 pt solid black line)
        self.setLineWidth(0.5)
        self.setStrokeColor(colors.black)
        self.line(left, header_rule_y, right, header_rule_y)

        # Running Footer: Centered Page Number
        # Roman numerals (i, ii, iii...) for frontmatter, Arabic (1, 2, 3...) for main matter
        if page_num < ch1_page:
            roman_numerals = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii", "xiii"]
            val = page_num - 1
            p_str = roman_numerals[val] if val < len(roman_numerals) else str(val)
        else:
            p_str = str(page_num - ch1_page + 1)

        self.setFont("Times-Roman", 11)
        self.drawCentredString((left + right) / 2.0, footer_y, p_str)
        self.restoreState()


# =========================================================================
# HELPER FUNCTIONS FOR LATEX BOOKTABS TABLES & FLOWABLES
# =========================================================================
def make_latex_booktabs(data, col_widths=None, align_left_col0=True):
    """Creates a table matching LaTeX booktabs (heavy top/bottom rule, light mid rule, no vertical lines)"""
    t = Table(data, colWidths=col_widths)
    ts = [
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),    # \toprule
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),    # \midrule
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, colors.black),  # \bottomrule
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEADING', (0, 0), (-1, -1), 13),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]
    if align_left_col0:
        ts.append(('ALIGN', (0, 0), (0, -1), 'LEFT'))
        ts.append(('ALIGN', (1, 0), (-1, -1), 'CENTER'))
    else:
        ts.append(('ALIGN', (0, 0), (-1, -1), 'LEFT'))
    t.setStyle(TableStyle(ts))
    return t


def code_listing_box(code_text, caption=""):
    """Creates a LaTeX lstlisting-styled box with line numbers and light gray background"""
    styles = getSampleStyleSheet()
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.black
    )
    lines = code_text.strip().split('\n')
    data = []
    for idx, l in enumerate(lines, 1):
        num_p = Paragraph(f"<font color='#666666'>{idx:2d}</font>", code_style)
        code_p = Paragraph(l.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;'), code_style)
        data.append([num_p, code_p])
    
    t = Table(data, colWidths=[24, 385])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ]))
    res = [t]
    if caption:
        cap_style = ParagraphStyle('ListCap', parent=styles['Normal'], fontName='Times-Bold', fontSize=9, leading=12, alignment=1)
        res.append(Spacer(1, 3))
        res.append(Paragraph(caption, cap_style))
    return res


print("Helper functions ready.")
