#!/usr/bin/env python3
"""
OCR Script for Financial_Accounting.pdf
Converts scanned PDF pages to text using Tesseract OCR.
Uses pdftoppm for PDF->image conversion (no PyMuPDF needed).
"""

import os
import sys
from pathlib import Path
import subprocess
import tempfile
import shutil
import glob


# Configuration
PDF_PATH = Path("/home/sblo/Dev/UsaCom/books/Financial_Accounting.pdf")
OUTPUT_DIR = Path("/home/sblo/Dev/UsaCom/books/rawtxt/financial_accounting")
LINES_PER_CHUNK = 1000


def pdf_to_images(pdf_path, output_dir):
    """Convert PDF pages to PNG images using pdftoppm."""
    print(f"Converting PDF to images: {pdf_path}")
    
    # Create temp directory for images
    tmp_img_dir = output_dir / "tmp_images"
    tmp_img_dir.mkdir(parents=True, exist_ok=True)
    
    # Use pdftoppm to convert PDF to PNG images
    # -png: output format
    # -r 200: 200 DPI resolution (good for OCR)
    prefix = str(tmp_img_dir / "page")
    
    result = subprocess.run(
        ['pdftoppm', '-png', '-r', '200', str(pdf_path), prefix],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error running pdftoppm: {result.stderr}")
        sys.exit(1)
    
    # Get list of generated images
    image_files = sorted(glob.glob(f"{prefix}*.png"))
    print(f"  Created {len(image_files)} page images")
    
    return image_files


def ocr_image(image_path):
    """Perform OCR on image using Tesseract via subprocess."""
    try:
        result = subprocess.run(
            ['tesseract', image_path, 'stdout', '--psm', '3', '-l', 'eng'],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"  Warning: OCR timeout for {image_path}")
        return ""


def ocr_pdf(image_files):
    """Perform OCR on all images and return combined text."""
    all_text = []
    total = len(image_files)

    for idx, image_path in enumerate(image_files):
        page_num = idx + 1
        text = ocr_image(image_path)
        if text.strip():
            all_text.append(f"--- PAGE {page_num} ---\n{text}")

        if page_num % 25 == 0:
            print(f"OCR Progress: {page_num}/{total} pages ({page_num/total*100:.1f}%)")

    return "\n\n".join(all_text)


def split_into_chunks(text, lines_per_chunk):
    """Split text into chunks of specified line count."""
    lines = text.split('\n')
    chunks = []
    
    for i in range(0, len(lines), lines_per_chunk):
        chunk_lines = lines[i:i + lines_per_chunk]
        chunks.append('\n'.join(chunk_lines))
    
    return chunks


def save_chunks(chunks, output_dir):
    """Save chunks to files with alphabetical naming."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Use alphabetical suffix (aa, ab, ac, ...)
    suffix_num = 0

    for i, chunk in enumerate(chunks):
        # Convert number to alphabetical suffix
        suffix = ""
        n = suffix_num
        while n >= 26:
            suffix = chr(ord('a') + (n % 26)) + suffix
            n = n // 26 - 1
        suffix = chr(ord('a') + n) + suffix

        filename = f"financial_accounting_chunk_{suffix}"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(chunk)

        line_count = len(chunk.split('\n'))
        print(f"  Created {filename} ({line_count} lines)")
        suffix_num += 1

    return len(chunks)


def cleanup_images(output_dir):
    """Remove temporary image files."""
    tmp_img_dir = output_dir / "tmp_images"
    if tmp_img_dir.exists():
        shutil.rmtree(tmp_img_dir)
        print(f"  Cleaned up temporary images")


def main():
    """Main OCR process."""
    print("=" * 60)
    print("Financial Accounting Book OCR Process")
    print("=" * 60)

    # Check if PDF exists
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}")
        sys.exit(1)

    print(f"\nStep 1: Converting PDF to images...")
    image_files = pdf_to_images(PDF_PATH, OUTPUT_DIR)
    print(f"  Converted {len(image_files)} pages to images")

    print(f"\nStep 2: Performing OCR (this may take 30-60 minutes)...")
    combined_text = ocr_pdf(image_files)

    print(f"\nStep 3: Cleaning up temporary images...")
    cleanup_images(OUTPUT_DIR)

    print(f"\nStep 4: Splitting into chunks...")
    chunks = split_into_chunks(combined_text, LINES_PER_CHUNK)
    print(f"  Created {len(chunks)} chunks")

    print(f"\nStep 5: Saving chunks to {OUTPUT_DIR}...")
    num_saved = save_chunks(chunks, OUTPUT_DIR)

    print("\n" + "=" * 60)
    print("OCR Complete!")
    print(f"  Total pages processed: {len(image_files)}")
    print(f"  Total chunks created: {num_saved}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print("=" * 60)

    # Summary
    total_lines = sum(len(chunk.split('\n')) for chunk in chunks)
    total_chars = len(combined_text)
    print(f"\nSummary:")
    print(f"  Total lines: {total_lines:,}")
    print(f"  Total characters: {total_chars:,}")
    print(f"  Average lines per chunk: {total_lines/num_saved:.0f}")


if __name__ == "__main__":
    main()
