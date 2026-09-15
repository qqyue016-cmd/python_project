from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description='获取体重，返回整数，单位kg')
def get_weight():
    return 70

@tool(description='获取身高，返回整数，单位cm')
def get_height():
    return 175

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    system_prompt='''你是一个严格遵守ReAct框架的智能助手，必须按[思考、行动、观察、在思考]的流程解决问题
        且每轮只能调用一个工具，禁止单轮调用多个工具
        并告知我你的思考过程，工具调用原因，按思考、行动、观察三个结构告知我
        ''',
    tools=[get_weight, get_height]
)

for chunk in agent.stream(
        {"messages":[{"role": "user", "content": '计算我的BMI'}]},
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