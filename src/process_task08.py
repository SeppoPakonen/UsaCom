#!/usr/bin/env python3
"""Process Phase 4 Task 08: Parse entrepreneurship_chunk_ab.md"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import hashlib
from typing import Dict, List, Any


class USABusinessParser:
    def __init__(self):
        self.export_dir = Path("books/export")
        self.processed_dir = Path("processed")
        self.processed_dir.mkdir(exist_ok=True)

        self.business_terms = [
            "company", "corporation", "llc", "partnership", "business",
            "formation", "registration", "tax", "irs", "ein", "state",
            "federal", "compliance", "regulation", "license", "permit",
            "operating agreement", "bylaws", "articles of incorporation",
            "annual report", "franchise tax", "registered agent", "dba",
            "sole proprietorship", "s-corp", "c-corp", "nonprofit"
        ]

    def tokenize_text(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def extract_keywords(self, text: str, source_file: str) -> List[Dict[str, Any]]:
        tokens = self.tokenize_text(text)
        freq_dict = {}
        for token in tokens:
            if len(token) > 2:
                freq_dict[token] = freq_dict.get(token, 0) + 1

        total_tokens = len(tokens)
        keywords = []

        for term, freq in freq_dict.items():
            relevance = freq / total_tokens if total_tokens > 0 else 0
            category = "general_term"
            if term in self.business_terms:
                category = "business_term"

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
                "related_keywords": []
            }

            if relevance > 0.001 or term in self.business_terms:
                keywords.append(keyword)

        keywords.sort(key=lambda x: x['relevance'], reverse=True)
        return keywords[:100]

    def extract_ecs_elements(self, text: str, source_file: str) -> Dict[str, Any]:
        entities = []
        components = []
        systems = []

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
        constraints = []

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
                    "severity": "info",
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
        tokens = self.tokenize_text(text)
        word_count = len(tokens)
        estimated_reading_time = max(1, word_count // 200)

        keywords = self.extract_keywords(text, source_file)[:10]
        top_keyword_terms = [kw['term'] for kw in keywords]

        file_stem = Path(source_file).stem
        if 'chunk' in file_stem:
            content_type = 'book_chapter'
        elif 'manual' in file_stem.lower():
            content_type = 'guide'
        elif 'venture' in file_stem.lower():
            content_type = 'business_guide'
        else:
            content_type = 'documentation'

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
            "related_files": [],
            "creation_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "author": "auto_processing",
            "version": "1.0",
            "relevance_score": 0.7,
            "content_type": content_type,
            "business_domains": business_domains,
            "difficulty_level": "intermediate",
            "estimated_reading_time": estimated_reading_time,
            "word_count": word_count,
            "language": "en",
            "keywords": top_keyword_terms,
            "related_entities": [],
            "related_components": [],
            "related_systems": [],
            "related_constraints": [],
            "custom_fields": {
                "document_type": content_type,
                "processing_status": "completed",
                "original_file_name": Path(source_file).name
            }
        }

    def process_file(self, file_path: Path) -> Dict[str, Any]:
        print(f"Processing: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        keywords = self.extract_keywords(text, file_path)
        ecs_elements = self.extract_ecs_elements(text, file_path)
        constraints = self.extract_constraints(text, file_path)
        metadata = self.extract_metadata(text, file_path)

        result = {
            "source_file": str(file_path),
            "keywords": keywords,
            "ecs_elements": ecs_elements,
            "constraints": constraints,
            "metadata": metadata,
            "processing_timestamp": datetime.now().isoformat()
        }

        return result


def main():
    parser = USABusinessParser()
    
    # Process Task 08: entrepreneurship_chunk_ab.md
    input_file = parser.export_dir / "entrepreneurship_chunk_ab.md"
    output_file = parser.processed_dir / "entrepreneurship_chunk_ab_parsed.json"
    
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return
    
    result = parser.process_file(input_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Saved parsed data to: {output_file}")
    print("Task 08 completed successfully!")


if __name__ == "__main__":
    main()
