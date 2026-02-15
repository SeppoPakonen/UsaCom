# Phase 2 Task 1: Convert PDF Books to Raw Text

## Objective
Convert the PDF books in ./books/*.pdf to raw text files in ./books/rawtxt/*.txt, split into manageable chunks.

## Process Completed

### Files with Existing Text Content
1. **Technology Ventures.pdf**
   - Converted to text format successfully
   - Split into chunks of 1000 lines each
   - Created 28 chunks: techventure_chunk_aa through techventure_chunk_bh

2. **The_Startup_Owner s_Manual-A step by step guide for building a great company.pdf**
   - Converted to text format successfully
   - Split into chunks of 1000 lines each
   - Created 28 chunks: startup_chunk_aa through startup_chunk_bh

### File Requiring OCR (Now Completed)
1. **Entrepreneurship - Successfully Launching New Ventures.pdf**
   - This file contained only images/scanned pages with no extractable text
   - Created Python script (src/ocr_pdf.py) using PyMuPDF and pytesseract for OCR
   - Successfully performed OCR on all 614 pages of the 219MB PDF
   - Split into chunks of 1000 lines each
   - Created 28 chunks: entrepreneurship_chunk_aa through entrepreneurship_chunk_bh

## Output
- Created ./books/rawtxt/ directory
- Generated text chunks for all books (including OCR'd content)
- Each chunk contains approximately 1000 lines for manual processing
- Created OCR scripts in ./src/ directory for future use

## Next Steps
- Manually process all text chunks in Phase 3
- All books are now ready for manual conversion to clean markdown