#!/usr/bin/env python3
"""
OCR Script for PDF files using Tesseract
This script handles OCR for PDF files that don't have extractable text.
"""

import os
import sys
import subprocess
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io
import tempfile


def pdf_to_images_pymupdf(pdf_path):
    """
    Convert PDF to images using PyMuPDF (fitz)
    """
    print(f"Converting {pdf_path} to images using PyMuPDF...")
    
    doc = fitz.open(pdf_path)
    images = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Render page to image with high DPI for better OCR quality
        mat = fitz.Matrix(2.0, 2.0)  # 2x scale for better resolution
        pix = page.get_pixmap(matrix=mat)
        
        # Convert pixmap to PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        images.append((page_num, img))
        
        print(f"Processed page {page_num + 1}/{len(doc)}")
    
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


def ocr_pdf_with_pymupdf(pdf_path, output_path, lang='eng'):
    """
    Perform OCR on PDF using PyMuPDF to extract images and pytesseract for OCR
    """
    print(f"Starting OCR for {pdf_path}")
    
    # Convert PDF to images
    images = pdf_to_images_pymupdf(pdf_path)
    
    # Perform OCR on each image and collect text
    full_text = []
    for page_num, img in images:
        print(f"Performing OCR on page {page_num + 1}")
        text = ocr_image(img, lang)
        full_text.append(f"\n--- PAGE {page_num + 1} ---\n")
        full_text.append(text)
    
    # Write the combined text to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(full_text))
    
    print(f"OCR completed. Output saved to {output_path}")
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python ocr_pdf.py <input_pdf_path> <output_txt_path>")
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
    
    # Perform OCR
    success = ocr_pdf_with_pymupdf(input_pdf, output_txt)
    
    if success:
        print("OCR process completed successfully!")
    else:
        print("OCR process failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()