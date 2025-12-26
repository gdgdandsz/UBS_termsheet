# Project Structure

## 📁 Complete File List

```
UBS_FinAI/
│
├── 📖 Documentation
│   ├── README.md                      # Main project documentation
│   ├── README_PAYOFF_READY.md         # Technical deep-dive
│   ├── SETUP.md                       # Installation & setup guide
│   ├── GITHUB_UPLOAD_GUIDE.md         # How to upload to GitHub
│   ├── PROJECT_STRUCTURE.md           # This file
│   └── LICENSE                        # MIT License
│
├── ⚙️ Configuration
│   ├── .gitignore                     # Git ignore rules
│   ├── requirements.txt               # Python dependencies
│   └── config.py                      # Configuration loader
│
├── 📄 Core Extraction
│   ├── prompts.py                     # Main extractor (with post-processing)
│   ├── prompt.py                      # LLM prompt templates
│   ├── llm_client.py                  # LLM API client (OpenAI/Anthropic/DeepSeek)
│   └── document_loader.py             # PDF loading utilities
│
├── 🛡️ Validation & Testing
│   ├── payoff_ready_validator.py      # Safety validation layer
│   ├── compare_with_ground_truth.py   # Accuracy evaluation
│   ├── test.py                        # Main test suite
│   ├── test_case.py                   # Test case definitions
│   └── test_payoff_engines.py         # Payoff engine tests
│
├── 🧮 Payoff Calculation
│   ├── payoff_single.py               # Single underlying Phoenix
│   ├── payoff_worst_of.py             # Worst-of Phoenix
│   └── calculate_payoff_from_json.py  # JSON → Payoff pipeline
│
└── 📊 Sample Data (optional to upload)
    ├── BNP-PhoenixSnowball-SP500-XS1083630027-TS.pdf
    ├── IT0006764473-TS.pdf
    ├── BNP Phoenix Snowball analysis.pdf
    ├── term_sheet_extraction.pdf
    └── termsheet search keywords.docx
```

## 🔑 Key Files Explained

### Must-Have Files

| File | Purpose | Upload? |
|------|---------|---------|
| `README.md` | Main documentation | ✅ Yes |
| `requirements.txt` | Dependencies | ✅ Yes |
| `.gitignore` | Exclude sensitive files | ✅ Yes |
| `LICENSE` | MIT License | ✅ Yes |
| All `.py` files | Core functionality | ✅ Yes |

### Optional Files

| File | Purpose | Upload? |
|------|---------|---------|
| `*.pdf` | Sample term sheets | ⚠️ Optional |
| `*.docx` | Analysis notes | ⚠️ Optional |
| `*_analysis.pdf` | Documentation | ⚠️ Optional |

### Auto-Excluded (by .gitignore)

| File/Pattern | Reason |
|--------------|--------|
| `LLM_variables.env` | Contains API keys 🔒 |
| `test_results_*.json` | Temporary outputs |
| `payoff_results_*.json` | Temporary outputs |
| `__pycache__/` | Python cache |
| `.DS_Store` | Mac system file |

## 📊 File Statistics

- **Total Python files**: 13
- **Lines of code**: ~1,500+
- **Documentation**: 5 files
- **Tests**: 3 test files
- **Payoff engines**: 2

## 🎯 File Dependencies

```
test.py
  ├── prompts.py
  │   ├── llm_client.py
  │   │   └── config.py
  │   ├── document_loader.py
  │   └── prompt.py
  └── test_case.py

calculate_payoff_from_json.py
  ├── payoff_ready_validator.py
  ├── payoff_single.py
  └── payoff_worst_of.py
```

## 🚀 Quick Start Files

1. **For Users**: Start with `README.md`
2. **For Setup**: Follow `SETUP.md`
3. **For Upload**: Read `GITHUB_UPLOAD_GUIDE.md`
4. **For Technical**: See `README_PAYOFF_READY.md`

---

**Last Updated**: December 26, 2025
