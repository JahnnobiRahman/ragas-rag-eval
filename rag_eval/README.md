## Retrieval-Augmented Generation System with Structured Evaluation (Ragas 0.3)

A system-level implementation of Retrieval-Augmented Generation (RAG) with **experiment-driven evaluation** using **Ragas 0.3**.

This repository demonstrates how modern AI systems should be built: **observable, measurable, and architecturally transparent**.

## Overview

This project implements a minimal RAG pipeline from scratch and integrates it with the Ragas experimentation framework.

The purpose is to:

- **Build** a transparent retrieval + generation architecture
- **Introduce** structured observability at each system stage
- **Integrate** reproducible evaluation workflows
- **Diagnose** failure modes systematically
- **Benchmark** architectural improvements using controlled experiments

This is not a prompt demo. It is a system engineering + evaluation demonstration.

## System architecture

### Retrieval layer (current)

- **Document store**: in-memory list of documents (see `rag.py`)
- **Retriever**: keyword overlap scoring
- **Ranking**: deterministic top-\(k\)

Scoring logic:

\[
score = |\text{query\_words} \cap \text{document\_words}|
\]

Design goals:

- Full transparency
- Deterministic behavior
- Debuggable failure modes
- No hidden embedding abstractions

Planned extension:

- Embedding-based retrieval (FAISS / Chroma)
- Cosine similarity
- Retrieval precision/recall benchmarking

### Generation layer (current)

- **Model**: OpenAI `gpt-4o` (see `rag.py` and `evals.py`)
- **Prompting**: explicit context injection with a structured template
- **Context assembly**: controlled top-\(k\) docs
- **LLM metadata**: prompt/context lengths and token usage logged in traces

Prompt template (conceptually):

```
Answer the following question based on the provided documents:
Question: {query}
Documents:
{context}
Answer:
```

### Observability layer (current)

Each query execution produces a structured trace capturing:

- Retrieval start/completion
- Similarity scores + retrieved doc IDs
- Prompt/context length
- Model metadata + token usage (when available)
- Error events

Traces are stored under `evals/logs/` as JSON.

## Evaluation framework (Ragas 0.3)

Evaluation is treated as a first-class system component.

### Dataset + experiment pipeline

The evaluation workflow (`evals.py`) uses:

- `ragas.Dataset` (backed by local CSV storage under `evals/`)
- `@experiment()` runs that call the RAG client and score outputs
- A discrete metric (`DiscreteMetric`) producing **pass/fail** based on grading notes

Output format (conceptually):

`question | grading_notes | response | score | log_file`

Experiment artifacts are stored under `evals/experiments/` (CSV).

### Failure mode taxonomy

The system distinguishes three failure categories:

- **Coverage failure**: required knowledge does not exist in the document store
- **Retrieval failure**: knowledge exists but is not retrieved
- **Generation failure**: correct context is retrieved but reasoning fails

Because each run logs retrieval scores + the full trace, you can isolate which class of failure occurred.

## Quickstart

### Requirements

- Python **3.9+**
- An OpenAI API key

### 1) Create and activate a virtual environment

From the `rag_eval/` directory:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -U pip
pip install -e .
```

### 3) Set your API key

```bash
export OPENAI_API_KEY="your-openai-key"
```

### 4) Run the evaluation experiment

```bash
python evals.py
```

You should see:

- Trace JSON files written to `evals/logs/`
- An experiment CSV written under `evals/experiments/`

## Working with datasets

### Local dataset storage

`evals.py` uses a local CSV-backed Ragas dataset under `evals/datasets/`. You can:

- Edit `load_dataset()` in `evals.py` to add/modify questions and grading notes
- Or edit the CSV directly if you prefer file-driven iteration

### Optional: fetch Ragas docs for local grounding

There’s a helper script at `evals/datasets/fetch_docs.py` that downloads a few Ragas documentation pages into:

- `evals/datasets/ragas_docs/`

Run it from the project root:

```bash
python evals/datasets/fetch_docs.py
```

## Project structure

```
rag_eval/
├── README.md
├── pyproject.toml
├── rag.py
├── evals.py
├── __init__.py
└── evals/
    ├── datasets/
    │   ├── fetch_docs.py
    │   └── test_dataset.csv
    ├── experiments/
    └── logs/
```

## Engineering insight from initial experiments

Early experiment runs can surface systematic failures that look like “LLM mistakes” but are actually system issues. A common pattern:

- The evaluation dataset references knowledge not present in the knowledge base.
- The retriever returns no relevant documents (correct behavior).
- The model reports insufficient context.
- The metric scores the response as a failure.

Conclusion: this is a **knowledge base coverage mismatch**, not hallucination, retrieval error, or generation instability.

## Roadmap

### Phase 1 — Knowledge base expansion

- Ingest structured documentation
- Paragraph-level chunking
- Better context granularity

### Phase 2 — Embedding retrieval

- Replace keyword scoring
- Introduce semantic similarity
- Benchmark retrieval improvements using Ragas metrics

### Phase 3 — Advanced evaluation

- Multi-metric scoring
- Retrieval relevance scoring
- Regression benchmarking across architecture versions
- Agent workflow evaluation

## Design principles

- Observability before optimization
- Evaluation before scaling
- Diagnosis before prompt tuning
- Architecture before abstraction
- Reproducibility over heuristics

## Notes

- **Do not commit secrets**: keep API keys in environment variables (or a local `.env` that is gitignored).
- **Docs**: see Ragas documentation at `https://docs.ragas.io`.
