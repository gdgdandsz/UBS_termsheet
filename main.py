"""
Main script to run payoff extraction workflow
"""
import json
import sys
from pathlib import Path
from payoff_extractor import PayoffExtractor


def main():
    """Main execution function"""
    # Default PDF path
    default_pdf = "term_sheet.pdf"
    
    # Get PDF path from command line or use default
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_pdf
    
    # Check if file exists
    if not Path(pdf_path).exists():
        print(f"Error: File '{pdf_path}' not found!")
        print(f"Usage: python main.py [path_to_pdf]")
        sys.exit(1)
    
    # Initialize extractor
    print("=" * 60)
    print("Term Sheet Payoff Information Extractor")
    print("=" * 60)
    print()
    
    try:
        extractor = PayoffExtractor()
    except Exception as e:
        print(f"Error initializing LLM client: {e}")
        print("\nPlease check your .env file and ensure API keys are set correctly.")
        print("Make sure you have installed the required packages: pip install -r requirements.txt")
        sys.exit(1)
    
    # Extract information
    try:
        result = extractor.extract_from_pdf(pdf_path, use_chunking=True)
        
        # Save results
        output_file = Path(pdf_path).stem + "_payoff_extraction.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print()
        print("=" * 60)
        print("Extraction Results")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print()
        print(f"Results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

