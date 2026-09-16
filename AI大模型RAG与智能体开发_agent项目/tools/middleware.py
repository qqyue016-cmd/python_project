from typing import Callable
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt
from langchain.agents.middleware.types import ModelRequest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command
from langgraph.runtime import Runtime
from utils.logger_handler import logger
from utils.prompt_loader import load_report_prompt,load_system_prompt





@wrap_tool_call
def monitor_tools(
        request: ToolCallRequest, # 请求的数据封装
        handler:Callable[[ToolCallRequest], ToolMessage | Command ] # 调用的函数本身
) -> ToolMessage | Command:
    logger.info(f"[monitor tool]执行工具: {request.tool_call['name']}")
    logger.info(f"[monitor tool]传入参数: {request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[monitor tool]工具{request.tool_call['name']}调用成功")
        if request.tool_call['name'] == 'fill_context_for_report':
            request.runtime.context['report']=True

        return result
    except Exception as e:
        logger.error(f"[monitor tool]工具{request.tool_call['name']}调用出错: {str(e)}")
        raise e

@before_model
def log_before_model(
        state:AgentState,
        runtime:Runtime
):
    logger.info(f'[log_before_model]即将调用模型，带有{len(state['messages'])}条信息')
    logger.debug(f'[log_before_model]{type(state['messages'][-1].content).__name__} {state['messages'][-1].content.strip()}')
    return None

@dynamic_prompt
def report_prompt_switch(request:ModelRequest):
    is_report = request.runtime.context.get('report',False)
    if is_report:
        return load_report_prompt()
    return load_system_prompt()