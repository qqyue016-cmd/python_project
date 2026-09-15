
'''
日志处理工具
'''
from datetime import datetime
import logging
import os
from utils.path_tool import get_abs_path

# 日志保存的根目录
LOG_ROOT = get_abs_path('logs')

# 确保保存目录存在
os.makedirs(LOG_ROOT,exist_ok=True)

# 配置日志格式
DEFAULT_LOG_FORMAT = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
)

def get_logger(
        name:str='agent',
        console_level = logging.INFO,
        file_level = logging.DEBUG,
        log_file = None\

) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加Handler
    if logger.handlers:
        return logger

    # 配置控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    if not log_file: # 创建日志文件
        log_file = os.path.join(LOG_ROOT, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')

    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = get_logger()

if __name__ == '__main__':
    logger.info('This is an info message')