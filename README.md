# Term Sheet Payoff Information Extractor

A workflow based on direct LLM API calls for extracting payoff-related information from financial product term sheets.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:

Create a `.env` file:
```env
# DeepSeek (Recommended)
DEEPSEEK_API_KEY=your_api_key_here
LLM_MODEL=deepseek-chat
LLM_TEMPERATURE=0.0
LLM_PROVIDER=deepseek
DEEPSEEK_API_BASE_URL=https://api.deepseek.com

```

## Usage

### Basic Usage

```bash
python main.py term_sheet.pdf
```

### Use in Code

```python
from payoff_extractor import PayoffExtractor

# Initialize extractor
extractor = PayoffExtractor()

# Extract information from PDF
result = extractor.extract_from_pdf("term_sheet.pdf")

# Print results
import json
print(json.dumps(result, indent=2, ensure_ascii=False))
```

## Output Format

Extraction results are output in JSON format, containing all payoff-related information, automatically organized by the LLM based on the document content.
