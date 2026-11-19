# VESIT Mini Project - 2B LaTeX Report: Impact of Experimental Randomness on ML Model Stability and Reproducibility

**Department of Artificial Intelligence and Data Science (AI&DS)**  
**Vivekanand Education Society's Institute of Technology (VESIT)**  
**Academic Year:** 2026--2027  

---

## 👥 Student Details
- **Prem K.K. Bhojwani** (Roll No. 04)
- **Jiya Gurbani** (Roll No. 15)
- **Harsh Dingreja** (Roll No. 12)

**Project Guide:** Mrs. Bincy Ivin (Assistant Professor, Department of AI&DS)  
**Head of Department:** Dr. Anjali Shrikant Yeole  
**Principal:** Dr. J. M. Nair  

---

## 📁 Repository Structure

```
VESIT_Mini_Project_Template/
├── main.tex                    # Master LaTeX file
├── project_details.tex         # Central configuration for names, titles, guide
├── references.bib              # IEEE BibTeX citations
├── logbook.tex                 # Appendix: 12-Week Project Review Logbook
├── README.md                   # This documentation guide
├── frontmatter/
│   ├── titlepage.tex           # Official Cover / Title Page
│   ├── certificate.tex         # Official Certificate with sign lines
│   ├── declaration.tex         # Student Declaration page
│   ├── acknowledgement.tex     # Acknowledgement page
│   ├── abstract.tex            # Abstract with Keywords
│   └── abbreviations.tex       # List of Abbreviations
├── chapters/
│   ├── chapter1_introduction.tex           # Background, Problem Statement, Objectives
│   ├── chapter2_literature_review.tex      # Review of papers, Table 2.1, Research Gap
│   ├── chapter3_proposed_methodology.tex   # Equations, Subsampling, Normalization
│   ├── chapter4_system_design.tex          # Architecture diagram, Workflow, DFD
│   ├── chapter5_implementation.tex         # Python Colab code, Hyperparameters
│   ├── chapter6_results_discussion.tex     # Tables 6.1-6.6, Split seeds, Repro audit
│   └── chapter7_conclusion.tex             # Conclusions, Limitations, Future Scope
├── appendix/
│   └── appendix.tex            # UN SDG Mapping & All Output Visualizations
└── figures/                    # High-resolution diagrams and plots
    ├── VESIT LOGO ICON (1).png # Official VESIT crest
    ├── fig_system_architecture.png
    ├── fig_class_distribution.png
    ├── fig_continuous_features.png
    ├── fig_boxplots.png
    ├── fig_correlation_matrix.png
    ├── fig_train_test_split.png
    ├── fig_baseline_accuracy.png
    ├── fig_metric_comparison.png
    └── fig_data_scaling.png
```

---

## 🚀 How to Compile

### Option 1: Overleaf (Recommended)
1. Zip the entire `VESIT_Mini_Project_Template (1)` directory (or select all files and compress into `.zip`).
2. Go to [Overleaf](https://www.overleaf.com), click **New Project** $\rightarrow$ **Upload Project**, and select your `.zip` file.
3. Ensure the compiler is set to **pdfLaTeX** (default in Overleaf).
4. Click **Recompile**. Your entire 30+ page report with official headers, figures, tables, and bibliography will generate instantly!

### Option 2: Local LaTeX Installation (TeX Live / MiKTeX)
Run the standard LaTeX compilation sequence from PowerShell or terminal:
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
