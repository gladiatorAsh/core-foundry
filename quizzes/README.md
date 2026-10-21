# Question bank

One JSON file per topic. Both quiz front-ends (the `tools/quiz.py` CLI and `quiz.html`) read these.

| File | Topic |
|---|---|
| `genai.json` | GenAI & LLM system design (RAG, serving, agents, evals, fine-tuning, safety) |
| `coding.json` | Coding pattern recognition & complexity |
| `system-design.json` | Distributed system design |
| `ml-system-design.json` | ML system design & experimentation |
| `ml-fundamentals.json` | Classical ML & deep learning |
| `llm-fundamentals.json` | Transformers & LLMs |
| `stats.json` | Probability & statistics |
| `behavioral.json` | Behavioral, Amazon LPs, loop strategy |
| `full-stack.json` | Full-stack: JS/TS, React, Angular, Redux, D3, HTML/CSS, Node.js, .NET, Python, APIs, SQL, security, Azure, AWS, data stores, Docker, Postman |

## Schema

```json
{
  "topic": "genai",
  "title": "GenAI & LLM system design",
  "questions": [
    {
      "id": "genai-001",
      "type": "mcq",
      "question": "…",
      "options": ["…", "…", "…", "…"],
      "answer": 2,
      "explanation": "Why the right answer is right (and the others aren't).",
      "difficulty": 2,
      "tags": ["rag", "retrieval"],
      "ref": "04-genai-system-design/rag.md"
    },
    {
      "id": "genai-014",
      "type": "card",
      "question": "Name the stages of a RAG ingestion pipeline.",
      "answer": "Connectors → parsing → chunking → …",
      "difficulty": 1,
      "tags": ["rag"],
      "ref": "04-genai-system-design/rag.md"
    }
  ]
}
```

- `answer` is the **0-based index** into `options` for MCQs, or the answer text for flashcards (`card`).
- `difficulty`: 1 = core, 2 = expected at Senior/Staff, 3 = deep cut.
- `ref` must point to an existing file in this repo (the validator checks it).
- **IDs must stay stable.** Your spaced-repetition progress is keyed by ID. Append new questions with new IDs; don't renumber.

## Adding questions

1. Add entries to the right file (new IDs at the end).
2. `python tools/validate.py`
3. `python tools/build_web_quiz.py` (refreshes `quiz.html`)

Good habit: whenever a mock interview exposes a gap, write one MCQ and one flashcard about it the same day.
