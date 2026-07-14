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

## Acknowledgements & Original Sources

This project integrates code and concepts from the following open-source repositories. We are grateful to their authors and maintainers for their foundational work.

1.  **[UK Government BEIS - Inspect Evals](https://github.com/UKGovernmentBEIS/inspect_evals.git)**
    The primary source for evaluation frameworks and methodologies used in this project.

2.  **[Google Research - Camel Prompt Injection](https://github.com/google-research/camel-prompt-injection.git)**
    Provides critical insights and datasets related to prompt injection vulnerabilities and robustness testing.

3.  **[Microsoft - Fides](https://github.com/microsoft/fides.git)**
    Serves as a key reference for privacy engineering and ethical data handling practices.

We do not claim ownership of these external resources. All rights and credits belong to their respective owners.