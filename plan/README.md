# UsaCom Project Plan

This plan outlines the development of a USA company information system, starting from books and extending to detailed tax code and law code processing. The project follows a phased approach to transform raw book content into a structured simulation game.

## Phases Overview

### [Phase 1: Check if Books Need OCR](discovery/phase1/task01/check_text_data.md)
Check if the PDF books in ./books/*.pdf already contain text data or if they need OCR processing.

### [Phase 2: Convert PDF Books to Raw Text](discovery/phase2/task01/convert_to_txt.md)
Convert the PDF books in ./books/*.pdf to raw text files in ./books/rawtxt/*.txt, split into manageable chunks.

### [Phase 3: Manual Conversion from Raw Text to Clean Markdown](development/phase3/task01/manual_conversion.md)
Manually read all ./books/rawtxt/*.txt chunks and convert them to clean ./books/export/*.md files. This phase requires extensive manual work with no scripting allowed.

### [Phase 4: Parse Markdown Files and Generate Documentation](development/phase4/task01/parsing_processing.md)
Process the ./books/export/*.md files using methods documented in PARSING_TECH.md to create structured data in ./processed/ directory.

### [Phase 5: Create Unified Action Planner and Virtual Map](testing/phase5/task01/action_planner_map.md)
Develop a unified action planner based on processed directory data and create a metaphorical/virtual map for simulation.

### [Phase 6: Develop Simulation Game](deployment/phase6/task01/simulation_game.md)
Create an interactive simulation game based on the virtual map and action planner from Phase 5.

## Project Scope
- Focus on USA company information instead of Finland's company info
- Start from books and later extend to detailed tax code and law code
- Emphasis on transforming raw information into structured, actionable data
- Final product will be both an information system and educational simulation game

## Directory Structure
- discovery/: Early-stage investigation and preparation tasks
- development/: Core development and processing tasks  
- testing/: Validation and refinement tasks
- deployment/: Final implementation and delivery tasks