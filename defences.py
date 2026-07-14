# ruff: noqa: I001
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "camel-prompt-injection" / "src"))
sys.path.insert(0, str(Path(__file__).parent))

import json

from analyse_tools import Tools

from agentdojo import attacks, benchmark, logging
from agentdojo.task_suite import get_suite
from camel.interpreter.interpreter import MetadataEvalMode
from camel.models import make_tools_pipeline
from inspect_ai.solver import Generate, TaskState, solver
from pydantic_ai.models import KnownModelName


class Solvers:
    def __init__(self, model: KnownModelName):
        self.model = model

    @solver
    def CaMeL(self):
        async def solve(state: TaskState, generate: Generate):
            attack_name = "important_instructions"
            tools_pipeline = make_tools_pipeline(
                self.model,
                False,
                False,
                attack_name,
                "medium",
                None,
                "workspace",
                None,
                MetadataEvalMode.NORMAL,
                None,
            )

            suite = get_suite("v1.2", "workspace")
            attack = attacks.load_attack(attack_name, suite, tools_pipeline)

            user_task_id = "user_task_" + state.metadata["task_id"]
            injection_task_id = "injection_task_" + state.metadata["injection_task_id"]
            user_task = suite.get_user_task_by_id(user_task_id)

            logdir = Path("log-camel")
            logdir.mkdir(exist_ok=True)

            with logging.OutputLogger(str(logdir)):
                benchmark.run_task_with_injection_tasks(
                    suite,
                    tools_pipeline,
                    user_task,
                    attack,
                    logdir,
                    False,
                    [injection_task_id],
                    "v1.2",
                )

            model = str(self.model).split(":")[1]
            filename = f"log-camel/{model}+camel/workspace/{user_task_id}/important_instructions/{injection_task_id}.json"

            with open(filename, "r") as f:
                messages = json.load(f)["messages"]

            messages = Tools.agent_dojo_to_inspect_ai(messages)

            state.messages.clear()
            state.messages.extend(messages)
            if messages:
                state.output.completion = messages[-1].content
            else:
                state.output.completion = ""

            return state

        return solve
