# DECISION MATRIX — Income Tax Engine

## 1. Comparison

| Evaluation Criteria | Rules-Based | LLM Query-Time | LLM Compiled-Rules |
|---|---|---|---|
| Test cases | 200 | 10 | 10 |
| Execution success | 200/200 | 10/10 | 10/10 |
| Tax accuracy | Pending validation | Pending validation | Pending validation |
| Determinism | High for identical inputs | May vary | May vary |
| Average latency | Not measured | 17.325 seconds | 23.194 seconds |
| API cost | No API cost | Not measured | Not measured |
| Traceability | High | Depends on explanation | Depends on compiled rules |
| Rule updates | Manual code/data update | Update source rules | Recompile rules |

## 2. Advantages

### Rules-Based
- Predictable calculations.
- No external API dependency.
- Easy to trace calculation steps.

### LLM Query-Time
- Flexible natural-language interaction.
- Rules are supplied at query time.
- No separate rule compilation step is required.

### LLM Compiled-Rules
- Reuses previously compiled rules.
- Avoids repeating the compilation step.
- Can reduce repeated prompt size.

## 3. Limitations
- Rules-based systems require manual maintenance.
- LLM responses can be inconsistent.
- API quota and availability can affect execution.
- Compiled rules must be checked against official provisions.
- Successful execution does not establish tax accuracy.

## 4. Current Evaluation Observations
- Rules-based evaluator: 200/200 successful cases.
- Parser evaluator: 50/50 correct cases.
- LLM Query-Time: 10/10 successful API responses.
- LLM Compiled-Rules: 10/10 successful API responses.
- Query-Time average latency was lower than Compiled-Rules in the current test run.
- Tax accuracy and API cost still require independent evaluation.

## 5. Final Decision
A final production recommendation cannot be made until all three approaches are evaluated against the same independently validated tax calculations.

The rules-based approach offers predictable and traceable execution. LLM approaches offer flexible natural-language interaction but require additional validation of their tax calculations.