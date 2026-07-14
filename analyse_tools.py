__all__ = ["Tools"]

import os

import anthropic
import openai
from agentdojo import agent_pipeline
from google import genai
from inspect_ai.model import ChatMessageAssistant, ChatMessageTool, ChatMessageUser
from inspect_ai.tool import ToolCall


class Tools:
    @classmethod
    def _make_llm(cls, model: str) -> agent_pipeline.BasePipelineElement:
        if "google" in model:
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            llm = agent_pipeline.GoogleLLM(
                model.split(":")[1], client, max_tokens=65535
            )
        elif "openai" in model:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            llm = agent_pipeline.OpenAILLM(client, model.split(":")[1], None)
        elif "anthropic" in model:
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            llm = agent_pipeline.AnthropicLLM(
                client, model.split(":")[1], max_tokens=8192
            )
        else:
            raise ValueError(f"Unsupported model: {model}")
        llm.name = model.split(":")[1]
        return llm

    @classmethod
    def agent_dojo_to_inspect_ai(cls, updated_messages):
        def convert_tool_calls(ad_tool_calls):
            if not ad_tool_calls:
                return None

            tool_calls = []
            for tc in ad_tool_calls:
                tool_calls.append(
                    ToolCall(
                        id=str(tc["id"]) or "",
                        arguments=tc["args"] or {},
                        function=tc["function"],
                    )
                    or ""
                )

            return tool_calls

        messages = []
        for msg in updated_messages:
            role = msg["role"]
            raw_content = msg.get("content", []) or []
            # Универсальная сборка текста
            text = "\n".join(b["content"] for b in raw_content if b.get("content"))

            if role == "user":
                messages.append(ChatMessageUser(content=text))
            elif role == "assistant":
                messages.append(
                    ChatMessageAssistant(
                        content=text,
                        tool_calls=convert_tool_calls(msg.get("tool_calls")),
                    )
                )
            elif role == "tool":
                tool_call_info = msg.get("tool_call")
                func_name = (
                    tool_call_info.get("function")
                    if isinstance(tool_call_info, dict)
                    else None
                )

                messages.append(
                    ChatMessageTool(
                        content=text,
                        tool_call_id=msg.get("tool_call_id"),
                        function=func_name,
                    )
                )

        return messages

    @classmethod
    def inspect_ai_to_agent_dojo(cls, inspect_messages):
        ad_messages = []
        for msg in inspect_messages:
            role = msg.role
            content = getattr(msg, "content", "")
            content_blocks = [{"type": "text", "content": content}] if content else []

            if role == "user":
                ad_messages.append({"role": "user", "content": content_blocks})
            elif role == "assistant":
                ad_call = None
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    ad_call = [
                        {"function": tc.function, "args": tc.arguments, "id": tc.id}
                        for tc in msg.tool_calls
                    ]
                ad_messages.append(
                    {
                        "role": "assistant",
                        "content": content_blocks,
                        "tool_calls": ad_call,
                    }
                )
            elif role == "tool":
                ad_messages.append(
                    {
                        "role": "tool",
                        "content": content_blocks,
                        "tool_call_id": msg.tool_call_id,
                    }
                )
        return ad_messages
