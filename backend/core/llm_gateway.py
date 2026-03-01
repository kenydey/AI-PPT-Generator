"""
大模型网关 - 基于 LiteLLM 的统一多模型调用
支持 gpt-4o, gemini/gemini-1.5-pro, ollama/llama3, deepseek/deepseek-chat 等
"""
import litellm
from litellm import completion


async def generate_response(model_name: str, messages: list[dict]) -> str:
    """
    统一异步调用，返回模型回复文本。
    model_name 示例: gpt-4o, gemini/gemini-1.5-pro, ollama/llama3, deepseek/deepseek-chat
    """
    response = await completion(
        model=model_name,
        messages=messages,
    )
    return response.choices[0].message.content or ""
