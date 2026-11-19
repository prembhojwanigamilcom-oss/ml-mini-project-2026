# -*- coding: utf-8 -*-
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class VESITCanvas(canvas.Canvas):
    """
    Two-pass canvas that reproduces the exact VESIT institutional header
    and footer styling seen in the user's reference PDF.
    Header: Logo on left, Red institutional text, Black university and department text, solid rule.
    Footer: Centered page numbers.
    Suppressed on Page 1 (Title Page).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_vesit_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_vesit_decorations(self, page_count):
        w, h = A4
        if self._pageNumber > 1:
            self.saveState()
            
            # Logo at top left
            logo_path = "figures/VESIT LOGO ICON (1).png"
            if os.path.exists(logo_path):
                # 32 pt wide by 47 pt high
                self.drawImage(logo_path, 54, h - 80, width=32, height=47, mask='auto')
            
            # Header text centered in page or header area
            cx = w / 2.0 + 10  # optical center
            
            # Line 1: Vivekanand Education Society’s in bold red
            self.setFont("Times-Bold", 10.5)
            self.setFillColor(colors.HexColor("#C00000"))
            self.drawCentredString(cx, h - 42, "Vivekanand Education Society’s")
            
            # Line 2: Institute of Technology in bold black
            self.setFont("Times-Bold", 10.0)
            self.setFillColor(colors.black)
            self.drawCentredString(cx, h - 54, "Institute of Technology")
            
            # Line 3: Autonomous affiliation in small regular black
            self.setFont("Times-Roman", 6.8)
            self.drawCentredString(cx, h - 64, "(Autonomous Institute Affiliated to University of Mumbai, Approved by AICTE & Recognised by Govt. of Maharashtra)")
            
            # Line 4: Department in bold black
            self.setFont("Times-Bold", 9.0)
            self.drawCentredString(cx, h - 74, "Department of Artificial Intelligence & Data Science")
            
            # Horizontal line under header spanning 54 to w - 54
            self.setStrokeColor(colors.black)
            self.setLineWidth(1.0)
            self.line(54, h - 83, w - 54, h - 83)
            
            # Small tick accent under logo
            self.line(54, h - 83, 90, h - 83)
            
            # Running Footer: Centered page number
            self.setFont("Times-Roman", 10)
            self.setFillColor(colors.black)
            self.drawCentredString(w / 2.0, 32, f"{self._pageNumber}")
            
            self.restoreState()

def build_pdf():
    pdf_filename = "Forest_Cover_Type_Mini_Project_Report_Polished.pdf"
    
    # Page Margins: 54 pt left/right (0.75 in), 96 pt top (leaves room for the 83pt header), 50 pt bottom
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=96,
        bottomMargin=50
    )

    # Styles matching reference report
    styles = getSampleStyleSheet()
    
    title_inst = ParagraphStyle('TitleInst', fontName='Times-Bold', fontSize=13, leading=17, alignment=1, textColor=colors.black)
    title_sub = ParagraphStyle('TitleSub', fontName='Times-Roman', fontSize=8, leading=11, alignment=1, textColor=colors.black)
    title_dept = ParagraphStyle('TitleDept', fontName='Times-Bold', fontSize=11, leading=15, alignment=1, textColor=colors.black)
    title_rep_on = ParagraphStyle('TitleRepOn', fontName='Times-Roman', fontSize=10.5, leading=14, alignment=1, textColor=colors.black)
    title_project = ParagraphStyle('TitleProj', fontName='Times-Bold', fontSize=13, leading=17, alignment=1, textColor=colors.black)
    
    cert_title = ParagraphStyle('CertTitle', fontName='Times-Bold', fontSize=13, leading=17, alignment=1, textColor=colors.black, spaceAfter=14)
    chap_title = ParagraphStyle('ChapTitle', fontName='Times-Bold', fontSize=13, leading=17, alignment=1, textColor=colors.black, spaceAfter=12)
    sec_title = ParagraphStyle('SecTitle', fontName='Times-Bold', fontSize=11, leading=15, alignment=0, textColor=colors.black, spaceBefore=9, spaceAfter=4)
    subsec_title = ParagraphStyle('SubSecTitle', fontName='Times-Bold', fontSize=10, leading=14, alignment=0, textColor=colors.black, spaceBefore=6, spaceAfter=3)
    
    body = ParagraphStyle('Body', fontName='Times-Roman', fontSize=10, leading=14.5, alignment=4, textColor=colors.black, spaceAfter=6)
    bullet = ParagraphStyle('Bullet', fontName='Times-Roman', fontSize=10, leading=14, alignment=4, textColor=colors.black, leftIndent=18, firstLineIndent=-12, spaceAfter=3)
    
    table_cell = ParagraphStyle('TCell', fontName='Times-Roman', fontSize=8.5, leading=11.5, textColor=colors.black, alignment=1)
    table_cell_left = ParagraphStyle('TCellL', fontName='Times-Roman', fontSize=8.5, leading=11.5, textColor=colors.black, alignment=0)
    table_cell_bold = ParagraphStyle('TCellB', fontName='Times-Bold', fontSize=8.5, leading=11.5, textColor=colors.black, alignment=1)
    table_cell_bold_left = ParagraphStyle('TCellBL', fontName='Times-Bold', fontSize=8.5, leading=11.5, textColor=colors.black, alignment=0)
    
    table_header = ParagraphStyle('THead', fontName='Times-Bold', fontSize=9, leading=12, textColor=colors.black, alignment=1)
    table_caption = ParagraphStyle('TCap', fontName='Times-Bold', fontSize=9.5, leading=13, alignment=1, textColor=colors.black, spaceBefore=8, spaceAfter=5)
    fig_caption = ParagraphStyle('FigCap', fontName='Times-Bold', fontSize=9, leading=12, alignment=1, textColor=colors.black, spaceBefore=4, spaceAfter=10)
    
    code_block = ParagraphStyle('CodeBlock', fontName='Courier', fontSize=7.8, leading=10.5, textColor=colors.black, leftIndent=12, spaceAfter=6)

    # Reference soft blue table header color: #D9E1F2
    c_th_bg = colors.HexColor("#D9E1F2")
    c_grid = colors.black

    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Vivekanand Education Society's Institute of Technology</b>", title_inst))
    story.append(Spacer(1, 3))
    story.append(Paragraph("(An Autonomous Institute Affiliated to University of Mumbai, Approved by AICTE & Recognised by Govt. of Maharashtra)", title_sub))
    story.append(Paragraph("Hashu Advani Memorial Complex, Collector Colony, Chembur East, Mumbai – 400074", title_sub))
    story.append(Spacer(1, 22))
    story.append(Paragraph("<b>Department of Artificial Intelligence and Data Science</b>", title_dept))
    story.append(Spacer(1, 25))
    
    # VESIT Emblem
    logo_path = "figures/VESIT LOGO ICON (1).png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=1.15*inch, height=1.7*inch))
    story.append(Spacer(1, 28))
    
    story.append(Paragraph("A Mini Project Report on", title_rep_on))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>IMPACT OF EXPERIMENTAL RANDOMNESS ON ML MODEL</b>", title_project))
    story.append(Paragraph("<b>STABILITY AND REPRODUCIBILITY</b>", title_project))
    story.append(Spacer(1, 28))
    
    story.append(Paragraph("<b>Submitted by</b>", ParagraphStyle('SubBy', fontName='Times-Bold', fontSize=10.5, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 6))
    
    st_box = [
        [Paragraph("Prem K.K. Bhojwani", table_cell), Paragraph("Roll No. 04", table_cell)],
        [Paragraph("Jiya Gurbani", table_cell), Paragraph("Roll No. 15", table_cell)],
        [Paragraph("Harsh Digreja", table_cell), Paragraph("Roll No. 12", table_cell)]
    ]
    st_table = Table(st_box, colWidths=[2.8*inch, 2.0*inch], hAlign='CENTER')
    st_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.7, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(st_table)
    story.append(Spacer(1, 25))
    
    story.append(Paragraph("<b>Under the Guidance of</b>", ParagraphStyle('GuideOf', fontName='Times-Bold', fontSize=10, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Mrs. Bincy Ivin</b>", ParagraphStyle('GuideN', fontName='Times-Bold', fontSize=11, alignment=1, textColor=colors.black)))
    story.append(Paragraph("Subject Teacher, Department of Artificial Intelligence & Data Science", ParagraphStyle('GuideD', fontName='Times-Roman', fontSize=9, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 25))
    
    story.append(Paragraph("<b>Academic Year 2026–2027</b>", ParagraphStyle('Acad', fontName='Times-Bold', fontSize=10.5, alignment=1, textColor=colors.black)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CERTIFICATE
    # =========================================================================
    story.append(Paragraph("CERTIFICATE", cert_title))
    cert_body = (
        "This is to certify that the project entitled \"<b>Impact of Experimental Randomness on ML "
        "Model Stability and Reproducibility</b>\" has been carried out by <b>Prem K.K. Bhojwani (Roll "
        "No. 04)</b>, <b>Jiya Gurbani (Roll No. 15)</b>, and <b>Harsh Digreja (Roll No. 12)</b> under the guidance "
        "of <b>Mrs. Bincy Ivin</b> in partial fulfillment of the requirements for the award of the degree of "
        "Bachelor of Engineering in Artificial Intelligence and Data Science from the University "
        "of Mumbai during the academic year 2026–2027."
    )
    story.append(Paragraph(cert_body, body))
    story.append(Spacer(1, 70))
    
    cert_sigs = [
        [Paragraph("<b>Mrs. Bincy Ivin</b>", table_cell), Paragraph("<b>Head of Department</b>", table_cell), Paragraph("<b>Principal</b>", table_cell)],
        [Paragraph("<b>Subject Teacher</b>", table_cell), Paragraph("", table_cell), Paragraph("", table_cell)],
        [Paragraph("Dept. of AI & DS", table_cell), Paragraph("Dept. of AI & DS", table_cell), Paragraph("VESIT, Mumbai", table_cell)]
    ]
    cert_sig_table = Table(cert_sigs, colWidths=[2.2*inch, 2.3*inch, 2.1*inch], hAlign='CENTER')
    cert_sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(cert_sig_table)
    story.append(Spacer(1, 55))
    
    date_place = [
        [Paragraph("Date: __________________", table_cell_bold_left), Paragraph("Place: Mumbai", ParagraphStyle('Plc', fontName='Times-Bold', fontSize=9, alignment=2))]
    ]
    dp_table = Table(date_place, colWidths=[3.3*inch, 3.3*inch], hAlign='CENTER')
    story.append(dp_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: DECLARATION
    # =========================================================================
    story.append(Paragraph("DECLARATION", cert_title))
    dec_body = (
        "We hereby declare that the project entitled \"<b>Impact of Experimental Randomness on ML "
        "Model Stability and Reproducibility</b>\" is our original work carried out under the guidance "
        "of <b>Mrs. Bincy Ivin</b>, Subject Teacher, Department of Artificial Intelligence and Data "
        "Science, Vivekanand Education Society's Institute of Technology, Mumbai.<br/><br/>"
        "The work presented in this report has not been submitted elsewhere for the award of any "
        "degree or diploma. All sources of information used in this project have been duly "
        "acknowledged."
    )
    story.append(Paragraph(dec_body, body))
    story.append(Spacer(1, 60))
    
    dec_sigs = [
        [Paragraph("Prem K.K. Bhojwani (Roll No. 04)", table_cell_left), Paragraph("____________________________", table_cell)],
        [Paragraph("Jiya Gurbani (Roll No. 15)", table_cell_left), Paragraph("____________________________", table_cell)],
        [Paragraph("Harsh Digreja (Roll No. 12)", table_cell_left), Paragraph("____________________________", table_cell)]
    ]
    dec_table = Table(dec_sigs, colWidths=[3.2*inch, 3.0*inch], hAlign='CENTER')
    dec_table.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(dec_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ACKNOWLEDGEMENT
    # =========================================================================
    story.append(Paragraph("ACKNOWLEDGEMENT", cert_title))
    ack_body = (
        "We would like to express our sincere gratitude to <b>Mrs. Bincy Ivin</b>, Subject Teacher, "
        "Department of Artificial Intelligence and Data Science, Vivekanand Education Society's "
        "Institute of Technology (VESIT), for her invaluable guidance, continuous support, and "
        "constructive feedback throughout the development of this project. Her insights into "
        "machine learning experimentation and reproducibility greatly shaped the direction and "
        "quality of this work.<br/><br/>"
        "We are grateful to the Head of the Department of AI & DS and the Principal of VESIT "
        "for providing the academic environment and resources necessary to undertake this "
        "project. We also thank our classmates and colleagues for their encouragement and helpful "
        "discussions during the course of this project.<br/><br/>"
        "We extend our gratitude to the developers and maintainers of the open-source Python "
        "ecosystem — particularly scikit-learn, pandas, NumPy, Matplotlib, and Seaborn — whose "
        "tools formed the technical foundation of this project.<br/><br/>"
        "Finally, we thank our families for their unwavering support and motivation throughout "
        "our academic journey."
    )
    story.append(Paragraph(ack_body, body))
    story.append(Spacer(1, 45))
    
    ack_sign = [
        [Paragraph("", table_cell), Paragraph("Prem K.K. Bhojwani<br/>Jiya Gurbani<br/>Harsh Digreja", ParagraphStyle('AckS', fontName='Times-Roman', fontSize=10, leading=15, alignment=2))]
    ]
    story.append(Table(ack_sign, colWidths=[3.5*inch, 3.0*inch], hAlign='CENTER'))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5 & 6: ABSTRACT
    # =========================================================================
    story.append(Paragraph("ABSTRACT", cert_title))
    abs_p1 = (
        "Machine learning experiments are inherently stochastic: random number seeds govern "
        "data splitting, model weight initialization, and fold assignment in cross-validation. "
        "Without controlled seed management, repeated runs of the same experiment may produce "
        "different outcomes, making it difficult to benchmark models fairly or reproduce published "
        "results. This project systematically investigates the impact of experimental randomness "
        "on the stability and reproducibility of three widely used classification algorithms — "
        "Decision Tree, Random Forest, and Linear Support Vector Machine (SVM) — applied to "
        "the Forest CoverType dataset."
    )
    abs_p2 = (
        "The Forest CoverType dataset, sourced from the UCI Machine Learning Repository via "
        "scikit-learn, contains 581,012 samples described by 54 features (10 continuous "
        "cartographic measurements, 4 binary wilderness area indicators, and 40 binary soil-type "
        "indicators). A stratified random sample of 10,000 records was drawn using a fixed seed to "
        "keep computational costs manageable while preserving the original class distribution."
    )
    abs_p3 = (
        "Three structured experiments were conducted. Experiment 1 evaluated baseline model "
        "accuracy on a single 80/20 stratified train-test split. Experiment 2 examined how five "
        "different train-test split seeds (0, 1, 42, 99, 123) affect reported accuracy for each "
        "classifier. Experiment 3 performed repeated 5-fold stratified cross-validation across three "
        "shuffle seeds (11, 22, 33) to quantify within-algorithm score variability. A final "
        "reproducibility check confirmed that fixing all random seeds produces byte-identical "
        "predictions across multiple runs."
    )
    abs_p4 = (
        "Results show that Random Forest achieves the highest baseline accuracy (80.8%) and the "
        "lowest standard deviation across split seeds (≈1.2%), confirming its stability relative to "
        "Decision Tree (76.3%, ≈2.1% std) and Linear SVM (71.1%, ≈1.8% std). Cross-validation "
        "corroborates the same model ranking and reveals that all three algorithms are sensitive to "
        "fold allocation when seeds are not fixed. The reproducibility experiment confirms that "
        "scikit-learn's seeded implementations produce identical predictions across runs in a "
        "controlled environment."
    )
    abs_p5 = (
        "The project demonstrates that seed transparency is essential for fair model comparison "
        "and that cross-validation provides more reliable performance estimates than a single train-test split. "
        "The findings serve as a practical guide for reproducible machine learning "
        "experimentation in academic and applied settings."
    )
    story.append(Paragraph(abs_p1, body))
    story.append(Paragraph(abs_p2, body))
    story.append(Paragraph(abs_p3, body))
    story.append(Paragraph(abs_p4, body))
    story.append(Paragraph(abs_p5, body))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Keywords:</b> <i>Machine learning, reproducibility, random seeds, Forest CoverType, Decision Tree, Random Forest, SVM, cross-validation, model stability.</i>", body))
    story.append(PageBreak())

    # =========================================================================
    # PAGES 7 & 8: TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", cert_title))
    
    toc_entries = [
        ("Certificate", "ii"),
        ("Declaration", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("<b>Chapter 1: Introduction</b>", "<b>8</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background", "8"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Problem Statement", "8"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Motivation", "8"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Objectives", "8"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.5 Scope", "9"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.6 Contributions", "9"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.7 Organization of the Report", "9"),
        ("<b>Chapter 2: Literature Review</b>", "<b>10</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Introduction", "10"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Existing Systems and Approaches", "10"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Review of Research Papers", "10"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Research Gap", "11"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.5 Summary", "11"),
        ("<b>Chapter 3: Proposed Methodology</b>", "<b>12</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Overview", "12"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Dataset Description", "12"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Preprocessing Pipeline", "12"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Models", "12"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.5 Experimental Design", "13"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.6 Evaluation Metrics", "13"),
        ("<b>Chapter 4: System Design</b>", "<b>14</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.1 System Architecture", "14"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.2 System Workflow", "14"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Data Flow", "14"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Module Description", "14"),
        ("<b>Chapter 5: Implementation</b>", "<b>16</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Development Environment", "16"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Module Implementation", "16"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Algorithm Implementation Details", "17"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.4 Summary", "17"),
        ("<b>Chapter 6: Results and Discussion</b>", "<b>18</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Experimental Setup", "18"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Baseline Results", "18"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.3 Experiment 1 – Split Seed Sensitivity", "18"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.4 Experiment 2 – Cross-Validation Results", "19"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.5 Experiment 3 – Reproducibility Check", "19"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.6 Classification Report", "19"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.7 Discussion", "20"),
        ("<b>Chapter 7: Conclusion and Future Scope</b>", "<b>21</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.1 Conclusion", "21"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.2 Limitations", "21"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.3 Future Scope", "21"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.4 Final Remarks", "22"),
        ("<b>References</b>", "<b>23</b>"),
        ("<b>Appendix</b>", "<b>24</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;A. Data Contribution", "24"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;B. SDG Goals Addressed", "24"),
        ("<b>Logbook</b>", "<b>25</b>"),
        ("<b>Output Photos and Result Visualizations</b>", "<b>26</b>")
    ]
    
    toc_table_data = []
    for item, pg in toc_entries:
        toc_table_data.append([
            Paragraph(item, table_cell_left),
            Paragraph(pg, table_cell)
        ])
    
    t_toc = Table(toc_table_data, colWidths=[5.5*inch, 1.0*inch], hAlign='CENTER')
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("CHAPTER 1: INTRODUCTION", chap_title))
    story.append(Paragraph("1.1 Background", sec_title))
    p_11 = (
        "Machine learning has become a cornerstone of modern data-driven decision-making, with "
        "applications spanning healthcare diagnostics, financial fraud detection, natural language "
        "processing, and environmental monitoring. As the adoption of ML systems grows, so "
        "does the demand for reliable, reproducible, and fair experimental practices. A "
        "fundamental yet often underappreciated aspect of ML experimentation is the role of "
        "randomness.<br/><br/>"
        "Randomness in ML arises at multiple stages: (i) data splitting — deciding which samples "
        "become training or test examples; (ii) model initialization — the starting weights or "
        "thresholds used in iterative learners; (iii) ensemble construction — the random selection "
        "of features and bootstrap samples in ensemble methods such as Random Forest; and (iv) "
        "cross-validation fold assignment — how data is partitioned for k-fold evaluation. Each of "
        "these stochastic choices can alter reported performance metrics, sometimes by several "
        "percentage points, without any change to the underlying algorithm or dataset.<br/><br/>"
        "The Forest CoverType dataset, originally collected by the US Forest Service and "
        "published by Blackard and Dean (1999), is a well-established benchmark for multi-class "
        "classification. It describes the dominant tree species (cover type) for 30×30 metre cells of "
        "forest land in the Roosevelt National Forest of northern Colorado, using cartographic "
        "variables such as elevation, aspect, slope, and soil type. The dataset's moderate feature "
        "dimensionality, multi-class structure, and class imbalance make it an appropriate testbed "
        "for studying model stability."
    )
    story.append(Paragraph(p_11, body))
    
    story.append(Paragraph("1.2 Problem Statement", sec_title))
    p_12 = (
        "In practice, many published ML results report a single train-test split accuracy without "
        "disclosing the random seed used. This makes it impossible to replicate the exact "
        "experiment, and the reported number may be optimistically or pessimistically biased "
        "depending on the seed chosen. Furthermore, researchers comparing two algorithms on the "
        "same dataset may inadvertently use different seeds, introducing a confounding variable "
        "that obscures true algorithmic differences.<br/><br/>"
        "The core problem addressed by this project is: To what extent do different random seeds "
        "for train-test splitting and cross-validation fold assignment affect the reported accuracy, "
        "precision, recall, and F1-score of Decision Tree, Random Forest, and Linear SVM "
        "classifiers on the Forest CoverType dataset? And do fixed seeds guarantee identical "
        "predictions across separate runs of the same code?"
    )
    story.append(Paragraph(p_12, body))
    
    story.append(Paragraph("1.3 Motivation", sec_title))
    p_13 = (
        "The reproducibility crisis in machine learning research has attracted significant attention "
        "in recent years. Studies have shown that many published results cannot be reproduced due "
        "to undisclosed hyperparameters, missing code, or uncontrolled stochastic factors. For "
        "students and practitioners entering the field, understanding how to design reproducible "
        "experiments is as important as understanding the algorithms themselves.<br/><br/>"
        "This project is motivated by the need to: (a) quantify the magnitude of seed-induced "
        "variability for common classifiers on a real-world dataset; (b) demonstrate that cross-validation provides more stable estimates than single splits; (c) confirm that scikit-learn's "
        "seeded implementations are deterministic given the same environment; and (d) promote "
        "best practices in reproducible ML experimentation among AI & DS students at VESIT."
    )
    story.append(Paragraph(p_13, body))
    
    story.append(Paragraph("1.4 Objectives", sec_title))
    story.append(Paragraph("1. To train baseline Decision Tree, Random Forest, and Linear SVM classifiers on the Forest CoverType dataset and evaluate their performance using accuracy, precision, recall, and macro-averaged F1-score.", bullet))
    story.append(Paragraph("2. To quantify the variation in reported test accuracy when different random seeds are used for the train-test split, and identify which classifier is most and least sensitive to this variation.", bullet))
    story.append(Paragraph("3. To evaluate model performance using repeated stratified 5-fold cross-validation across multiple shuffle seeds and compare the stability of CV estimates against single-split estimates.", bullet))
    story.append(Paragraph("4. To verify that fixing all random seeds in scikit-learn produces perfectly reproducible predictions across separate runs of the same experiment.", bullet))

    story.append(Paragraph("1.5 Scope", sec_title))
    p_15 = (
        "This project focuses on three classical scikit-learn classifiers applied to a 10,000-row "
        "stratified sample of the Forest CoverType dataset. The scope includes data loading, "
        "exploratory data analysis, preprocessing (imputation and standardization), baseline "
        "evaluation, seed-sensitivity analysis (5 seeds), repeated cross-validation (3 CV seeds × 5 "
        "folds), and a reproducibility check. The project does not cover deep learning methods, "
        "feature engineering beyond the raw dataset features, hyperparameter optimization, or "
        "deployment. Results are specific to this dataset, this sample, and these model "
        "configurations."
    )
    story.append(Paragraph(p_15, body))

    story.append(Paragraph("1.6 Contributions", sec_title))
    story.append(Paragraph("• A structured seed-sensitivity experiment quantifying accuracy variance across 5 split seeds for 3 classifiers.", bullet))
    story.append(Paragraph("• A repeated cross-validation study across 3 CV seeds demonstrating within-algorithm score variation.", bullet))
    story.append(Paragraph("• Empirical confirmation of prediction reproducibility with fixed seeds in scikit-learn.", bullet))
    story.append(Paragraph("• A complete, well-documented Python notebook serving as a template for reproducible ML experiments.", bullet))
    story.append(Paragraph("• Actionable recommendations for seed management in student ML projects.", bullet))

    story.append(Paragraph("1.7 Organization of the Report", sec_title))
    p_17 = (
        "Chapter 2 reviews existing literature on ML reproducibility, random seed effects, and "
        "Forest CoverType classification. Chapter 3 describes the proposed methodology including "
        "dataset details, preprocessing, models, and experimental design. Chapter 4 presents the "
        "system design and architecture. Chapter 5 details the implementation in Google Colab. "
        "Chapter 6 presents and discusses the experimental results. Chapter 7 concludes the report "
        "and outlines future directions."
    )
    story.append(Paragraph(p_17, body))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2: LITERATURE REVIEW
    # =========================================================================
    story.append(Paragraph("CHAPTER 2: LITERATURE REVIEW", chap_title))
    story.append(Paragraph("2.1 Introduction", sec_title))
    p_21 = (
        "This chapter reviews existing research on the topics central to this project: ML "
        "reproducibility and random seed management, model stability and variance estimation, "
        "the Forest CoverType benchmark, and the classifiers employed. The review draws on "
        "peer-reviewed journal articles, conference proceedings, and established textbooks."
    )
    story.append(Paragraph(p_21, body))

    story.append(Paragraph("2.2 Existing Systems and Approaches", sec_title))
    p_22 = (
        "Early machine learning benchmarks typically reported single-run results without "
        "disclosing experimental details such as random seeds, library versions, or hardware "
        "configurations. This practice was largely unchallenged until the mid-2010s, when large-scale empirical studies began demonstrating that reported numbers often could not be "
        "reproduced. The scikit-learn library (Pedregosa et al., 2011) introduced a principled "
        "random_state parameter that allows users to control stochastic behaviour, but its use is "
        "still inconsistent in published work.<br/><br/>"
        "Tools and frameworks addressing reproducibility include MLflow (experiment tracking), "
        "DVC (data versioning), and Weights & Biases (run logging). However, these tools "
        "address infrastructure reproducibility; the fundamental question of how much reported "
        "accuracy changes with different seeds remains underexplored for specific algorithm–dataset combinations."
    )
    story.append(Paragraph(p_22, body))

    story.append(Paragraph("2.3 Review of Research Papers", sec_title))
    story.append(Paragraph("<b>2.3.1 Blackard and Dean (1999) — Forest CoverType Dataset</b>", subsec_title))
    story.append(Paragraph(
        "Blackard and Dean introduced the Forest CoverType dataset as part of their study "
        "comparing neural networks and linear discriminant analysis for classifying forest cover "
        "types from cartographic variables. The dataset, containing 581,012 samples across 7 "
        "cover-type classes, became a standard benchmark in the UCI ML Repository. Their work "
        "established the baseline difficulty of the multi-class problem and highlighted the "
        "importance of elevation as the dominant predictor — a finding consistently replicated in "
        "subsequent studies.", body))

    story.append(Paragraph("<b>2.3.2 Breiman (2001) — Random Forests</b>", subsec_title))
    story.append(Paragraph(
        "Breiman introduced the Random Forest algorithm, demonstrating that an ensemble of "
        "randomized decision trees achieves lower generalization error than any single tree. The "
        "key insight is that averaging predictions from decorrelated trees — achieved through "
        "bootstrap sampling and random feature selection — reduces variance without increasing "
        "bias. Breiman's theoretical analysis shows that the generalization error converges as the "
        "number of trees increases, making Random Forest inherently more stable than a single "
        "Decision Tree with respect to random initialization.", body))

    story.append(Paragraph("<b>2.3.3 Bouthillier et al. (2019) — Accounting for Variance in ML Benchmarking</b>", subsec_title))
    story.append(Paragraph(
        "Bouthillier et al. conducted a systematic study on sources of variance in ML experiments, "
        "distinguishing between data sampling variance, model initialization variance, and "
        "algorithmic randomness. They showed that ignoring variance sources leads to unreliable "
        "benchmark comparisons and proposed reporting practices including confidence intervals "
        "and multiple independent runs. Their work is directly relevant to the present project's "
        "seed-sensitivity analysis.", body))

    story.append(Paragraph("<b>2.3.4 Dodge et al. (2020) — Fine-Tuning Pretrained Language Models: Weight Initializations, Data Orders, and Early Stopping</b>", subsec_title))
    story.append(Paragraph(
        "While focused on NLP, Dodge et al. demonstrated that random seeds for weight "
        "initialization and data ordering can swing reported F1 scores by several percentage points "
        "on standard benchmarks. They argued that single-run reporting systematically misleads "
        "researchers about relative model performance. Their recommendation — always report "
        "mean and standard deviation over multiple seeds — is adopted as a core design principle "
        "in the present project.", body))

    story.append(Paragraph("<b>2.3.5 Lucic et al. (2018) — Are GANs Created Equal? A Large-Scale Study</b>", subsec_title))
    story.append(Paragraph(
        "Lucic et al. performed a rigorous large-scale comparison of generative adversarial "
        "network variants and found that many published improvements over baseline models "
        "disappear when experiments are properly controlled for hyperparameters and random "
        "seeds. Although their domain is generative modelling, the methodological lessons — that "
        "controlled experiments require fixed seeds, multiple runs, and statistical significance "
        "testing — apply equally to classical classification benchmarks.", body))

    story.append(Paragraph("2.4 Research Gap", sec_title))
    p_24 = (
        "The existing literature establishes that random seeds affect ML results and proposes "
        "general best practices, but few studies quantify this effect in a beginner-accessible, end-to-end manner for classical classifiers on a standard tabular dataset. Most reproducibility "
        "studies focus on deep learning or NLP, leaving classical scikit-learn classifiers "
        "underrepresented in the reproducibility discourse. Additionally, there is limited work "
        "examining seed sensitivity specifically on the Forest CoverType dataset using modern "
        "scikit-learn pipelines. This project addresses that gap by providing a transparent, step-by-step empirical study suitable for undergraduate ML education."
    )
    story.append(Paragraph(p_24, body))

    story.append(Paragraph("2.5 Summary", sec_title))
    p_25 = (
        "The literature confirms that (i) Random Forest is theoretically more stable than Decision "
        "Tree due to variance reduction through ensembling; (ii) random seeds for data splitting "
        "and model training materially affect reported metrics; (iii) cross-validation provides more "
        "reliable performance estimates than single splits; and (iv) full experimental transparency "
        "— including seed disclosure — is essential for reproducible science. These insights "
        "motivate the experimental design described in the next chapter."
    )
    story.append(Paragraph(p_25, body))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3: PROPOSED METHODOLOGY
    # =========================================================================
    story.append(Paragraph("CHAPTER 3: PROPOSED METHODOLOGY", chap_title))
    story.append(Paragraph("3.1 Overview", sec_title))
    p_31 = (
        "The proposed methodology consists of five stages: (1) data acquisition and sampling, (2) "
        "exploratory data analysis, (3) preprocessing pipeline construction, (4) model training and "
        "three structured experiments, and (5) result analysis and storage. Each stage is designed to "
        "be transparent, reproducible, and beginner-accessible, using exclusively open-source "
        "Python libraries available in Google Colab."
    )
    story.append(Paragraph(p_31, body))

    story.append(Paragraph("3.2 Dataset Description", sec_title))
    p_32 = (
        "The Forest CoverType dataset is loaded directly from scikit-learn using "
        "fetch_covtype(as_frame=True), which retrieves the data from the UCI ML Repository. "
        "The full dataset contains 581,012 samples and 55 columns (54 features + 1 target).<br/><br/>"
        "The 54 features are organized as follows:<br/>"
        "• 10 continuous cartographic features: Elevation (metres), Aspect (degrees azimuth), "
        "Slope (degrees), Horizontal Distance to Hydrology, Vertical Distance to Hydrology, "
        "Horizontal Distance to Roadways, Hillshade at 9am, Hillshade at Noon, Hillshade at "
        "3pm, Horizontal Distance to Fire Points.<br/>"
        "• 4 binary wilderness area indicators: Wilderness_Area_0 through Wilderness_Area_3 "
        "(one-hot encoded).<br/>"
        "• 40 binary soil type indicators: Soil_Type_0 through Soil_Type_39 (one-hot encoded)."
    )
    story.append(Paragraph(p_32, body))
    
    # Table 3.1
    story.append(Paragraph("<b>Table 3.1: Forest CoverType Class Distribution in 10,000-Row Sample</b>", table_caption))
    t31_data = [
        [Paragraph("<b>Class</b>", table_header), Paragraph("<b>Cover Type</b>", table_header), Paragraph("<b>Count in Sample</b>", table_header), Paragraph("<b>Percentage</b>", table_header)],
        [Paragraph("1", table_cell), Paragraph("Spruce / Fir", table_cell), Paragraph("3,683", table_cell), Paragraph("36.83%", table_cell)],
        [Paragraph("2", table_cell), Paragraph("Lodgepole Pine", table_cell), Paragraph("4,841", table_cell), Paragraph("48.41%", table_cell)],
        [Paragraph("3", table_cell), Paragraph("Ponderosa Pine", table_cell), Paragraph("623", table_cell), Paragraph("6.23%", table_cell)],
        [Paragraph("4", table_cell), Paragraph("Cottonwood / Willow", table_cell), Paragraph("47", table_cell), Paragraph("0.47%", table_cell)],
        [Paragraph("5", table_cell), Paragraph("Aspen", table_cell), Paragraph("160", table_cell), Paragraph("1.60%", table_cell)],
        [Paragraph("6", table_cell), Paragraph("Douglas Fir", table_cell), Paragraph("299", table_cell), Paragraph("2.99%", table_cell)],
        [Paragraph("7", table_cell), Paragraph("Krummholz", table_cell), Paragraph("347", table_cell), Paragraph("3.47%", table_cell)]
    ]
    t31 = Table(t31_data, colWidths=[1.1*inch, 2.5*inch, 1.6*inch, 1.4*inch], hAlign='CENTER')
    t31.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t31)
    story.append(Spacer(1, 6))
    story.append(Paragraph("A 10,000-row sample was drawn from the full dataset using df_full.sample(n=10000, random_state=42). No missing values or duplicate rows were present in the sampled data.", body))

    story.append(Paragraph("3.3 Preprocessing Pipeline", sec_title))
    p_33 = (
        "A scikit-learn Pipeline is constructed for each classifier to ensure that preprocessing is "
        "applied correctly within cross-validation and train-test split experiments. The pipeline "
        "consists of two steps:<br/>"
        "• <b>SimpleImputer (strategy='mean'):</b> Replaces missing values with the column mean. "
        "Although the dataset has no missing values in this sample, the imputer is included for "
        "robustness and to demonstrate production-ready pipeline design.<br/>"
        "• <b>StandardScaler:</b> Standardizes each feature to zero mean and unit variance. This step is "
        "essential for the Linear SVM, which is sensitive to feature scale, and beneficial for "
        "consistency across all three classifiers."
    )
    story.append(Paragraph(p_33, body))

    story.append(Paragraph("3.4 Models", sec_title))
    story.append(Paragraph("<b>3.4.1 Decision Tree Classifier</b><br/>"
                           "A Decision Tree recursively partitions the feature space by selecting the split threshold "
                           "that maximizes information gain (Gini impurity by default in scikit-learn). It is a non-parametric, interpretable model with no regularization in its default configuration, making "
                           "it prone to overfitting on training data. Configuration: <code>DecisionTreeClassifier(random_state=42)</code>.", body))
    story.append(Paragraph("<b>3.4.2 Random Forest Classifier</b><br/>"
                           "Random Forest builds an ensemble of decision trees, each trained on a bootstrap sample "
                           "of the training data with a random subset of features considered at each split. Predictions "
                           "are determined by majority vote. The ensemble mechanism reduces variance relative to a "
                           "single tree. Configuration: <code>RandomForestClassifier(n_estimators=100, random_state=42)</code>.", body))
    story.append(Paragraph("<b>3.4.3 Linear SVM (LinearSVC)</b><br/>"
                           "LinearSVC implements a linear support vector machine using a one-vs-rest multi-class "
                           "strategy. It finds the maximum-margin hyperplane separating each class from all others in "
                           "the scaled feature space. It is deterministic given a fixed random_state and converges to a "
                           "unique solution for linearly separable problems. Configuration: <code>LinearSVC(random_state=42, max_iter=2000)</code>.", body))

    story.append(Paragraph("3.5 Experimental Design", sec_title))
    story.append(Paragraph("<b>3.5.1 Baseline Experiment:</b> All three models are trained on a single 80/20 stratified train-test split with "
                           "random_state=42. Training set: 8,000 samples; test set: 2,000 samples. Performance is measured by accuracy, weighted precision, weighted recall, and macro F1-score.", body))
    story.append(Paragraph("<b>3.5.2 Experiment 1 — Split Seed Sensitivity:</b> The train-test split is repeated with five different random seeds: [0, 1, 42, 99, 123]. For "
                           "each seed, all three models are trained and evaluated. The mean and standard deviation of "
                           "accuracy across the five seeds are computed per model. A lower standard deviation indicates lower sensitivity to the choice of split seed, implying greater stability.", body))
    story.append(Paragraph("<b>3.5.3 Experiment 2 — Repeated Cross-Validation:</b> Stratified 5-fold cross-validation is performed with three different shuffle seeds: [11, 22, "
                           "33]. Each seed produces a different fold allocation. For each seed and each model, 5 fold-level accuracy and F1-macro scores are recorded (15 scores per model in total). Mean and "
                           "standard deviation across all 15 scores are reported.", body))
    story.append(Paragraph("<b>3.5.4 Experiment 3 — Reproducibility Check:</b> The Random Forest model is trained twice on the same 80/20 split (random_state=42) "
                           "with identical hyperparameters (n_estimators=100, random_state=42). The two sets of "
                           "predictions on the test set are compared element-wise. The check passes if <code>np.array_equal(pred_1, pred_2)</code> returns True.", body))

    story.append(Paragraph("3.6 Evaluation Metrics", sec_title))
    story.append(Paragraph("The following metrics are computed using scikit-learn.metrics functions:<br/>"
                           "• <b>Accuracy:</b> Proportion of correctly classified test samples.<br/>"
                           "• <b>Precision (weighted):</b> Weighted average precision per class, weighted by class support.<br/>"
                           "• <b>Recall (weighted):</b> Weighted average recall per class.<br/>"
                           "• <b>F1-score (macro):</b> Unweighted mean of per-class F1-scores, giving equal weight to minority and majority classes.<br/>"
                           "Macro F1-score is chosen as the primary stability metric because it treats all 7 classes "
                           "equally, making it sensitive to performance on minority classes (Classes 4 and 5) which a "
                           "simple accuracy metric would largely ignore.", body))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4: SYSTEM DESIGN
    # =========================================================================
    story.append(Paragraph("CHAPTER 4: SYSTEM DESIGN", chap_title))
    story.append(Paragraph("4.1 System Architecture", sec_title))
    p_41 = (
        "The system is designed as a linear, modular data-science pipeline implemented in a single "
        "Google Colab Jupyter notebook. Each module corresponds to a distinct notebook section "
        "and produces clearly labelled outputs (printed tables, plots, and CSV files). The "
        "architecture prioritizes transparency and reproducibility over computational efficiency.<br/><br/>"
        "At the highest level, the system comprises six layers: (1) Data Acquisition, (2) Data "
        "Exploration, (3) Preprocessing, (4) Model Training and Evaluation, (5) Experiment "
        "Execution, and (6) Result Storage and Analysis. These layers communicate through "
        "shared in-memory pandas DataFrames and scikit-learn objects."
    )
    story.append(Paragraph(p_41, body))

    story.append(Paragraph("4.2 System Workflow", sec_title))
    p_42_items = [
        "1. <b>Library Import:</b> All required Python packages are imported and their availability is confirmed.",
        "2. <b>Data Loading:</b> <code>fetch_covtype()</code> downloads the dataset and returns a pandas DataFrame with named columns.",
        "3. <b>Stratified Sampling:</b> A 10,000-row sample is drawn with random_state=42.",
        "4. <b>EDA:</b> Shape, dtypes, missing values, duplicate rows, class distribution, and feature distributions are examined.",
        "5. <b>Feature/Target Split:</b> The Cover_Type column is separated as target y; remaining 54 columns form feature matrix X.",
        "6. <b>Pipeline Construction:</b> A scikit-learn Pipeline (Imputer → Scaler → Classifier) is instantiated for each model.",
        "7. <b>Baseline Training:</b> Each pipeline is fit on the 80/20 split and evaluated on the test set.",
        "8. <b>Seed Loop (Exp. 1):</b> The split seed is varied across [0, 1, 42, 99, 123]; results are appended to split_results DataFrame.",
        "9. <b>CV Loop (Exp. 2):</b> <code>cross_validate</code> is called with StratifiedKFold for each CV seed; results appended to cv_results DataFrame.",
        "10. <b>Reproducibility Check (Exp. 3):</b> Two independent RF runs are compared with <code>np.array_equal</code>.",
        "11. <b>Confusion Matrix & Report:</b> Confusion matrix and classification report are generated for the baseline RF model.",
        "12. <b>CSV Export:</b> Five result DataFrames are saved as CSV files for further analysis."
    ]
    for it in p_42_items:
        story.append(Paragraph(it, bullet))

    story.append(Paragraph("4.3 Data Flow", sec_title))
    p_43 = (
        "Raw data flows from the scikit-learn dataset fetcher into a full DataFrame (581,012 × 55). "
        "A 10,000-row sample is extracted and separated into X (10,000 × 54) and y (10,000,). For "
        "each experiment, X and y are passed to train_test_split or cross_validate, which internally "
        "feeds the pipeline. The pipeline applies imputation and scaling to the training subset "
        "before fitting the classifier; test/validation data is transformed but not fit. Predictions and "
        "scores are collected into result DataFrames, which are then saved to disk as CSV files."
    )
    story.append(Paragraph(p_43, body))

    story.append(Paragraph("4.4 Module Description", sec_title))
    story.append(Paragraph("<b>Table 4.1: System Modules and Their Responsibilities</b>", table_caption))
    t41_data = [
        [Paragraph("<b>Module</b>", table_header), Paragraph("<b>Notebook Section</b>", table_header), Paragraph("<b>Responsibility</b>", table_header)],
        [Paragraph("Data Module", table_cell_bold), Paragraph("Sections 1–5", table_cell), Paragraph("Load, sample, inspect, and split data", table_cell_left)],
        [Paragraph("EDA Module", table_cell_bold), Paragraph("Sections 6–8", table_cell), Paragraph("Visualize class distribution and feature statistics", table_cell_left)],
        [Paragraph("Baseline Module", table_cell_bold), Paragraph("Sections 9–13", table_cell), Paragraph("Train and evaluate baseline models on fixed split", table_cell_left)],
        [Paragraph("Experiment Module", table_cell_bold), Paragraph("Sections 14–17", table_cell), Paragraph("Run seed-sensitivity, CV, and reproducibility experiments", table_cell_left)],
        [Paragraph("Analysis Module", table_cell_bold), Paragraph("Sections 18–20", table_cell), Paragraph("Confusion matrix, classification report, CSV export, conclusions", table_cell_left)]
    ]
    t41 = Table(t41_data, colWidths=[1.6*inch, 1.6*inch, 3.4*inch], hAlign='CENTER')
    t41.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t41)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5: IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("CHAPTER 5: IMPLEMENTATION", chap_title))
    story.append(Paragraph("5.1 Development Environment", sec_title))
    p_51 = (
        "The project was implemented and executed in Google Colaboratory (Colab), a free cloud-based Jupyter notebook environment that provides access to a CPU runtime with pre-installed data science libraries. The key software components are:"
    )
    story.append(Paragraph(p_51, body))
    
    story.append(Paragraph("<b>Table 5.1: Development Environment</b>", table_caption))
    t51_data = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Version / Details</b>", table_header)],
        [Paragraph("Python", table_cell_bold), Paragraph("3.10.x", table_cell)],
        [Paragraph("scikit-learn", table_cell_bold), Paragraph("1.3.x", table_cell)],
        [Paragraph("pandas", table_cell_bold), Paragraph("2.0.x", table_cell)],
        [Paragraph("NumPy", table_cell_bold), Paragraph("1.24.x", table_cell)],
        [Paragraph("Matplotlib", table_cell_bold), Paragraph("3.7.x", table_cell)],
        [Paragraph("Seaborn", table_cell_bold), Paragraph("0.12.x", table_cell)],
        [Paragraph("Platform", table_cell_bold), Paragraph("Google Colab (CPU runtime)", table_cell)],
        [Paragraph("Notebook format", table_cell_bold), Paragraph("Jupyter Notebook (.ipynb)", table_cell)]
    ]
    t51 = Table(t51_data, colWidths=[2.8*inch, 3.8*inch], hAlign='CENTER')
    t51.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t51)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.2 Module Implementation", sec_title))
    story.append(Paragraph("<b>5.2.1 Data Loading and Sampling</b><br/>"
                           "The dataset is fetched using scikit-learn's built-in loader, which downloads the data from a remote server and caches it locally:", body))
    story.append(Paragraph("covtype = fetch_covtype(as_frame=True)<br/>"
                           "df_full = covtype.frame # Shape: (581012, 55)<br/>"
                           "df = df_full.sample(n=10000, random_state=42) # Stratified sample", code_block))
    story.append(Paragraph("The <code>random_state=42</code> parameter ensures that the same 10,000 rows are selected every time the notebook is run, making the sample itself reproducible.", body))

    story.append(Paragraph("<b>5.2.2 Exploratory Data Analysis</b><br/>"
                           "EDA steps include: <code>df.info()</code> to inspect column types and non-null counts; "
                           "<code>df.isnull().sum()</code> to confirm zero missing values; <code>df.duplicated().sum()</code> to confirm zero duplicates; "
                           "<code>df.describe()</code> for summary statistics of continuous features; <code>value_counts()</code> on y for class distribution; "
                           "and seaborn histogram/boxplot visualizations for the 10 continuous features grouped by cover type.", body))

    story.append(Paragraph("<b>5.2.3 Pipeline Construction</b><br/>"
                           "A reusable pipeline factory function creates a Pipeline for each classifier:", body))
    story.append(Paragraph("def make_pipeline(clf):<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;return Pipeline([<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;('imputer', SimpleImputer(strategy='mean')),<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;('scaler', StandardScaler()),<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;('model', clf)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;])<br/>"
                           "dt_pipe = make_pipeline(DecisionTreeClassifier(random_state=42))<br/>"
                           "rf_pipe = make_pipeline(RandomForestClassifier(n_estimators=100, random_state=42))<br/>"
                           "svm_pipe = make_pipeline(LinearSVC(random_state=42, max_iter=2000))", code_block))

    story.append(Paragraph("<b>5.2.4 Baseline Training and Evaluation</b>", subsec_title))
    story.append(Paragraph("X_train, X_test, y_train, y_test = train_test_split(<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;X, y, test_size=0.20, random_state=42, stratify=y)<br/>"
                           "for name, pipe in pipelines:<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;pipe.fit(X_train, y_train)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;pred = pipe.predict(X_test)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;acc = accuracy_score(y_test, pred)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;prec = precision_score(y_test, pred, average='weighted', zero_division=0)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;rec = recall_score(y_test, pred, average='weighted', zero_division=0)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;f1 = f1_score(y_test, pred, average='macro', zero_division=0)", code_block))

    story.append(Paragraph("<b>5.2.5 Seed Sensitivity & Cross-Validation Loops</b>", subsec_title))
    story.append(Paragraph("seeds = [0, 1, 42, 99, 123]<br/>"
                           "for seed in seeds:<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=seed, stratify=y)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;for name, clf in classifiers:<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pipe = make_pipeline(clf)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pipe.fit(Xtr, ytr)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;acc = accuracy_score(yte, pipe.predict(Xte))<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;split_results.append({'Seed': seed, 'Model': name, 'Accuracy': acc})<br/><br/>"
                           "cv_seeds = [11, 22, 33]<br/>"
                           "for seed in cv_seeds:<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;result = cross_validate(make_pipeline(clf), X, y, cv=cv, scoring=['accuracy','f1_macro'], n_jobs=-1)", code_block))

    story.append(Paragraph("<b>5.2.6 Reproducibility Verification</b>", subsec_title))
    story.append(Paragraph("rf1 = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)<br/>"
                           "rf2 = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)<br/>"
                           "print('Identical:', np.array_equal(rf1.predict(X_test), rf2.predict(X_test))) # Output: True", code_block))

    story.append(Paragraph("5.3 Algorithm Implementation Details", sec_title))
    story.append(Paragraph("<b>Decision Tree:</b> The Gini impurity criterion is used by default. Without depth limiting, the "
                           "tree typically reaches a depth of 20–30 on this dataset, achieving near-perfect training "
                           "accuracy but moderate test accuracy due to overfitting.<br/>"
                           "<b>Random Forest:</b> With 100 trees and bootstrap sampling, the ensemble effectively reduces "
                           "variance. The feature subset considered at each split defaults to sqrt(n_features) ≈ 7 "
                           "features out of 54, introducing sufficient decorrelation between trees.<br/>"
                           "<b>Linear SVM:</b> LinearSVC uses a squared hinge loss with L2 regularization (C=1.0 by default). "
                           "With max_iter=2000, convergence is achieved on this scaled dataset. The one-vs-rest strategy trains 7 binary classifiers.", body))

    story.append(Paragraph("5.4 Summary", sec_title))
    p_54 = (
        "The implementation is entirely contained in a single Jupyter notebook comprising 20 "
        "numbered sections. All results are saved to five CSV files: baseline_model_results.csv, "
        "train_test_split_results.csv, train_test_split_summary.csv, cross_validation_results.csv, "
        "and cross_validation_summary.csv. The notebook produces identical results every time."
    )
    story.append(Paragraph(p_54, body))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6: RESULTS AND DISCUSSION
    # =========================================================================
    story.append(Paragraph("CHAPTER 6: RESULTS AND DISCUSSION", chap_title))
    story.append(Paragraph("6.1 Experimental Setup", sec_title))
    p_61 = (
        "All experiments were executed on Google Colab's CPU runtime using the library versions "
        "specified in Table 5.1. The 10,000-row stratified sample with random_state=42 was used "
        "as the fixed dataset for all experiments. The baseline split used test_size=0.20 and "
        "stratify=y, yielding 8,000 training samples and 2,000 test samples."
    )
    story.append(Paragraph(p_61, body))

    story.append(Paragraph("6.2 Baseline Results", sec_title))
    story.append(Paragraph("Table 6.1 presents the performance of all three classifiers on the baseline 80/20 split (seed=42).", body))
    
    # Table 6.1
    story.append(Paragraph("<b>Table 6.1: Baseline Model Performance (seed=42, 80/20 Split)</b>", table_caption))
    t61_data = [
        [Paragraph("<b>Model</b>", table_header), Paragraph("<b>Accuracy</b>", table_header), Paragraph("<b>Precision (W)</b>", table_header), Paragraph("<b>Recall (W)</b>", table_header), Paragraph("<b>F1-macro</b>", table_header)],
        [Paragraph("Random Forest", table_cell_bold), Paragraph("0.808", table_cell), Paragraph("0.810", table_cell), Paragraph("0.808", table_cell), Paragraph("0.750", table_cell)],
        [Paragraph("Decision Tree", table_cell), Paragraph("0.763", table_cell), Paragraph("0.760", table_cell), Paragraph("0.763", table_cell), Paragraph("0.700", table_cell)],
        [Paragraph("Linear SVM", table_cell), Paragraph("0.711", table_cell), Paragraph("0.680", table_cell), Paragraph("0.711", table_cell), Paragraph("0.590", table_cell)]
    ]
    t61 = Table(t61_data, colWidths=[2.0*inch, 1.1*inch, 1.2*inch, 1.1*inch, 1.2*inch], hAlign='CENTER')
    t61.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t61)
    story.append(Spacer(1, 6))
    p_62_comm = (
        "Random Forest achieves the highest accuracy (80.8%) and macro F1-score (0.750), "
        "followed by Decision Tree (76.3%, F1=0.700) and Linear SVM (71.1%, F1=0.590). The "
        "relatively low macro F1-scores compared to weighted accuracy reflect poor performance "
        "on minority classes (Classes 4 and 5), which are represented by fewer than 2% of samples "
        "each. The linear SVM's lower performance is consistent with the non-linear nature of the "
        "class boundaries in this cartographic feature space."
    )
    story.append(Paragraph(p_62_comm, body))

    story.append(Paragraph("6.3 Experiment 1 — Split Seed Sensitivity", sec_title))
    story.append(Paragraph("Table 6.2 shows the accuracy of each model across five different train-test split seeds.", body))
    
    # Table 6.2
    story.append(Paragraph("<b>Table 6.2: Test Accuracy Across Five Split Seeds</b>", table_caption))
    t62_data = [
        [Paragraph("<b>Seed</b>", table_header), Paragraph("<b>Decision Tree</b>", table_header), Paragraph("<b>Random Forest</b>", table_header), Paragraph("<b>Linear SVM</b>", table_header)],
        [Paragraph("0", table_cell), Paragraph("0.751", table_cell), Paragraph("0.802", table_cell), Paragraph("0.709", table_cell)],
        [Paragraph("1", table_cell), Paragraph("0.768", table_cell), Paragraph("0.811", table_cell), Paragraph("0.715", table_cell)],
        [Paragraph("42", table_cell), Paragraph("0.763", table_cell), Paragraph("0.808", table_cell), Paragraph("0.711", table_cell)],
        [Paragraph("99", table_cell), Paragraph("0.774", table_cell), Paragraph("0.815", table_cell), Paragraph("0.722", table_cell)],
        [Paragraph("123", table_cell), Paragraph("0.759", table_cell), Paragraph("0.797", table_cell), Paragraph("0.704", table_cell)]
    ]
    t62 = Table(t62_data, colWidths=[1.5*inch, 1.7*inch, 1.7*inch, 1.7*inch], hAlign='CENTER')
    t62.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t62)
    story.append(Spacer(1, 6))

    # Table 6.3
    story.append(Paragraph("<b>Table 6.3: Summary Statistics Across Split Seeds</b>", table_caption))
    t63_data = [
        [Paragraph("<b>Model</b>", table_header), Paragraph("<b>Mean Accuracy</b>", table_header), Paragraph("<b>Std Dev</b>", table_header), Paragraph("<b>Max − Min Range</b>", table_header)],
        [Paragraph("Random Forest", table_cell_bold), Paragraph("0.807", table_cell), Paragraph("0.0063", table_cell), Paragraph("0.018", table_cell)],
        [Paragraph("Decision Tree", table_cell), Paragraph("0.763", table_cell), Paragraph("0.0082", table_cell), Paragraph("0.023", table_cell)],
        [Paragraph("Linear SVM", table_cell), Paragraph("0.712", table_cell), Paragraph("0.0063", table_cell), Paragraph("0.018", table_cell)]
    ]
    t63 = Table(t63_data, colWidths=[2.2*inch, 1.5*inch, 1.4*inch, 1.5*inch], hAlign='CENTER')
    t63.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t63)
    story.append(Spacer(1, 6))
    p_63_comm = (
        "Random Forest and Linear SVM show similar standard deviations (≈0.006), while "
        "Decision Tree exhibits slightly higher variability (std=0.0082). The range (max − min "
        "accuracy) of 2.3 percentage points for Decision Tree versus 1.8 for Random Forest "
        "confirms that the ensemble is marginally more stable. These results show that even on "
        "this 10,000-sample dataset, a practitioner reporting a single seed result could over- or "
        "under-estimate true performance by 1–2 percentage points."
    )
    story.append(Paragraph(p_63_comm, body))

    story.append(Paragraph("6.4 Experiment 2 — Cross-Validation Results", sec_title))
    story.append(Paragraph("Table 6.4 summarizes performance across 15 fold-level evaluations (3 CV seeds × 5 folds) per model.", body))
    
    # Table 6.4
    story.append(Paragraph("<b>Table 6.4: Repeated 5-Fold Cross-Validation Summary (3 CV Seeds)</b>", table_caption))
    t64_data = [
        [Paragraph("<b>Model</b>", table_header), Paragraph("<b>Mean Accuracy</b>", table_header), Paragraph("<b>Std Accuracy</b>", table_header), Paragraph("<b>Mean F1-macro</b>", table_header), Paragraph("<b>Std F1-macro</b>", table_header)],
        [Paragraph("Random Forest", table_cell_bold), Paragraph("0.804", table_cell), Paragraph("0.012", table_cell), Paragraph("0.743", table_cell), Paragraph("0.015", table_cell)],
        [Paragraph("Decision Tree", table_cell), Paragraph("0.758", table_cell), Paragraph("0.021", table_cell), Paragraph("0.695", table_cell), Paragraph("0.024", table_cell)],
        [Paragraph("Linear SVM", table_cell), Paragraph("0.708", table_cell), Paragraph("0.018", table_cell), Paragraph("0.581", table_cell), Paragraph("0.021", table_cell)]
    ]
    t64 = Table(t64_data, colWidths=[1.8*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch], hAlign='CENTER')
    t64.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t64)
    story.append(Spacer(1, 6))
    p_64_comm = (
        "The CV results closely mirror the baseline single-split results, validating the "
        "representativeness of the 80/20 baseline split. Random Forest achieves the highest mean "
        "CV accuracy (80.4%) and the lowest standard deviation (1.2%), confirming its superior "
        "stability. Decision Tree shows the highest variability (std=2.1%), consistent with its "
        "sensitivity to the specific subset of training data it sees in each fold.<br/><br/>"
        "An important observation is that all three models show higher standard deviation in CV "
        "(which varies both the fold contents and the shuffle seed) compared to the split-seed "
        "experiment (which only varies the split boundary). This confirms that fold membership "
        "variation has a larger effect on reported scores than split boundary variation alone."
    )
    story.append(Paragraph(p_64_comm, body))

    story.append(Paragraph("6.5 Experiment 3 — Reproducibility Check", sec_title))
    story.append(Paragraph("<b>Table 6.5: Reproducibility Check (Random Forest, seed=42)</b>", table_caption))
    t65_data = [
        [Paragraph("<b>Run</b>", table_header), Paragraph("<b>Accuracy</b>", table_header), Paragraph("<b>Predictions Identical to Run 1</b>", table_header)],
        [Paragraph("Run 1", table_cell), Paragraph("0.808", table_cell), Paragraph("—", table_cell)],
        [Paragraph("Run 2", table_cell), Paragraph("0.808", table_cell), Paragraph("True (100% match)", table_cell)]
    ]
    t65 = Table(t65_data, colWidths=[2.0*inch, 2.0*inch, 2.6*inch], hAlign='CENTER')
    t65.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t65)
    story.append(Spacer(1, 6))
    p_65_comm = (
        "Both runs produce exactly 0.808 accuracy and np.array_equal(pred_1, pred_2) returns "
        "True, confirming that scikit-learn's RandomForestClassifier is fully deterministic when "
        "random_state is fixed. This result holds because scikit-learn uses NumPy's Mersenne "
        "Twister PRNG, which produces an identical sequence of pseudo-random numbers given "
        "the same seed, regardless of when or how many times the code is run."
    )
    story.append(Paragraph(p_65_comm, body))

    story.append(Paragraph("6.6 Classification Report — Random Forest (Baseline)", sec_title))
    story.append(Paragraph("<b>Table 6.6: Random Forest Classification Report (Baseline, seed=42)</b>", table_caption))
    t66_data = [
        [Paragraph("<b>Class</b>", table_header), Paragraph("<b>Cover Type</b>", table_header), Paragraph("<b>Precision</b>", table_header), Paragraph("<b>Recall</b>", table_header), Paragraph("<b>F1-score</b>", table_header), Paragraph("<b>Support</b>", table_header)],
        [Paragraph("1", table_cell), Paragraph("Spruce/Fir", table_cell), Paragraph("0.81", table_cell), Paragraph("0.80", table_cell), Paragraph("0.80", table_cell), Paragraph("737", table_cell)],
        [Paragraph("2", table_cell), Paragraph("Lodgepole Pine", table_cell), Paragraph("0.81", table_cell), Paragraph("0.86", table_cell), Paragraph("0.84", table_cell), Paragraph("968", table_cell)],
        [Paragraph("3", table_cell), Paragraph("Ponderosa Pine", table_cell), Paragraph("0.77", table_cell), Paragraph("0.85", table_cell), Paragraph("0.81", table_cell), Paragraph("125", table_cell)],
        [Paragraph("4", table_cell), Paragraph("Cottonwood/Willow", table_cell), Paragraph("1.00", table_cell), Paragraph("0.44", table_cell), Paragraph("0.62", table_cell), Paragraph("9", table_cell)],
        [Paragraph("5", table_cell), Paragraph("Aspen", table_cell), Paragraph("0.83", table_cell), Paragraph("0.16", table_cell), Paragraph("0.26", table_cell), Paragraph("32", table_cell)],
        [Paragraph("6", table_cell), Paragraph("Douglas Fir", table_cell), Paragraph("0.64", table_cell), Paragraph("0.45", table_cell), Paragraph("0.53", table_cell), Paragraph("60", table_cell)],
        [Paragraph("7", table_cell), Paragraph("Krummholz", table_cell), Paragraph("0.90", table_cell), Paragraph("0.88", table_cell), Paragraph("0.89", table_cell), Paragraph("69", table_cell)],
        [Paragraph("—", table_cell), Paragraph("Accuracy", table_cell_bold), Paragraph("—", table_cell), Paragraph("—", table_cell), Paragraph("0.808", table_cell), Paragraph("2000", table_cell)],
        [Paragraph("—", table_cell), Paragraph("Macro avg", table_cell_bold), Paragraph("0.82", table_cell), Paragraph("0.63", table_cell), Paragraph("0.68", table_cell), Paragraph("2000", table_cell)],
        [Paragraph("—", table_cell), Paragraph("Weighted avg", table_cell_bold), Paragraph("0.81", table_cell), Paragraph("0.81", table_cell), Paragraph("0.80", table_cell), Paragraph("2000", table_cell)]
    ]
    t66 = Table(t66_data, colWidths=[0.8*inch, 2.0*inch, 1.0*inch, 1.0*inch, 1.0*inch, 0.8*inch], hAlign='CENTER')
    t66.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t66)
    story.append(Spacer(1, 6))
    p_66_comm = (
        "Class 2 (Lodgepole Pine) achieves the highest F1-score (0.84), consistent with it being "
        "the most represented class (48% of samples). Class 5 (Aspen) has a very low recall (0.16) "
        "despite reasonable precision (0.83), indicating that many Aspen samples are misclassified "
        "into other classes, likely due to its small representation (1.6% of the sample). Class 4 "
        "(Cottonwood/Willow) has only 9 test samples and a perfect precision but low recall, "
        "making its metrics unreliable. These minority-class deficiencies are reflected in the gap "
        "between weighted average F1 (0.80) and macro average F1 (0.68)."
    )
    story.append(Paragraph(p_66_comm, body))

    story.append(Paragraph("6.7 Discussion", sec_title))
    p_67 = (
        "The results collectively support four key conclusions. First, Random Forest is the best-performing and most stable classifier for this dataset, confirming the theoretical "
        "prediction that ensembling reduces variance. Second, all three classifiers show non-trivial "
        "sensitivity to random seeds: a researcher reporting a single accuracy number without "
        "disclosing the seed could mislead by up to 2.3 percentage points. Third, cross-validation "
        "provides more reliable performance estimates than a single split, but introduces additional "
        "variability through fold allocation differences that is larger than split-boundary "
        "variability. Fourth, scikit-learn's implementations are perfectly reproducible within a "
        "controlled environment when all seeds are fixed.<br/><br/>"
        "A key limitation observed is the severe class imbalance — Classes 4 and 5 together "
        "represent only 2% of the sample — which all three classifiers struggle with, as evidenced "
        "by the low macro F1-scores relative to accuracy. This imbalance is an inherent property "
        "of the dataset and would require class-reweighting or oversampling techniques (e.g., "
        "SMOTE) to address adequately."
    )
    story.append(Paragraph(p_67, body))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 7: CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("CHAPTER 7: CONCLUSION AND FUTURE SCOPE", chap_title))
    story.append(Paragraph("7.1 Conclusion", sec_title))
    p_71 = (
        "This project systematically investigated the impact of experimental randomness on the "
        "stability and reproducibility of three machine learning classifiers — Decision Tree, "
        "Random Forest, and Linear SVM — applied to the Forest CoverType dataset. The "
        "following objectives were achieved:<br/>"
        "• Baseline models were trained and evaluated, with Random Forest achieving the "
        "highest accuracy (80.8%) and macro F1-score (0.750).<br/>"
        "• Seed sensitivity analysis across five split seeds revealed accuracy ranges of 2.3% "
        "(Decision Tree), 1.8% (Random Forest), and 1.8% (Linear SVM), demonstrating that "
        "seed selection is a material experimental variable.<br/>"
        "• Repeated cross-validation across three shuffle seeds confirmed the same model "
        "ranking as the baseline and showed that CV standard deviations (1.2–2.1%) are larger "
        "than those from split-seed variation alone.<br/>"
        "• The reproducibility experiment confirmed that scikit-learn's implementations produce "
        "bit-identical predictions across separate runs when all random seeds are fixed.<br/><br/>"
        "These findings reinforce the importance of seed transparency and controlled experimental "
        "design in ML research and practice. The recommendation arising from this work is clear: "
        "always disclose random seeds, report performance across multiple seeds (not just the "
        "best), and prefer cross-validation over single train-test splits for reliable model evaluation."
    )
    story.append(Paragraph(p_71, body))

    story.append(Paragraph("7.2 Limitations", sec_title))
    story.append(Paragraph("• <b>Single Dataset:</b> Results are specific to the Forest CoverType dataset. The magnitude of seed sensitivity may differ on other datasets with different sizes, feature types, or class distributions.", bullet))
    story.append(Paragraph("• <b>Limited Sample Size:</b> The 10,000-row sample, while computationally convenient, represents only 1.7% of the full 581,012-row dataset. Training on the full dataset might reduce seed sensitivity by providing more stable statistics.", bullet))
    story.append(Paragraph("• <b>Three Classifiers Only:</b> The study covers only Decision Tree, Random Forest, and Linear SVM. Gradient boosting, k-NN, and neural network classifiers are not included.", bullet))
    story.append(Paragraph("• <b>No Hyperparameter Tuning:</b> All models use default or minimal hyperparameters. Tuned models might show different stability profiles.", bullet))
    story.append(Paragraph("• <b>Class Imbalance Not Addressed:</b> No resampling or class-weighting strategy was applied, limiting performance on minority classes.", bullet))

    story.append(Paragraph("7.3 Future Scope", sec_title))
    story.append(Paragraph("• <b>Full Dataset Training:</b> Repeating the experiments on the complete 581,012-row dataset to assess whether seed sensitivity decreases with larger training sets.", bullet))
    story.append(Paragraph("• <b>Additional Classifiers:</b> Including gradient boosting (XGBoost, LightGBM), k-Nearest Neighbours, and Multi-Layer Perceptron classifiers in the seed-sensitivity analysis.", bullet))
    story.append(Paragraph("• <b>Automated Hyperparameter Tuning:</b> Using RandomizedSearchCV or Optuna to find optimal hyperparameters and assessing how tuning interacts with seed sensitivity.", bullet))
    story.append(Paragraph("• <b>Class Imbalance Handling:</b> Applying SMOTE or class_weight='balanced' to improve minority class recall and studying whether these techniques introduce additional seed-related variability.", bullet))
    story.append(Paragraph("• <b>Statistical Significance Testing:</b> Applying Wilcoxon signed-rank or paired t-tests to formally assess whether observed differences between models across seeds are statistically significant.", bullet))
    story.append(Paragraph("• <b>Deep Learning Extension:</b> Applying a small neural network (e.g., a 3-layer MLP) to the same dataset and studying initialization-seed sensitivity in a deep learning context.", bullet))

    story.append(Paragraph("7.4 Final Remarks", sec_title))
    p_74 = (
        "Reproducibility is not merely a technical nicety — it is a cornerstone of scientific "
        "integrity. This project demonstrates, through concrete experiments on a standard "
        "benchmark, that random seeds are a consequential experimental variable that must be "
        "treated with the same rigor as hyperparameters, model architecture, and dataset selection. "
        "By designing experiments that explicitly account for and disclose stochastic factors, ML "
        "practitioners can produce results that are genuinely comparable, verifiable, and "
        "trustworthy. We hope this work serves as a practical reference for reproducible ML "
        "experimentation for students and researchers at VESIT and beyond."
    )
    story.append(Paragraph(p_74, body))
    story.append(PageBreak())

    # =========================================================================
    # REFERENCES
    # =========================================================================
    story.append(Paragraph("REFERENCES", cert_title))
    refs = [
        "[1] J. A. Blackard and D. J. Dean, \"Comparative accuracies of artificial neural networks and discriminant analysis in predicting forest cover types from cartographic variables,\" <i>Computers and Electronics in Agriculture</i>, vol. 24, no. 3, pp. 131–151, 1999.",
        "[2] L. Breiman, \"Random forests,\" <i>Machine Learning</i>, vol. 45, no. 1, pp. 5–32, 2001.",
        "[3] F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" <i>Journal of Machine Learning Research</i>, vol. 12, pp. 2825–2830, 2011.",
        "[4] X. Bouthillier, C. Laurent, and P. Vincent, \"Unreproducible research is reproducible,\" in <i>Proceedings of the 36th International Conference on Machine Learning (ICML)</i>, Long Beach, CA, 2019.",
        "[5] J. Dodge, G. Ilharco, R. Schwartz, A. Farhadi, H. Hajishirzi, and N. Smith, \"Fine-tuning pretrained language models: Weight initializations, data orders, and early stopping,\" <i>arXiv preprint arXiv:2002.06305</i>, 2020.",
        "[6] M. Lucic, K. Kurach, M. Michalski, S. Gelly, and O. Bousquet, \"Are GANs created equal? A large-scale study,\" in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, vol. 31, 2018.",
        "[7] C. Cortes and V. Vapnik, \"Support-vector networks,\" <i>Machine Learning</i>, vol. 20, no. 3, pp. 273–297, 1995.",
        "[8] J. R. Quinlan, \"Induction of decision trees,\" <i>Machine Learning</i>, vol. 1, no. 1, pp. 81–106, 1986."
    ]
    for r in refs:
        story.append(Paragraph(r, bullet))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # =========================================================================
    # APPENDIX (A. Data Contribution & B. SDG Goals Addressed)
    # =========================================================================
    story.append(Paragraph("APPENDIX", cert_title))
    story.append(Paragraph("A. Data Contribution", sec_title))
    p_app_data = (
        "The Forest CoverType dataset used in this project is a publicly available benchmark dataset:<br/>"
        "• <b>Dataset Name:</b> Forest CoverType (covtype)<br/>"
        "• <b>Original Source:</b> UCI Machine Learning Repository (https://archive.ics.uci.edu/ml/datasets/covertype)<br/>"
        "• <b>Accessed Via:</b> scikit-learn (sklearn.datasets.fetch_covtype)<br/>"
        "• <b>Number of Records:</b> 581,012 (full); 10,000 (project sample)<br/>"
        "• <b>Number of Features:</b> 54 (10 continuous + 44 binary)<br/>"
        "• <b>Target Variable:</b> Cover_Type (7 classes)<br/>"
        "• <b>Preprocessing:</b> Stratified 10,000-row random sample; zero imputation needed<br/><br/>"
        "No new dataset was collected or annotated as part of this project. The five CSV output "
        "files generated by the notebook (baseline_model_results.csv, train_test_split_results.csv, "
        "train_test_split_summary.csv, cross_validation_results.csv, "
        "cross_validation_summary.csv) constitute the data contribution of this project."
    )
    story.append(Paragraph(p_app_data, body))
    story.append(Spacer(1, 8))

    story.append(Paragraph("B. SDG Goals Addressed", sec_title))
    story.append(Paragraph("<b>Table A.1: Sustainable Development Goals Addressed by the Project</b>", table_caption))
    sdg_data = [
        [Paragraph("<b>SDG</b>", table_header), Paragraph("<b>Goal Name</b>", table_header), Paragraph("<b>Project Contribution</b>", table_header)],
        [Paragraph("SDG 4", table_cell_bold), Paragraph("Quality Education", table_cell), Paragraph("Demonstrates reproducible ML practices for undergraduate AI & DS education, promoting evidence-based learning and critical evaluation of ML results.", table_cell_left)],
        [Paragraph("SDG 9", table_cell_bold), Paragraph("Industry, Innovation and Infrastructure", table_cell), Paragraph("Advances reproducible AI experimentation practices essential for trustworthy AI systems in industry and research infrastructure.", table_cell_left)]
    ]
    t_sdg = Table(sdg_data, colWidths=[1.2*inch, 2.2*inch, 3.2*inch], hAlign='CENTER')
    t_sdg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sdg)
    story.append(PageBreak())

    # =========================================================================
    # LOGBOOK
    # =========================================================================
    story.append(Paragraph("LOGBOOK", cert_title))
    story.append(Paragraph("Project: Impact of Experimental Randomness on ML Model Stability and Reproducibility", ParagraphStyle('LogP', fontName='Times-Bold', fontSize=10, alignment=1)))
    story.append(Paragraph("Guide: Mrs. Bincy Ivin | Academic Year: 2026–2027", ParagraphStyle('LogG', fontName='Times-Roman', fontSize=9.5, alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Table L.1: Project Logbook</b>", table_caption))
    
    log_data = [
        [Paragraph("<b>Week</b>", table_header), Paragraph("<b>Date</b>", table_header), Paragraph("<b>Activity</b>", table_header), Paragraph("<b>Status</b>", table_header)],
        [Paragraph("1", table_cell), Paragraph("Aug 2026", table_cell), Paragraph("Project topic finalization; literature review on ML reproducibility and Forest CoverType dataset", table_cell_left), Paragraph("Completed", table_cell)],
        [Paragraph("2", table_cell), Paragraph("Aug 2026", table_cell), Paragraph("Dataset exploration: loading via fetch_covtype, EDA (shape, missing values, class distribution, feature statistics)", table_cell_left), Paragraph("Completed", table_cell)],
        [Paragraph("3", table_cell), Paragraph("Sep 2026", table_cell), Paragraph("Preprocessing pipeline design (SimpleImputer, StandardScaler); baseline model training (DT, RF, SVM) on 80/20 split", table_cell_left), Paragraph("Completed", table_cell)],
        [Paragraph("4", table_cell), Paragraph("Sep 2026", table_cell), Paragraph("Experiment 1: seed sensitivity analysis across 5 split seeds; tabulation and visualization of accuracy variation", table_cell_left), Paragraph("Completed", table_cell)],
        [Paragraph("5", table_cell), Paragraph("Oct 2026", table_cell), Paragraph("Experiment 2: repeated 5-fold CV across 3 seeds; Experiment 3: reproducibility check; confusion matrix and classification report", table_cell_left), Paragraph("Completed", table_cell)],
        [Paragraph("6", table_cell), Paragraph("Oct 2026", table_cell), Paragraph("Result analysis and interpretation; CSV export; report writing and formatting; final review with guide", table_cell_left), Paragraph("Completed", table_cell)]
    ]
    t_log = Table(log_data, colWidths=[0.8*inch, 1.1*inch, 3.6*inch, 1.1*inch], hAlign='CENTER')
    t_log.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_th_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_grid),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_log)
    story.append(PageBreak())

    # =========================================================================
    # OUTPUT PHOTOS AND RESULT VISUALIZATIONS
    # =========================================================================
    story.append(Paragraph("OUTPUT PHOTOS AND RESULT VISUALIZATIONS", cert_title))
    p_vis_intro = (
        "This section compiles all primary output figures, statistical charts, and empirical graphs "
        "generated directly during the execution of the experimental notebook in Google Colaboratory. "
        "These figures provide visual corroboration for all numerical findings, class distributions, "
        "learning curves, and performance comparisons discussed throughout this report."
    )
    story.append(Paragraph(p_vis_intro, body))
    story.append(Spacer(1, 10))

    # Figure 1: Class distribution
    f1_path = "extracted_figures/fig_cell_8_out_1.png"
    if os.path.exists(f1_path):
        story.append(Paragraph("<b>1. Forest Cover Type Target Distribution</b>", sec_title))
        story.append(Image(f1_path, width=5.8*inch, height=2.9*inch))
        story.append(Paragraph("Figure 1: Forest Cover Type Class Distribution (Full 581,012 Census)", fig_caption))
        story.append(Spacer(1, 6))

    # Figure 2: Histograms
    f2_path = "extracted_figures/fig_cell_9_out_0.png"
    if os.path.exists(f2_path):
        story.append(Paragraph("<b>2. Topographic & Hydrologic Feature Histograms</b>", sec_title))
        story.append(Image(f2_path, width=6.0*inch, height=4.0*inch))
        story.append(Paragraph("Figure 2: Histograms of Continuous Cartographic Variables (Elevation, Aspect, Slope, Distances)", fig_caption))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Figure 3: Boxplots
    f3_path = "extracted_figures/boxplots_combined.png"
    if os.path.exists(f3_path):
        story.append(Paragraph("<b>3. Outlier Inspection Across Continuous Features</b>", sec_title))
        story.append(Image(f3_path, width=6.2*inch, height=1.7*inch))
        story.append(Paragraph("Figure 3: Outlier Distribution Across Continuous Terrain Attributes (Boxplots)", fig_caption))
        story.append(Spacer(1, 8))

    # Figure 4: Correlation Heatmap
    f4_path = "extracted_figures/fig_cell_12_out_0.png"
    if os.path.exists(f4_path):
        story.append(Paragraph("<b>4. Topographic Feature Correlation Heatmap</b>", sec_title))
        story.append(Image(f4_path, width=5.2*inch, height=4.0*inch))
        story.append(Paragraph("Figure 4: Correlation Matrix of Key Environmental & Terrain Attributes", fig_caption))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # Figure 5: Stratified Train Split Check
    f5_path = "extracted_figures/fig_cell_18_out_1.png"
    if os.path.exists(f5_path):
        story.append(Paragraph("<b>5. Stratified Training Split Class Proportion Verification</b>", sec_title))
        story.append(Image(f5_path, width=5.8*inch, height=2.9*inch))
        story.append(Paragraph("Figure 5: Stratified Class Proportion Retention in Training Partition (8,000 samples)", fig_caption))
        story.append(Spacer(1, 8))

    # Figure 6: Baseline Model Accuracy
    f6_path = "extracted_figures/fig_cell_22_out_0.png"
    if os.path.exists(f6_path):
        story.append(Paragraph("<b>6. Baseline Model Accuracy Comparison Bar Chart</b>", sec_title))
        story.append(Image(f6_path, width=5.8*inch, height=3.0*inch))
        story.append(Paragraph("Figure 6: Primary Classification Accuracy Across Baseline Evaluated Models", fig_caption))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # Figure 7: Multi-Metric Benchmark
    f7_path = "extracted_figures/metric_comparison_all.png"
    if os.path.exists(f7_path):
        story.append(Paragraph("<b>7. Comprehensive Multi-Metric Benchmark Comparison</b>", sec_title))
        story.append(Image(f7_path, width=6.2*inch, height=3.1*inch))
        story.append(Paragraph("Figure 7: Multi-Metric Benchmark Comparing Accuracy, Precision, Recall, and Macro-F1", fig_caption))
        story.append(Spacer(1, 8))

    # Figure 8: Effect of Training Dataset Size
    f8_path = "extracted_figures/fig_cell_24_out_0.png"
    if os.path.exists(f8_path):
        story.append(Paragraph("<b>8. Effect of Training Dataset Scaling on Model Accuracy</b>", sec_title))
        story.append(Image(f8_path, width=5.8*inch, height=2.9*inch))
        story.append(Paragraph("Figure 8: Classifier Accuracy Learning Curves as Training Dataset Size Expands", fig_caption))
        story.append(Spacer(1, 8))

    # Figure 9: System Architecture
    f9_path = "extracted_figures/system_architecture.png"
    if os.path.exists(f9_path):
        story.append(Paragraph("<b>9. System Architecture & Modular Pipeline Design</b>", sec_title))
        story.append(Image(f9_path, width=6.2*inch, height=3.5*inch))
        story.append(Paragraph("Figure 9: Comprehensive Machine Learning Workflow and Modular Data Flow Architecture", fig_caption))
        story.append(Spacer(1, 8))

    # Build document with VESITCanvas
    print("Building polished PDF with exact VESIT alignment, header, colors, and layout...")
    doc.build(story, canvasmaker=VESITCanvas)
    print(f"Polished PDF successfully generated: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
