#!/usr/bin/env python3
"""
Task-specific parser for first file in books/rawtxt/
Process: entrepreneurship_chunk_aa
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import hashlib
import sys
from typing import Dict, List, Any


class SingleFileParser:
    def __init__(self, input_file_path, output_dir="processed"):
        self.input_file_path = Path(input_file_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
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
    
    def process_single_file(self):
        """Process the single input file and save results"""
        print(f"Processing single file: {self.input_file_path}")
        
        # Read the input file
        with open(self.input_file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Extract all components
        keywords = self.extract_keywords(text, self.input_file_path)
        ecs_elements = self.extract_ecs_elements(text, self.input_file_path)
        constraints = self.extract_constraints(text, self.input_file_path)
        metadata = self.extract_metadata(text, self.input_file_path)
        
        # Create result dictionary
        result = {
            "source_file": str(self.input_file_path),
            "keywords": keywords,
            "ecs_elements": ecs_elements,
            "constraints": constraints,
            "metadata": metadata,
            "processing_timestamp": datetime.now().isoformat()
        }
        
        # Generate output filename based on input
        input_stem = self.input_file_path.stem
        output_filename = f"{input_stem}_processed.json"
        output_path = self.output_dir / output_filename
        
        # Save result to processed directory
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully processed {self.input_file_path}")
        print(f"Output saved to: {output_path}")
        
        return output_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python process_single_file.py <input_file_path>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    processor = SingleFileParser(input_file)
    processor.process_single_file()


if __name__ == "__main__":
    # For this specific task, process the first file
    input_file = "books/rawtxt/entrepreneurship_chunk_aa"
    processor = SingleFileParser(input_file)
    processor.process_single_file()