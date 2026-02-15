# Phase 3: Manual Conversion from Raw Text to Clean Markdown

## Objective
Manually read all ./books/rawtxt/*.txt chunks and convert them to clean ./books/export/*.md files

## Important Notes
- NO SCRIPTING OR PROGRAMMATIC PROCESSING ALLOWED
- This phase requires extensive manual work by human reviewers
- Each chunk must be carefully proofread and converted to clean markdown format
- AI agents cannot process large amounts of text at once (limited to ~500-1000 lines per task)

## Process
1. Each chunk from ./books/rawtxt/ will be assigned to a human reviewer
2. Reviewers will manually convert raw text to clean markdown format
3. Pay attention to:
   - Headers and section titles
   - Lists and bullet points
   - Tables and figures (describe in text)
   - Page numbers and footnotes
   - Formatting inconsistencies
4. Maintain original meaning and content accuracy
5. Save converted files as .md in ./books/export/ with matching names

## Chunks to Process
There are 84 total chunks across 3 books:
- Technology Ventures: 28 chunks (techventure_chunk_aa through techventure_chunk_bh)
- Startup Owner's Manual: 28 chunks (startup_chunk_aa through startup_chunk_bh)
- Entrepreneurship: 28 chunks (entrepreneurship_chunk_aa through entrepreneurship_chunk_bh)

## Output
- ./books/export/ directory with clean markdown files
- Quality-checked content ready for automated processing