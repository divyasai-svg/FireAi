# AI usage note

AI assistance was used to scaffold the repository, explain the assignment, and review detector boundaries. The submitted detector logic remains ordinary Python and is intentionally readable.

The offline runner does not call a network model, so it is reproducible without credentials. The `llm_review` function is the seam for the free-tier Gemini implementation. In production it should:

1. receive only candidate rows and the detector evidence;
2. request strict JSON (`problem`, `confirmed`, `evidence_fields`, `confidence`, `reason`);
3. reject malformed or unsupported labels;
4. log model/version/prompt hash and latency;
5. retain the original row plus the model response for audit;
6. fall back to the deterministic finding on timeout or parse failure.

One useful failure caught by this design is that an LLM can call a description “resolved” merely because the word appears in `Resolution Description`, even when `Status=Open`; the state rule catches the contradiction without trusting the model. Another is that a model can silently normalize malformed ZIP values; the schema rule preserves the raw value and fails closed.
