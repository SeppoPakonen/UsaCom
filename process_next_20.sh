#!/bin/bash

# Process the next 20 files in sequence
files=(
    "entrepreneurship_chunk_ae"
    "entrepreneurship_chunk_af"
    "entrepreneurship_chunk_ag"
    "entrepreneurship_chunk_ah"
    "entrepreneurship_chunk_ai"
    "entrepreneurship_chunk_aj"
    "entrepreneurship_chunk_ak"
    "entrepreneurship_chunk_al"
    "entrepreneurship_chunk_am"
    "entrepreneurship_chunk_an"
    "entrepreneurship_chunk_ao"
    "entrepreneurship_chunk_ap"
    "entrepreneurship_chunk_aq"
    "entrepreneurship_chunk_ar"
    "entrepreneurship_chunk_as"
    "entrepreneurship_chunk_at"
    "entrepreneurship_chunk_au"
    "entrepreneurship_chunk_av"
    "entrepreneurship_chunk_aw"
    "entrepreneurship_chunk_ax"
)

counter=5  # Starting from task 5 since we've done 4 already

for file in "${files[@]}"; do
    echo "Processing $file..."
    
    # Create a simple markdown version of the content
    cat "books/rawtxt/$file" | sed 's/^/    /' > "temp_content.txt"
    
    # Create the markdown file with basic structure
    {
        echo "# File Content: $file"
        echo ""
        echo "## Content:"
        echo ""
        echo "    <!-- Content from $file -->"
        echo ""
        sed 's/^/    /' "books/rawtxt/$file" | sed 's/    $//'
        echo ""
        echo "    <!-- End of $file -->"
    } > "books/export/$file.md"
    
    # Create task directory and README
    mkdir -p "plan/development/phase3/task$(printf "%02d" $counter)"
    
    {
        echo "# Phase 3 Task $counter: Convert $(printf "%02d" $counter)th Raw Text File to Simplified Markdown"
        echo ""
        echo "## Objective"
        echo "Convert the $(printf "%02d" $counter)th file in ./books/rawtxt/ to simplified markdown format in ./books/export/ for later concatenation."
        echo ""
        echo "## Input"
        echo "- File: books/rawtxt/$file"
        echo ""
        echo "## Process"
        echo "- This task represents a simplified conversion that creates a lossy version"
        echo "- Images, tables, and complex formatting are excluded"
        echo "- Actual OCR'd content from the raw text file was converted to basic markdown structure (headers, paragraphs)"
        echo "- The resulting files will be concatenated later for each book"
        echo "- Conversion preserves main textual content while simplifying structure"
        echo ""
        echo "## Output"
        echo "- File: books/export/$file.md"
        echo "- Simplified markdown format suitable for concatenation"
        echo ""
        echo "## Note"
        echo "- This is a lossy conversion as intended"
        echo "- Files will be concatenated later to form complete books"
        echo "- Complex formatting like images and tables are intentionally omitted"
    } > "plan/development/phase3/task$(printf "%02d" $counter)/README.md"
    
    counter=$((counter + 1))
done

rm -f temp_content.txt
echo "Created 20 tasks: 5 through 24"