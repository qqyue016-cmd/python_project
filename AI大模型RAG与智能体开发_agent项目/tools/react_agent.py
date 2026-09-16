from langchain.agents import create_agent
from utils.prompt_loader import load_system_prompt
from tools.agent_tools import rag_summarize,get_weather,get_external_data,get_user_id,get_user_location,get_current_month,fetch_external_data,fill_context_for_report
from tools.middleware import log_before_model,monitor_tools,report_prompt_switch
from model.factory import chat_model

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            tools=[rag_summarize,get_weather,get_user_id,get_user_location,get_current_month,fetch_external_data,fill_context_for_report],
            middleware=[log_before_model,monitor_tools,report_prompt_switch],
            system_prompt=load_system_prompt(),
        )

    def execute_stream(self,query: str):
        input_dict={
            'messages':[
                {'role':'user','content':query}
            ]
        }

        for chunk in self.agent.stream(input_dict,stream_mode='values',context={'report':False}):
            lastest_message = chunk['messages'][-1]
            if lastest_message:
                yield lastest_message.content.strip() + '\n'


if __name__ == '__main__':
    r = ReactAgent()
    for chunk in r.execute_stream('帮我生成一份我的使用报告'):
        print(chunk,end='',flush=True)