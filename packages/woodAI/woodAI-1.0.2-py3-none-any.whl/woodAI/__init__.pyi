__all__ = ['chat_set', 'chat', 'chat_clear']

# chatbot的初始化设定
def chat_set(
    system_role: str = '', turn_count: int = 3
) -> None:
    pass

# 进入对话
def chat(
    prompt: str
) -> str:
    pass

# 清空上下文关联记录
def chat_clear() -> None:
    pass
