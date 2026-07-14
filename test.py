# ruff: noqa: I001
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "camel-prompt-injection" / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from typing import cast
from inspect_ai import eval
from inspect_evals.agentdojo import agentdojo
from pydantic_ai.models import KnownModelName
from approvals import Approvals
from defences import Solvers

user_tasks = [0, 27]
injection_tasks = [0, 3, 8]

for model in ["google/gemini-3.1-flash-lite"]:
    app = Approvals(model)
    model_name = cast(KnownModelName, ":".join(model.split("/")))
    solver = Solvers(model_name)

    eval(
        agentdojo(
            workspace="workspace",
            user_task_ids=user_tasks,
            injection_task_ids=injection_tasks,
        ),
        model=model,
        log_dir="./logs",
        # approval=app.Judge(),
        solver=solver.CaMeL(),
    )
