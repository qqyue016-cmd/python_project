'''
知识库
'''

import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str: str):
    '''
    检查传入字符串在md5.txt里是否存在
    :return:
    '''
    # 返回False代表未处理，返回Ture代表已处理
    if not os.path.exists(config.md5_text):
        # 进入if代表传入的md5未被处理过
        open(config.md5_text,'w',encoding='utf-8').close()
        return False
    else:
        with open(config.md5_text, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if line.strip() == md5_str:
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

class KnowledgeBaseService(object):
    def __init__(self):
        # 创建数据库
        os.makedirs('./chroma.db',exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name, #向量数据库表名
            embedding_function=DashScopeEmbeddings(model='text-embedding-v4'), #调用向量嵌入式模型
            persist_directory=config.persist_directory #数据库本地存储文件夹
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, #分割后文本段最大长度
            chunk_overlap=config.chunk_overlap, #连续文本段之间的字符重叠数量
            separators=config.separators, #自然段落划分的符号
            length_function=len     #python自带len函数作为测量长度的依据
        )

    def upload_by_str(self,data: str,filename):
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return '[跳过]此文件已存在'
        if len(data) > config.max_split_char_number:
            knowledge_chunks = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata={
            'source':filename,
            'creat_time':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operator':'小林'
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)

        return '[成功]文件已上传'

if __name__=='__main__':
    a = KnowlegdeBaseService()
    print(a.upload_by_str('this is a test','test'))
