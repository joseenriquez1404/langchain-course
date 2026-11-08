# langchain-course

Exercises from a LangChain course on Udemy. The current branch, `agents-under-the-hood`, builds a tool-calling agent by hand, without `create_agent`, so the loop is visible.

## What's in `main.py`

A shopping assistant that uses Gemini (`google_genai:gemini-3.5-flash-lite`, temperature 0) and two tools:

| Tool | Purpose |
|---|---|
| `get_product_price(product)` | Looks up a price in a hardcoded catalog (`laptop`, `headphones`, `keyboard`). Returns `0.0` for unknown products. |
| `apply_discount(price, discount_tier)` | Applies a `bronze` (5%), `silver` (12%) or `gold` (23%) discount and returns the rounded price. |

`run_agent(question)` runs the loop manually, for up to `MAX_ITERATIONS` (10):

1. Send the messages to the model with the tools bound.
2. If the reply has no tool calls, return it as the final answer.
3. Otherwise run the first tool call and append the `AIMessage` and a `ToolMessage` with the result.
4. Repeat.

The system prompt forces the model to fetch the real price first, never calculate discounts itself, and ask for a tier if none is given. The function is decorated with `@traceable`, so runs show up in LangSmith as "LangChain Agent Loop".

Only the first tool call of each model reply is executed. Parallel tool calls are ignored.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file with your keys:

```
GOOGLE_API_KEY=...
# Optional, for LangSmith tracing
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=...
```

## Run

```bash
uv run main.py
```

The default question is "What is the price of a laptop with a silver discount?". Expected result: 1299.99 with 12% off, which is 1143.99.

## Layout

- `main.py`: the agent loop.
- `src/langchain_course/`: package skeleton created by `uv init`.
- `static/`: LangChain and LangGraph logos.
- `pyproject.toml`, `uv.lock`: dependencies (`langchain[google-genai]`, `langchain-google-genai`, `dotenv`, `black`, `isort`).
