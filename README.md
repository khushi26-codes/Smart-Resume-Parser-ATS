# 📄 Smart Resume Parser - AI Based ATS System

> Final Year Diploma Project - Information Technology
> An intelligent resume parser that extracts information from **both scanned and text-based resumes** with ATS scoring.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)
![OCR](https://img.shields.io/badge/OCR-EasyOCR%2BPyMuPDF-green)

### 🚀 Live Demo
`streamlit run app.py`

### ✨ Features
- ✅ **Dual Support:** Text PDF/DOCX + Scanned Image PDF (257+ words via EasyOCR)
- ✅ **Generic Parsing:** Not hardcoded - Works for any candidate (Tested: Khushi Yadav, Tez Prakash etc.)
- ✅ **Smart Extraction:**
    - Name (First 5 lines logic, avoids "Resume" keyword)
    - Email, Phone, LinkedIn (Regex)
    - Skills & Education (Dynamic keyword matching)
    - Experience (Fresher / Internship / Experience)
- ✅ **ATS Score:** Auto-calculated 0-95% based on completeness
- ✅ **Professional UI:** Metrics, Progress Bar, Cards, Data Visuals
- ✅ **Export:** CSV & JSON report for multiple resumes

### 🛠️ Tech Stack - As per Guide
1. **PyMuPDF (fitz) + python-docx** - Text extraction
2. **Cleaning** - Lowercase, Regex, Word boundary
3. **spaCy + Regex** - Entity extraction
4. **JSON / Table Format** - Pandas DataFrame
5. **Streamlit** - Drag & Drop UI
6. **Export** - CSV/JSON
7. **Extra: EasyOCR** - For scanned resumes (Main problem solved)

### 📦 Installation

```bash
pip install streamlit PyMuPDF python-docx easyocr pandas pillow numpy
