# Phase 2: Convert PDF Books to Raw Text

## Objective
Convert the PDF books in ./books/*.pdf to raw text files in ./books/rawtxt/*.txt

## Prerequisites
- Phase 1 completed to determine which files need OCR
- If files need OCR, use Tesseract or similar OCR tool
- If files already have text, use pdftotext utility

## Process
1. Create ./books/rawtxt/ directory
2. For each PDF in ./books/, create corresponding .txt file in ./books/rawtxt/
3. Name files consistently (e.g., Entrepreneurship_-_Successfully_Launching_New_Ventures.txt)
4. Split large text files into manageable chunks (approx. 500-1000 lines per chunk)
5. Save chunk files with sequential numbering (e.g., entrepreneurship_chunk_001.txt)

## Output
- ./books/rawtxt/ directory with converted text files
- Chunked files ready for manual processing