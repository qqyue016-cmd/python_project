from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi


@tool(description='查询天气')
def get_weather(city: str) -> str:
    return f"{city}的天气是晴天"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    system_prompt='你是一个ai智能助手',
    tools=[get_weather]
)

res = agent.invoke(
    {
        'messages': [
            {'role': 'user', 'content': '深圳今天天气怎么样'}
        ]
    }
)

for msg in res['messages']:
    print(type(msg).__name__, msg.content)
