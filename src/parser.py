#!/usr/bin/env python3
"""
Document Parser for USA Business Information
Based on the parsing methodology described in PARSING_TECH.md
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import hashlib
from typing import Dict, List, Any, Optional
import yaml


class USABusinessParser:
    def __init__(self, export_dir: str = "books/export", processed_dir: str = "processed"):
        self.export_dir = Path(export_dir)
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(exist_ok=True)
        
        # Common USA business terms for keyword extraction
        self.business_terms = [
            "company", "corporation", "llc", "partnership", "business", 
            "formation", "registration", "tax", "irs", "ein", "state", 
            "federal", "compliance", "regulation", "license", "permit",
            "operating agreement", "bylaws", "articles of incorporation",
            "annual report", "franchise tax", "registered agent", "dba",
            "sole proprietorship", "s-corp", "c-corp", "nonprofit"
        ]
    
    def tokenize_text(self, text: str) -> List[str]:
        """Split text into tokens"""
        # Simple tokenization - could be enhanced with NLTK or spaCy
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens
    
    def extract_keywords(self, text: str, source_file: str) -> List[Dict[str, Any]]:
        """Extract keywords from text following PARSING_TECH.md methodology"""
        tokens = self.tokenize_text(text)
        
        # Count frequencies
        freq_dict = {}
        for token in tokens:
            if len(token) > 2:  # Skip short words
                freq_dict[token] = freq_dict.get(token, 0) + 1
        
        # Calculate relevance scores and categorize
        total_tokens = len(tokens)
        keywords = []
        
        for term, freq in freq_dict.items():
            relevance = freq / total_tokens if total_tokens > 0 else 0
            
            # Categorize based on known business terms
            category = "general_term"
            if term in self.business_terms:
                category = "business_term"
            
            # Find position in text
            pos_match = re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE)
            position = pos_match.start() if pos_match else -1
            
            keyword = {
                "term": term,
                "frequency": freq,
                "relevance": round(relevance, 4),
                "category": category,
                "tags": ["auto_extraction", "usa_business"],
                "source_file": str(source_file),
                "position_in_text": position,
                "related_keywords": []  # Would be populated in a full implementation
            }
            
            # Add to results if relevance is above threshold
            if relevance > 0.001 or term in self.business_terms:
                keywords.append(keyword)
        
        # Sort by relevance
        keywords.sort(key=lambda x: x['relevance'], reverse=True)
        return keywords[:100]  # Return top 100 keywords
    
    def extract_ecs_elements(self, text: str, source_file: str) -> Dict[str, Any]:
        """Extract ECS (Entity-Component-System) elements from text"""
        # This is a simplified version - a full implementation would use NLP
        entities = []
        components = []
        systems = []
        
        # Look for entity-like patterns (organizations, roles, etc.)
        entity_patterns = [
            r'\b(?:company|corporation|llc|business|organization)\b',
            r'\b(?:owner|manager|director|officer|president)\b',
            r'\b(?:board|committee|department)\b'
        ]
        
        for pattern in entity_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity = {
                    "name": match.group().lower(),
                    "description": f"Entity mentioned in document: {match.group()}",
                    "attributes": {
                        "type": "business_entity",
                        "extracted_from": str(source_file),
                        "position": match.start()
                    },
                    "tags": ["business_entity", "usa_context"],
                    "source_file": str(source_file),
                    "relationships": {}
                }
                entities.append(entity)
        
        # Look for component-like patterns (attributes, properties, etc.)
        component_patterns = [
            r'\b(?:tax id|ein|ssn|identification number)\b',
            r'\b(?:address|location|registered office)\b',
            r'\b(?:capital|investment|funding)\b'
        ]
        
        for pattern in component_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                component = {
                    "name": match.group().lower(),
                    "description": f"Component mentioned in document: {match.group()}",
                    "properties": {
                        "type": "business_component",
                        "extracted_from": str(source_file),
                        "position": match.start()
                    },
                    "data_schema": {},
                    "tags": ["business_component", "usa_context"],
                    "source_file": str(source_file)
                }
                components.append(component)
        
        # Look for system-like patterns (processes, operations, etc.)
        system_patterns = [
            r'\b(?:formation|registration|filing|reporting)\b',
            r'\b(?:compliance|audit|review)\b',
            r'\b(?:operation|management|governance)\b'
        ]
        
        for pattern in system_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                system = {
                    "name": match.group().lower(),
                    "description": f"System/process mentioned in document: {match.group()}",
                    "behavior": f"Process described in document context",
                    "dependencies": [],
                    "triggers": ["document_mention"],
                    "tags": ["business_process", "usa_context"],
                    "source_file": str(source_file)
                }
                systems.append(system)
        
        return {
            "source_file": str(source_file),
            "entities": entities,
            "components": components,
            "systems": systems,
            "extraction_date": datetime.now().isoformat()
        }
    
    def extract_constraints(self, text: str, source_file: str) -> List[Dict[str, Any]]:
        """Extract constraints from text (regulatory, procedural, etc.)"""
        constraints = []
        
        # Look for constraint-indicating phrases
        constraint_indicators = [
            (r'must', 'requirement'),
            (r'shall', 'requirement'),
            (r'should', 'recommendation'),
            (r'required', 'requirement'),
            (r'necessary', 'requirement'),
            (r'need to', 'requirement'),
            (r'have to', 'requirement'),
            (r'comply with', 'compliance'),
            (r'within \d+ days?', 'temporal'),
            (r'by .* deadline', 'temporal'),
            (r'fee of \$?\d+', 'financial')
        ]
        
        constraint_id_counter = 0
        for pattern, constraint_type in constraint_indicators:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract surrounding context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                constraint = {
                    "id": f"constraint_{hashlib.md5(str(match.group()).encode()).hexdigest()[:8]}_{constraint_id_counter}",
                    "title": f"{match.group().capitalize()} requirement from {Path(source_file).name}",
                    "description": context,
                    "constraint_type": constraint_type,
                    "condition": f"text_contains('{match.group()}')",
                    "scope": "usa_business_compliance",
                    "severity": "info",  # Could be determined by context
                    "source_file": str(source_file),
                    "tags": ["auto_extracted", "usa_business"],
                    "related_constraints": [],
                    "validation_logic": f"check_{constraint_type}_requirement()",
                    "error_message": f"Requirement '{match.group()}' not met"
                }
                
                constraints.append(constraint)
                constraint_id_counter += 1
        
        return constraints
    
    def extract_metadata(self, text: str, source_file: str) -> Dict[str, Any]:
        """Extract metadata from text"""
        tokens = self.tokenize_text(text)
        
        # Calculate word count and reading time
        word_count = len(tokens)
        estimated_reading_time = max(1, word_count // 200)  # 200 wpm average
        
        # Extract top keywords for metadata
        keywords = self.extract_keywords(text, source_file)[:10]
        top_keyword_terms = [kw['term'] for kw in keywords]
        
        # Determine content type based on file name
        file_stem = Path(source_file).stem
        if 'chunk' in file_stem:
            content_type = 'book_chapter'
        elif 'manual' in file_stem.lower():
            content_type = 'guide'
        elif 'venture' in file_stem.lower():
            content_type = 'business_guide'
        else:
            content_type = 'documentation'
        
        # Determine business domains
        business_domains = []
        if any(term in text.lower() for term in ['formation', 'register', 'incorporate']):
            business_domains.append('business_formation')
        if any(term in text.lower() for term in ['tax', 'irs', 'ein', 'federal']):
            business_domains.append('taxation')
        if any(term in text.lower() for term in ['compliance', 'regulation', 'requirement']):
            business_domains.append('compliance')
        
        return {
            "source_file": str(source_file),
            "title": f"USA Business Info: {Path(source_file).name}",
            "description": f"USA business information from {Path(source_file).name}",
            "tags": ["usa_business", "information", "documentation"],
            "categories": business_domains if business_domains else ["general_business"],
            "related_files": [],  # Would be populated by cross-referencing
            "creation_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "author": "auto_processing",
            "version": "1.0",
            "relevance_score": 0.7,  # Default, could be calculated
            "content_type": content_type,
            "business_domains": business_domains,
            "difficulty_level": "intermediate",  # Could be determined by complexity
            "estimated_reading_time": estimated_reading_time,
            "word_count": word_count,
            "language": "en",  # Assuming English for USA content
            "keywords": top_keyword_terms,
            "related_entities": [],  # Would be populated from ECS extraction
            "related_components": [],
            "related_systems": [],
            "related_constraints": [],  # Would be populated from constraint extraction
            "custom_fields": {
                "document_type": content_type,
                "processing_status": "completed",
                "original_file_name": Path(source_file).name
            }
        }
    
    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single markdown file"""
        print(f"Processing: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Extract all components
        keywords = self.extract_keywords(text, file_path)
        ecs_elements = self.extract_ecs_elements(text, file_path)
        constraints = self.extract_constraints(text, file_path)
        metadata = self.extract_metadata(text, file_path)
        
        # Create result dictionary
        result = {
            "source_file": str(file_path),
            "keywords": keywords,
            "ecs_elements": ecs_elements,
            "constraints": constraints,
            "metadata": metadata,
            "processing_timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def process_all_files(self):
        """Process all markdown files in the export directory"""
        markdown_files = list(self.export_dir.glob("*.md"))
        
        if not markdown_files:
            print(f"No markdown files found in {self.export_dir}")
            return
        
        print(f"Found {len(markdown_files)} markdown files to process")
        
        for file_path in markdown_files:
            try:
                result = self.process_file(file_path)
                
                # Save result to processed directory
                output_filename = f"{file_path.stem}_parsed.json"
                output_path = self.processed_dir / output_filename
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                print(f"Saved parsed data to: {output_path}")
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue
    
    def generate_plantuml_diagrams(self):
        """Generate PlantUML diagrams based on parsed data"""
        # This would generate PlantUML diagrams based on the parsed data
        # For now, we'll create a simple example diagram
        
        plantuml_content = """@startuml
!theme plain
title USA Business Information - ECS Relationships

package "Keywords" {
  class BusinessTerm {
    - term: String
    - frequency: Integer
    - relevance: Float
  }
}

package "ECS Elements" {
  class Entity {
    - name: String
    - description: String
  }
  
  class Component {
    - name: String
    - properties: Map
  }
  
  class System {
    - name: String
    - behavior: String
  }
}

package "Constraints" {
  class Constraint {
    - id: String
    - title: String
    - constraint_type: String
  }
}

package "Metadata" {
  class DocumentMetadata {
    - source_file: String
    - title: String
    - tags: List
  }
}

BusinessTerm ||--|| Entity : relates_to
BusinessTerm ||--|| Component : relates_to
BusinessTerm ||--|| System : relates_to
BusinessTerm ||--|| Constraint : relates_to
BusinessTerm ||--|| DocumentMetadata : belongs_to

Entity ||--o{ Component : has
System ||--o{ Component : uses
Constraint ||--|| DocumentMetadata : applies_to

@enduml
"""
        
        plantuml_path = self.processed_dir / "usa_business_model.puml"
        with open(plantuml_path, 'w', encoding='utf-8') as f:
            f.write(plantuml_content)
        
        print(f"Generated PlantUML diagram: {plantuml_path}")
    
    def generate_markdown_summary(self):
        """Generate a summary markdown file with statistics"""
        # Count processed files
        json_files = list(self.processed_dir.glob("*_parsed.json"))
        total_processed = len(json_files)
        
        # Create summary
        summary_content = f"""# USA Business Information Processing Summary

## Statistics
- Total files processed: {total_processed}
- Processing completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Source directory: `{self.export_dir}`
- Output directory: `{self.processed_dir}`

## Processing Components
1. **Keyword Extraction**: Identifies important business terms
2. **ECS Elements**: Entities, Components, and Systems in business contexts
3. **Constraints**: Regulatory, procedural, and compliance requirements
4. **Metadata**: Document information and categorization

## Next Steps
- Review parsed JSON files for accuracy
- Generate additional visualizations
- Integrate with downstream systems
- Expand parsing to additional document types

## Generated Files
- Parsed data: `*_parsed.json` files
- PlantUML diagram: `usa_business_model.puml`
"""
        
        summary_path = self.processed_dir / "processing_summary.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"Generated summary: {summary_path}")


def main():
    parser = USABusinessParser()
    parser.process_all_files()
    parser.generate_plantuml_diagrams()
    parser.generate_markdown_summary()
    print("Parsing completed!")


if __name__ == "__main__":
    main()