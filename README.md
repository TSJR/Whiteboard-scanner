# Whiteboard Scanner

A Raspberry Pi + Google Cloud Vision + GPT-4o pipeline that converts
photos of classroom whiteboards into a clean, structured LaTeX-generated
PDF. Designed so students can focus on learning instead of copying
notes.

This project automatically performs:

**Image Capture → OCR → LaTeX Conversion → PDF Generation**

## Overview

The workflow of this project is:

1.  The Raspberry Pi captures one or more whiteboard images and saves
    them into the `images/` directory.\
2.  `app.py` reads every image in that folder (sorted alphabetically).\
3.  Each image is sent to **Google Cloud Vision** for text OCR.\
4.  All extracted text is concatenated into a single document.\
5.  The text is fed to **OpenAI GPT-4o**, which converts it into
    structured **LaTeX** based on your custom prompt.\
6.  The generated LaTeX is compiled into a final PDF using
    **pdflatex**.\
7.  The PDF is written to `output/output.pdf`.
