'''
知识库
'''

import os
import config_data as config
import hashlib

def check_md5(md5_str: str):
    '''
    检查传入字符串在md5.txt里是否存在
    :return:
    '''
    # 返回False代表未处理，返回Ture代表已处理
    if not os.path.exists(config.md5_text):
        # if进入代表传入的md5未被处理过
        open(config.md5_text,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_text,'r',encoding='utf-8').readline():
            line == md5_str
            return True
    return False

def save_md5(md5_str: str):
    '''
    将字符串存入md5.txt中
    :param md5_string:
    :return:
    '''
    with open(config.md5_text,'a',encoding='utf-8') as f:
        # ‘a’为追加模式，在文本后面写入新文本
        f.write(md5_str + '\n')


def get_string_md5(input_string: str,encoding='utf-8'):
    '''
    将字符串转为md5字符串
    :return:
    '''
    # 将传入字符串转为bytes字节数组
    string_byte = input_string.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5() #得到md5对象
    md5_obj.update(string_byte) #更新内容（传入即将转换的字节数组）
    md5_hex = md5_obj.hexdigest() #得到md5的十六进制字符串

    return md5_hex

class KnowlegdeBaseService(object):
    def __init__(self):
        self.chroma
        self.spliter

    def upload_by_str(self,data,filename):
        pass

if __name__=='__main__':
    pass
