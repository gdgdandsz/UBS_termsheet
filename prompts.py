"""
Prompt templates for extracting payoff information from term sheets
"""

# Main extraction prompt template
PAYOFF_EXTRACTION_PROMPT_TEMPLATE = """Can you accurately extract all payoff-related information for me?

Please extract all payoff-related information from the following document, including:
- Fixed Coupon: amount, payment date, calculation formula
- Conditional Coupons: trigger conditions, barrier prices and levels, payment frequency, calculation formulas
- Automatic Early Redemption: trigger conditions, redemption price, valuation dates
- Final Redemption Amount: redemption conditions and amounts under different scenarios
- Knock-in Event: definition, trigger conditions, knock-in price
- Underlyings: reference asset information
- Other payoff-related terms and conditions

Requirements:
1. Use exact wording, numbers, formulas, and percentages from the document
2. Extract completely and accurately, do not miss important information
3. If information does not exist, do not include that field (do not write "Not specified" or "未指定")
4. Organize information in clear JSON format, can be categorized logically

Document Text:
{document_text}

Please return a valid JSON object containing all extracted payoff-related information."""

# Section-specific extraction prompt
SECTION_EXTRACTION_PROMPT_TEMPLATE = """Can you accurately extract all payoff-related information from this section for me?

Section Name: {section_name}

Section Content:
{section_text}

Please extract all numerical values, percentages, dates, formulas, and conditions related to payoff. Use exact wording from the document.

Return a clear JSON object containing all extracted information."""

# Validation prompt
VALIDATION_PROMPT_TEMPLATE = """Please review the following extracted data and verify its accuracy and completeness against the original document text.

Extracted Data:
{extracted_data}

Original Text Excerpt:
{original_text}

Please check for accuracy, completeness, and any missing information. If you find discrepancies or missing information, please provide the corrected and complete data in JSON format."""


def get_payoff_extraction_prompt(document_text: str) -> str:
    """Generate payoff extraction prompt"""
    return PAYOFF_EXTRACTION_PROMPT_TEMPLATE.format(document_text=document_text)


def get_section_extraction_prompt(section_text: str, section_name: str) -> str:
    """Generate section extraction prompt"""
    return SECTION_EXTRACTION_PROMPT_TEMPLATE.format(
        section_text=section_text,
        section_name=section_name
    )


def get_validation_prompt(extracted_data: str, original_text: str) -> str:
    """Generate validation prompt"""
    return VALIDATION_PROMPT_TEMPLATE.format(
        extracted_data=extracted_data,
        original_text=original_text
    )

