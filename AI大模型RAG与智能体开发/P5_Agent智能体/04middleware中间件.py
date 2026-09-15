"""
P5 - 04 Agent 中间件(Middleware) —— 完整示例

两类 hook：
  ① before/after 型：在固定节点前后执行（观察/改状态）
  ② wrap 型：把"模型调用/工具调用"整体包一层（计时、重试、短路、篡改入参）
"""
import time
from langchain.agents import create_agent
from langchain.agents.middleware import (
    before_agent, after_agent, before_model, after_model,
    wrap_model_call, wrap_tool_call,
)
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool


# ==================== 1. 工具 ====================
@tool(description='查询股票价格')
def get_stock_price(stock_name: str) -> str:
    """查询指定股票的当前价格"""
    return f"{stock_name}的股票价格是10元"


@tool(description='查询股票信息')
def get_info(stock_name: str) -> str:
    """查询指定股票的公司信息"""
    return f"股票{stock_name}，是一家上市公司，专注于IT职业教育"


# ==================== 2. before/after 型 ====================
@before_agent
def on_agent_start(state, runtime):
    print('\n' + '=' * 50)
    print('[before_agent] Agent 开始执行')
    return None


@after_agent
def on_agent_end(state, runtime):
    print(f'[after_agent] 结束，最终回答: {state["messages"][-1].content}')
    print('=' * 50 + '\n')
    return None


@before_model
def on_before_model(state, runtime):
    last = state['messages'][-1]
    print(f'[before_model] 模型将看到: {type(last).__name__}', end='')
    if getattr(last, 'tool_call_id', None):  # ToolMessage = 工具执行结果
        print(f' (工具结果: {last.content[:30]})')
    else:
        print()
    return None


@after_model
def on_after_model(state, runtime):
    last = state['messages'][-1]
    if getattr(last, 'tool_calls', None):
        print(f'[after_model] 模型决定调用工具: {[tc["name"] for tc in last.tool_calls]}')
    else:
        print(f'[after_model] 模型输出: {last.content[:40]}')
    return None


# ==================== 3. wrap 型 ====================
# wrap_model_call: 把"一次模型调用"整个包住 —— handler(request) 才是真正调模型
@wrap_model_call
def time_model_call(request, handler):
    start = time.time()
    response = handler(request)          # 真正执行模型调用（可调多次=重试，跳过=短路）
    print(f'[wrap_model_call] 本次模型调用耗时 {time.time()-start:.1f}s')
    return response


# wrap_tool_call: 把"一次工具调用"整个包住 —— request.tool / request.tool_call 可读
@wrap_tool_call
def watch_tool_call(request, handler):
    tool_name = request.tool.name                     # 工具名
    args = request.tool_call.get('args', {})          # 工具入参
    print(f'[wrap_tool_call] 调用工具 [{tool_name}]，参数: {args}')
    try:
        response = handler(request)                   # 真正执行工具
        return response
    except Exception as e:
        print(f'[wrap_tool_call] 工具调用失败: {e}'),
        raise


# ==================== 4. 组装并运行 ====================
agent = create_agent(
    model=ChatTongyi(model='qwen3-max', streaming=True),
    system_prompt='你是一个股票问答智能助手，请使用工具回答用户关于股票的问题',
    tools=[get_info, get_stock_price],
    # 多个中间件按列表顺序从外到内嵌套（洋葱模型）
    middleware=[
        on_agent_start,
        time_model_call,   # 模型调用 → 先过这层（计时）
        watch_tool_call,   # 工具调用 → 先过这层（日志）
        on_before_model, on_after_model,
        on_agent_end,
    ]
)

if __name__ == '__main__':
    res = agent.invoke({
        'messages': [{'role': 'user', 'content': '传智教育的股价是多少？帮我查询一下'}]
    })
    print('\n最终返回:', res['messages'][-1].content)
