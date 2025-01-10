from langchain_openai import ChatOpenAI

api_key = None
base_url = None

generalLLM: ChatOpenAI = ChatOpenAI(
    model="qwen-turbo",
    api_key=api_key,
    base_url=base_url,
)
coderLLM: ChatOpenAI = ChatOpenAI(
    model="qwen-coder-turbo",
    api_key=api_key,
    base_url=base_url,
)
