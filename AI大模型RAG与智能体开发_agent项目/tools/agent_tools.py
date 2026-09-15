from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import random
from utils.config_handler import load_agent
from utils.path_tool import get_abs_path
import os
from utils.logger_handler import logger

rag = RagSummarizeService()

external_data = {}
user_ids = ['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010']
month_arr = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12']

@tool(description='从向量存储中检索相关资料')
def rag_summarize(query):
    return rag.rag_summarize(query)

@tool(description='获取用户当地天气')
def get_weather(city: str):
    return f"{city}的天气是晴天,气温26摄氏度，湿度50%，南风一级，AQI21，最近6小时降雨概率极低"

@tool(description='获取用户定位')
def get_user_location() ->str:
    return random.choice(["北京", "合肥", "深圳", "杭州"])

@tool(description='获取用户ID')
def get_user_id() ->str:
    return random.choice(user_ids)

@tool(description='获取当前月份')
def get_current_month() ->str:
    return random.choice(month_arr)

def get_external_data():
    if not external_data:
        external_data_path = get_abs_path(load_agent['external_data_path'])
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f'外部系统{external_data_path}文件不存在')

        with open(external_data_path, 'r',encoding=' utf-8') as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(',')

                user_id = arr[0].replace('"','')
                feature = arr[1].replace('"','')
                efficiency = arr[2].replace('"','')
                consumables = arr[3].replace('"','')
                comparison = arr[4].replace('"','')
                time = arr[5].replace('"','')

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    'feature': feature,
                    'efficiency': efficiency,
                    'consumables': consumables,
                    'comparison': comparison
                }

@tool(description='从外部系统中用户在特定月份的使用记录，一存字符串返回，如未检索到则返回空字符串')
def fetch_external_data(user_id: str,month: str):
    get_external_data()

    try:
        return f'用户{user_id}在{month}的使用记录：{external_data[user_id][month]}'
    except KeyError as e:
        logger.warning(f'[fetch_external_data]未找到用户{user_id}在{month}的使用记录')
        return ''

if __name__ == '__main__':
    print(fetch_external_data('1001','2025-01'))