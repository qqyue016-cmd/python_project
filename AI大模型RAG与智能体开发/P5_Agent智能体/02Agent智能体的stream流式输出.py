from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool


@tool(description='查询股票价格')
def get_stock_price(stock_name: str) -> str:
    return f"{stock_name}的股票价格是10元"

@tool(description='查询股票信息')
def get_info(stock_name: str) -> str:
    return f"股票{stock_name}，是一家上市公司，专注于IT职业教育"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    system_prompt='你是一个ai智能助手,可以回答股票的相关问题，记住请告诉我思考过程，让我知道你调用了什么工具',
    tools=[get_info, get_stock_price]
)

for chunk in agent.stream(
        {"messages":[{"role": "user", "content": "传智教育的股价是多少帮我查询一下"}]},
    stream_mode='values'
):
    lastest_msg = chunk['messages'][-1]

    if lastest_msg:
        print(type(lastest_msg).__name__, lastest_msg.content)

    try:
        if lastest_msg.tool_calls:
            for tool_call in lastest_msg.tool_calls:
                print(f'工具调用{[tc["name"] for tc in tool_call.tool_calls]}')
    except AttributeError as e:
        pass