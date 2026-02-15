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

### File Requiring OCR
1. **Entrepreneurship - Successfully Launching New Ventures.pdf**
   - This file contains only images/scanned pages with no extractable text
   - Created a placeholder file indicating OCR is needed
   - Due to the large file size (219MB), OCR processing will require special handling
   - Alternative approaches for OCR may be needed

## Output
- Created ./books/rawtxt/ directory
- Generated text chunks for files with existing text content
- Created placeholder for file requiring OCR
- Each chunk contains approximately 1000 lines for manual processing

## Next Steps
- Manually process the text chunks in Phase 3
- Address OCR for the entrepreneurship book separately if needed