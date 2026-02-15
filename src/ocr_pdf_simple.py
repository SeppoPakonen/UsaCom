#!/usr/bin/env python3
"""
Simple OCR Script for PDF files using Tesseract
This script handles OCR for PDF files that don't have extractable text.
Processes in batches to manage memory and time.
"""

import os
import sys
import subprocess
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io


def pdf_to_images_pymupdf_range(pdf_path, start_page=0, end_page=None):
    """
    Convert specific range of PDF pages to images using PyMuPDF (fitz)
    """
    print(f"Converting pages {start_page} to {end_page} of {pdf_path} to images using PyMuPDF...")
    
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    if end_page is None or end_page > total_pages:
        end_page = total_pages
    
    images = []
    
    for page_num in range(start_page, end_page):
        page = doc.load_page(page_num)
        # Render page to image with high DPI for better OCR quality
        mat = fitz.Matrix(2.0, 2.0)  # 2x scale for better resolution
        pix = page.get_pixmap(matrix=mat)
        
        # Convert pixmap to PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        images.append((page_num, img))
        
        if (page_num + 1) % 10 == 0:  # Print progress every 10 pages
            print(f"Processed page {page_num + 1}/{total_pages}")
    
    doc.close()
    return images


def ocr_image(image, lang='eng'):
    """
    Perform OCR on a single image using pytesseract
    """
    try:
        import pytesseract
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except ImportError:
        print("pytesseract not found. Install with: pip install pytesseract")
        return ""
    except Exception as e:
        print(f"Error performing OCR on image: {e}")
        return ""


def ocr_pdf_batched(pdf_path, output_path, batch_size=50, lang='eng'):
    """
    Perform OCR on PDF in batches to manage memory and allow progress tracking
    """
    print(f"Starting batched OCR for {pdf_path}")
    
    # First, get total number of pages
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()
    
    print(f"Total pages to process: {total_pages}")
    
    # Process in batches
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"OCR Result for: {os.path.basename(pdf_path)}\n")
        f.write(f"Total pages: {total_pages}\n")
        f.write("="*50 + "\n\n")
    
    for start_page in range(0, total_pages, batch_size):
        end_page = min(start_page + batch_size, total_pages)
        print(f"\nProcessing batch: pages {start_page + 1} to {end_page}")
        
        # Convert batch of pages to images
        images = pdf_to_images_pymupdf_range(pdf_path, start_page, end_page)
        
        # Perform OCR on each image and collect text
        batch_text = []
        for page_idx, (page_num, img) in enumerate(images):
            page_text = ocr_image(img, lang)
            batch_text.append(f"\n--- PAGE {page_num + 1} ---\n")
            batch_text.append(page_text)
            
            # Show progress every 5 pages within the batch
            if (page_idx + 1) % 5 == 0:
                print(f"  OCR completed for page {page_num + 1} ({page_idx + 1}/{len(images)})")
        
        # Append batch text to output file
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(''.join(batch_text))
        
        print(f"Completed batch: pages {start_page + 1} to {end_page}")
    
    print(f"All batches completed. Output saved to {output_path}")
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python ocr_pdf_simple.py <input_pdf_path> <output_txt_path>")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_txt = sys.argv[2]
    
    if not os.path.exists(input_pdf):
        print(f"Input file does not exist: {input_pdf}")
        sys.exit(1)
    
    # Ensure required packages are available
    try:
        import pytesseract
        import fitz
        from PIL import Image
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Install required packages with: pip install pytesseract PyMuPDF Pillow")
        sys.exit(1)
    
    # Perform batched OCR
    success = ocr_pdf_batched(input_pdf, output_txt)
    
    if success:
        print("Batched OCR process completed successfully!")
    else:
        print("Batched OCR process failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()