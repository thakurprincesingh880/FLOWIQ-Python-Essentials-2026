# FLOWIQ - Submission Guide

The screenshot available for this work shows your approved VITyarthi flipped course and the course name **Python Essentials**. It does not show a separate project rubric or submission checklist, so this bundle includes a complete, organized submission set without assuming a hidden rubric.

## What the files mean

### 1. `main.py`
This is the **main modular project**. It opens an interactive menu and lets the evaluator use FLOWIQ.

### 1A. `FLOWIQ.py`
This is the **standalone single-file version**. Use it when the submission portal accepts only one Python file. It contains the same core logic without requiring the `flowiq/` package folder.

### 2. `flowiq/`
This is the project's Python package. It keeps the code organized into:
- `models.py` - classes and data
- `engine.py` - smart allocation and queue logic
- `analytics.py` - NumPy analytics, simulation and combinations
- `sample_data.py` - demonstration setup

Do not submit only `models.py`. The package works together with `main.py`.

### 3. `demo.py`
Runs a complete demonstration automatically. This is useful when you want to show the project without entering many inputs manually.

### 4. `self_test.py`
Contains simple built-in assertions to check important functions. Run it before submission.

### 5. `requirements.txt`
Lists external Python packages. The actual application uses **NumPy**; `python-docx` and `python-pptx` are included only for working with the documentation files.

### 6. `README.md`
Explains the project and how to run it.

### 7. `docs/FLOWIQ_Project_Report.docx`
Editable formal project report. Put your name, registration number, section, faculty name and submission date on the title page if required by your university.

### 8. `docs/FLOWIQ_Project_Report.pdf`
PDF copy of the report for easy viewing/sharing.

### 9. `PROJECT_REPORT.md`
Plain-text/Markdown copy of the report content. This is useful as a lightweight source version.

### 10. `PROJECT_VIVA.md`
Viva questions, answers and a 30-second project explanation.

### 11. `presentation/FLOWIQ_Project_Presentation.pptx`
A ready-to-edit presentation. Add your name/team details before presenting.

### 12. `notebook/FLOWIQ_Demo.ipynb`
Jupyter Notebook demonstration of the core features, matching the learning environment mentioned by VITyarthi.

## What to submit

Because the exact VIT/VITyarthi project upload rubric is not visible in the screenshot, the safest general submission is the **complete ZIP folder** so that no required project dependency is accidentally omitted.

If the portal asks for separate files, use:

- **Code:** `main.py` + `flowiq/` + `demo.py` + `self_test.py`
- **Report:** `FLOWIQ_Project_Report.docx` or PDF, depending on the portal instruction
- **Presentation:** `FLOWIQ_Project_Presentation.pptx` only if a PPT is requested
- **Notebook:** `FLOWIQ_Demo.ipynb` only if a notebook is requested

## Before uploading

1. Run `python self_test.py`.
2. Run `python demo.py`.
3. Open the report and fill in your personal academic details.
4. Do not upload `__pycache__` folders or `.pyc` files.
5. Keep the `flowiq` folder in the same location as `main.py`.
