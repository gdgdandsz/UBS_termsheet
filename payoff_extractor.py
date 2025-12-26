"""
Main workflow for extracting payoff information from term sheets
"""
import json
from typing import Dict, Optional
from llm_client import LLMClient
from document_loader import load_pdf_text, split_text
from prompts import (
    get_payoff_extraction_prompt,
    get_section_extraction_prompt,
    get_validation_prompt
)


class PayoffExtractor:
    """Main class for extracting payoff information from term sheets"""
    
    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ):
        """
        Initialize the payoff extractor
        
        Args:
            provider: LLM provider ("openai", "anthropic", "deepseek")
            model: Model name
            temperature: Temperature setting
        """
        self.llm_client = LLMClient(provider=provider, model=model, temperature=temperature)
    
    def extract_from_pdf(
        self,
        pdf_path: str,
        use_chunking: bool = True,
        chunk_size: int = 4000
    ) -> Dict:
        """
        Extract payoff information from a PDF term sheet
        
        Args:
            pdf_path: Path to the PDF file
            use_chunking: Whether to split document into chunks for processing
            chunk_size: Size of chunks if chunking is used
            
        Returns:
            Dictionary containing extracted payoff information
        """
        # Load document
        print(f"Loading PDF: {pdf_path}")
        document_text = load_pdf_text(pdf_path)
        print(f"Document loaded: {len(document_text)} characters")
        
        if use_chunking and len(document_text) > chunk_size:
            # Split into chunks
            print("Splitting document into chunks...")
            chunks = split_text(document_text, chunk_size=chunk_size, overlap=200)
            print(f"Split into {len(chunks)} chunks")
            
            # Process each chunk and merge results
            all_results = []
            for i, chunk in enumerate(chunks):
                print(f"Processing chunk {i+1}/{len(chunks)}...")
                try:
                    prompt = get_payoff_extraction_prompt(chunk)
                    result = self.llm_client.extract_json(prompt)
                    # Ensure result is a dictionary
                    if isinstance(result, dict):
                        all_results.append(result)
                    else:
                        print(f"Warning: Chunk {i+1} returned non-dict result, skipping")
                except Exception as e:
                    print(f"Error processing chunk {i+1}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            # Merge results
            if all_results:
                merged_result = self._merge_results(all_results)
                print("Extraction completed successfully!")
                return merged_result
            else:
                return {"error": "Failed to extract information from any chunk"}
        else:
            # Process entire document
            print("Extracting payoff information...")
            try:
                prompt = get_payoff_extraction_prompt(document_text)
                result = self.llm_client.extract_json(prompt)
                print("Extraction completed successfully!")
                return result
            except Exception as e:
                print(f"Error during extraction: {e}")
                return {
                    "error": f"Extraction failed: {str(e)}"
                }
    
    def _merge_results(self, results: list) -> Dict:
        """
        Merge multiple extraction results into one
        
        Args:
            results: List of extraction result dictionaries
            
        Returns:
            Merged result dictionary
        """
        merged = {}
        
        # Merge all results - use the most complete one or merge intelligently
        for result in results:
            if not isinstance(result, dict):
                continue
            
            # For each key in the result, merge into merged dict
            for key, value in result.items():
                if value is None or value == "":
                    continue
                
                if key not in merged:
                    # First time seeing this key, just use it
                    merged[key] = value
                elif isinstance(value, dict) and isinstance(merged[key], dict):
                    # Both are dicts, merge them
                    for sub_key, sub_value in value.items():
                        if sub_value and (sub_key not in merged[key] or not merged[key][sub_key]):
                            merged[key][sub_key] = sub_value
                elif isinstance(value, list) and isinstance(merged[key], list):
                    # Both are lists, merge unique items
                    # For conditional_coupons, check for duplicates based on trigger_condition
                    if key == "conditional_coupons":
                        seen_conditions = set()
                        # First, collect conditions from existing merged list
                        for item in merged[key]:
                            if isinstance(item, dict):
                                condition = item.get("trigger_condition", str(item))
                                seen_conditions.add(condition)
                        
                        # Then add new items that aren't duplicates
                        for item in value:
                            if isinstance(item, dict):
                                condition = item.get("trigger_condition", str(item))
                                if condition and condition not in seen_conditions:
                                    merged[key].append(item)
                                    seen_conditions.add(condition)
                            elif item not in merged[key]:
                                merged[key].append(item)
                    else:
                        # For other lists, just append unique items
                        for item in value:
                            if item not in merged[key]:
                                merged[key].append(item)
                else:
                    # If types don't match or value is more complete, use the new value
                    if isinstance(value, str) and len(value) > len(str(merged[key])):
                        merged[key] = value
                    elif not isinstance(merged[key], (dict, list)):
                        merged[key] = value
        
        return merged
    
    def extract_section(self, section_text: str, section_name: str) -> Dict:
        """
        Extract information from a specific section
        
        Args:
            section_text: Text content of the section
            section_name: Name of the section
            
        Returns:
            Dictionary containing extracted information
        """
        print(f"Extracting from section: {section_name}")
        try:
            prompt = get_section_extraction_prompt(section_text, section_name)
            result = self.llm_client.extract_json(prompt)
            return result
        except Exception as e:
            return {
                "error": f"Failed to extract section: {str(e)}"
            }
    
    def validate_extraction(self, extracted_data: Dict, original_text: str) -> Dict:
        """
        Validate extracted data against original text
        
        Args:
            extracted_data: Previously extracted data
            original_text: Original document text for validation
            
        Returns:
            Validation results
        """
        print("Validating extraction...")
        try:
            extracted_json = json.dumps(extracted_data, indent=2, ensure_ascii=False)
            # Limit text for validation to avoid token limits
            validation_text = original_text[:2000] if len(original_text) > 2000 else original_text
            
            prompt = get_validation_prompt(extracted_json, validation_text)
            result = self.llm_client.extract_json(prompt)
            return result
        except Exception as e:
            return {
                "error": f"Validation failed: {str(e)}"
            }
    
    def extract_with_validation(self, pdf_path: str) -> Dict:
        """
        Extract and validate payoff information
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted and validated information
        """
        # Extract
        extracted = self.extract_from_pdf(pdf_path)
        
        if "error" in extracted:
            return extracted
        
        # Load original text for validation
        original_text = load_pdf_text(pdf_path)
        
        # Validate
        validation = self.validate_extraction(extracted, original_text)
        
        return {
            "extracted_data": extracted,
            "validation": validation
        }
