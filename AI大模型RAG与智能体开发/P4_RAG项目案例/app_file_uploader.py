import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title('知识库更新服务')

uploder_file = st.file_uploader(
    '请上传txt文件',
    type=['txt'],
    accept_multiple_files=False
)

if 'service' not in st.session_state:
    st.session_state['service'] = KnowledgeBaseService()

if uploder_file is not None:
    file_name = uploder_file.name
    file_type = uploder_file.type
    file_size = uploder_file.size / 1024

    st.subheader(f'文件名：{file_name}')
    st.write(f'格式：{file_type} | 大小：{file_size:.2f} KB')

    text = uploder_file.getvalue().decode("utf-8")
    st.write(text)

    with st.spinner('正在载入向量库...'):
        time.sleep(1)
        result = st.session_state['service'].upload_by_str(text,file_name)
        st.write(result)