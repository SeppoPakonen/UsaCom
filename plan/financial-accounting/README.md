# Financial Accounting Book Processing Track

## Overview
This track covers the processing of the Financial_Accounting.pdf book for the UsaCom project.

## Book Information
- **File**: books/Financial_Accounting.pdf
- **Size**: 71 MB
- **Pages**: ~700 (estimated)
- **Content Type**: Scanned PDF requiring OCR

## Track Structure

### Phase 1: Assessment (COMPLETED)
- **Task 01**: Confirm OCR requirement
- **Status**: COMPLETED - PDF has no extractable text, OCR required

### Phase 2: OCR and Text Extraction
- **Task 01**: Install dependencies and perform OCR
- **Output**: books/rawtxt/financial_accounting/*.txt

### Phase 3: Manual Conversion to Markdown
- **Tasks 01-28**: Convert raw OCR text to clean markdown
- **Output**: books/export/financial_accounting/*.md

### Phase 4: Parse and Process
- **Tasks 01-28**: Parse markdown files to structured JSON
- **Output**: processed/financial_accounting/*_parsed.json

### Phase 5: Integration
- **Tasks 01-10**: Integrate financial accounting data into simulation game
- **Output**: Enhanced game mechanics with accounting concepts

## Directory Structure
```
plan/financial-accounting/
├── phase1/task01/     # Assessment
├── phase2/task01/     # OCR
├── phase3/task01-28/  # Manual conversion
├── phase4/task01-28/  # Parsing
└── phase5/task01-10/  # Integration

books/
├── rawtxt/financial_accounting/   # Raw OCR text chunks
└── export/financial_accounting/   # Clean markdown files

processed/
└── financial_accounting/          # Parsed JSON files
```

## Estimated Timeline
- Phase 1: Complete (assessment done)
- Phase 2: 1-2 hours (OCR processing)
- Phase 3: 8-12 hours (manual conversion)
- Phase 4: 1-2 hours (automated parsing)
- Phase 5: 2-3 hours (integration)

## Dependencies
- Tesseract OCR (/usr/bin/tesseract)
- PyMuPDF (fitz)
- pdf2image
- Pillow
- pytesseract

## Virtual Environment
Use ~/venv for all Python operations:
```bash
source ~/venv/bin/activate
python3 src/ocr_financial_accounting.py
```
