# Prompt Injection Defense Research: CaMeL + Inspect AI

## Overview

Implementation and testing of the **CaMeL** defense (from the `camel-prompt-injection` library) against prompt injection attacks on LLM agents, integrated into the **Inspect AI** framework using the **AgentDojo** benchmark.

## What was done

- **CaMeL + Inspect AI integration** — `defences.py` wraps the CaMeL pipeline as an Inspect solver and converts messages between AgentDojo and Inspect AI formats.
- **Test script** — `test.py` runs evaluation on the AgentDojo benchmark (workspace, selected user/injection tasks) with `google/gemini-3.1-flash-lite` model using CaMeL defense.
- **Conversion utility** — `analyse_tools.py` implements bidirectional message conversion (`agent_dojo_to_inspect_ai`, `inspect_ai_to_agent_dojo`) and supports Google/OpenAI/Anthropic models.

## Structure

```
test.py              — entry point, runs eval
defences.py          — CaMeL solver for Inspect AI
analyse_tools.py     — message converter between AgentDojo and Inspect AI
camel-prompt-injection/ — CaMeL library (external dependency)
```

## Usage

```bash
source .venv/bin/activate
python test.py
```

Model is set via the `model` variable in `test.py`. Results are logged to `./logs`.
