# RESULTS B — LLM-Based Income Tax Engine

## 1. Objective
Evaluate two LLM-based approaches for answering Indian income tax queries using the Google Gemini API.

## 2. Approach 1: LLM Query-Time
- Tax rules are loaded from a JSON file for every query.
- Rules and user input are included in the Gemini prompt.
- Gemini generates the tax explanation and response.
- Missing information can trigger clarification.

## 3. Approach 2: LLM Compiled-Rules
- Tax rules are sent to Gemini for compilation.
- The compiled output is saved as JSON.
- Future queries reuse the saved compiled rules.
- This avoids repeating the rule compilation step for every query.

## 4. Evaluation Results

### LLM Query-Time
- Total test cases: 10
- Successful responses: 10
- Failed responses: 0
- Response success rate: 100%
- Average latency: 17.325 seconds

### LLM Compiled-Rules
- Total test cases: 10
- Successful responses: 10
- Failed responses: 0
- Response success rate: 100%
- Average latency: 23.194 seconds

### Overall Observations
- All 20 Gemini API requests completed successfully.
- Query-Time had a lower average latency in this evaluation.
- API cost was not measured.
- Tax calculation accuracy is pending independent validation.

## 5. Limitations
- LLM responses can be inconsistent.
- API availability and quota limits can affect execution.
- Incomplete source tax rules can produce incomplete calculations.
- The supplied LLM rules do not include all applicable provisions, such as Section 87A rebate and cess.
- Compiled rules require validation before production use.
- A successful API response does not guarantee a legally accurate tax calculation.

## 6. Conclusion
Both LLM approaches successfully completed all 10 test cases in the current evaluation. Query-Time showed lower average latency than Compiled-Rules. However, tax accuracy, API cost and consistency require further evaluation before deciding which approach is more suitable.