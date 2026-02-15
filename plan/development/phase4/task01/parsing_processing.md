# Phase 4: Parse Markdown Files and Generate Documentation

## Objective
Process the ./books/export/*.md files using methods documented in PARSING_TECH.md to create structured data in ./processed/ directory

## Process
1. Create ./processed/ directory
2. Copy relevant Python parsing code from ../FinCom/ if applicable
3. Adapt parsing code to handle USA company information context
4. Parse each ./books/export/*.md file to extract:
   - Company formation procedures
   - Legal requirements
   - Tax obligations
   - Compliance guidelines
   - Business structures
5. Generate structured data files in ./processed/ directory
6. Create documentation files (both .md and .puml) showing relationships between concepts
7. Ensure Python programs can parse the generated files correctly

## Output
- ./processed/ directory with parsed and structured data
- Documentation files (.md and .puml) showing relationships
- Verified Python parsing capabilities