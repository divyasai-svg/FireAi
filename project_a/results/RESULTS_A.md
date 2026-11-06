
# RESULTS A — Rules-Based Income Tax Engine

## 1. Objective
Build a deterministic income tax calculator using hand-coded tax rules for FY 2024-25 (AY 2025-26).

## 2. Implementation
- Python-based rules engine.
- JSON file for tax slabs and standard deductions.
- Decimal arithmetic for tax calculations.
- Separate functions for tax slabs, deductions, rebate, surcharge and cess.
- Natural-language input parser.
- Clarification when required information is missing.

## 3. Test Dataset
- 200 generated test cases.
- Old and new tax regimes.
- Different salary ranges.
- Resident and non-resident scenarios.

## 4. Evaluation
Accuracy: Pending validation against official tax calculations.

Latency: To be measured.

Determinism: Expected to produce the same output for identical inputs.

## 5. Limitations
- Tax rules must be manually updated.
- Input parser supports limited language patterns.
- Legal eligibility conditions require further validation.
- Generated test cases are not independently verified tax answers.

## 6. Conclusion
The rules-based approach provides predictable and traceable calculations when the implemented tax rules and input data are correct.
