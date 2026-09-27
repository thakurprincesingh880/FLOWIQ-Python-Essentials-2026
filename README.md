# FLOWIQ - Smart Service Flow Optimization System

**Course:** CSE1021 - Introduction to Problem Solving and Programming / VITyarthi Python Essentials  
**Project type:** Python Essentials course project  
**Domain:** Service operations, waiting-time reduction and resource allocation  
**Current implementation:** Console application + Jupyter demonstration

## 1. What is FLOWIQ?

FLOWIQ is a Python prototype that helps a service center handle people more intelligently. A person submits a request, the program calculates a transparent priority score, checks which counters can serve the requested service, assigns the request to the least-loaded eligible counter, estimates waiting time, and maintains live queue information.

The same basic engine can later be adapted for colleges, clinics, banks, restaurants, hotels, service centers or other places that have queues and limited service capacity.

## 2. What is actually implemented?

1. **Smart request registration** - captures user, service, urgency, impact and group size.
2. **Priority engine** - turns urgency, impact, group size and waiting time into an explainable score.
3. **Smart counter allocation** - chooses the eligible counter with the lowest projected workload.
4. **Waiting-time estimation** - uses current queued work as a simple estimate.
5. **Live queue processing** - serves the highest-priority waiting request at a counter.
6. **Time simulation** - advances waiting time for all queued tickets.
7. **What-if simulation** - compares average and maximum waiting time for different numbers of counters.
8. **Capability pairing** - finds counters that share service capabilities using `itertools.combinations()`.
9. **NumPy dashboard** - computes queue totals, averages and completed-ticket statistics.
10. **OOP design** - uses classes, inheritance, overriding, encapsulation, class methods, static methods and operator overloading.

## 3. Important limitation

FLOWIQ is an **educational decision-support prototype**. It is not a real hospital, bank or business operations system, and its estimates are intentionally simple. No real-world safety, medical or financial decision should be made from the demo output.

## 4. Project structure

```text
FLOWIQ_Submission/
|-- main.py                  <- interactive modular program to run
|-- FLOWIQ.py                <- standalone one-file version
|-- demo.py                  <- automatic demo for presentation
|-- self_test.py             <- built-in checks
|-- requirements.txt         <- NumPy + document helpers
|-- README.md                <- this guide
|-- SUBMISSION_GUIDE.md      <- what each file is for
|-- PROJECT_REPORT.md        <- report in Markdown
|-- PROJECT_VIVA.md          <- viva questions and answers
|-- RUN_ME_FIRST.txt         <- beginner run guide
|-- flowiq/
|   |-- __init__.py
|   |-- models.py            <- classes / OOP
|   |-- engine.py            <- routing and decision algorithms
|   |-- analytics.py         <- NumPy + itertools
|   |-- sample_data.py       <- demo data
|-- notebook/
|   |-- FLOWIQ_Demo.ipynb    <- Jupyter version
|-- docs/
|   |-- FLOWIQ_Project_Report.docx
|   |-- FLOWIQ_Project_Report.pdf
|-- presentation/
|   |-- FLOWIQ_Project_Presentation.pptx
|-- demo/
    |-- demo_output.txt
```

## 5. How to run

### Install Python
Use a recent Python 3 version.

### Install NumPy

```bash
pip install numpy
```

The DOCX/PPTX packages are only needed if you want to regenerate/edit the documentation yourself. They are not needed to run the application. See documentation_requirements.txt.

### Run the interactive application

```bash
python main.py
```

### Run the automatic demo

```bash
python demo.py
```

### Run the self-test

```bash
python self_test.py
```

## 6. What to show the faculty

For a short demo, run `python demo.py`. Then run `python main.py` and demonstrate:

- option 1: live dashboard
- option 3: new request
- option 4: smart counter recommendation
- option 7: what-if simulation
- option 8: shared capability pairs

## 7. VITyarthi alignment

The current VITyarthi Python Essentials course page lists 13 sections covering Python fundamentals, operators, input/output, precedence, type conversion, core data structures, control flow, functions, modules/packages, `itertools`, NumPy arrays and object-oriented programming. FLOWIQ was designed specifically around those concepts. A syllabus mapping is included in the project report.

Reference: https://vityarthi.com/detail/python-essentials-2
