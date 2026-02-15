# Phase 3: Manual Conversion from Raw Text to Clean Markdown

## Objective
Manually read all ./books/rawtxt/*.txt chunks and convert them to clean ./books/export/*.md files

## Important Notes
- NO SCRIPTING OR PROGRAMMATIC PROCESSING ALLOWED
- This phase requires extensive manual work by human reviewers
- Each chunk must be carefully proofread and converted to clean markdown format
- AI agents cannot process large amounts of text at once (limited to ~500-1000 lines per task)

## Process
1. Create ./books/export/ directory
2. Assign individual chunks to human reviewers
3. Each reviewer manually converts raw text to clean markdown format
4. Pay attention to:
   - Headers and section titles
   - Lists and bullet points
   - Tables and figures (describe in text)
   - Page numbers and footnotes
   - Formatting inconsistencies
5. Maintain original meaning and content accuracy
6. Save converted files as .md in ./books/export/

## Output
- ./books/export/ directory with clean markdown files
- Quality-checked content ready for automated processing