from rag import RagService
import streamlit as st
import config_data as config

st.title('智能客服')
st.divider() #分隔符

if 'message' not in st.session_state:
    st.session_state['message'] = [{'role': 'assistant', 'content': '你好呀，有什么我可以帮忙的吗？'}]

if 'rag' not in st.session_state:
    st.session_state['rag'] = RagService()

for message in st.session_state['message']:
    st.chat_message(message['role']).write(message['content'])

# 用户输入栏
prompt = st.chat_input()

if prompt:
    st.chat_message('user').write(prompt)
    st.session_state['message'].append({'role': 'user', 'content': prompt})

    with st.spinner('Ai思考中'):
        response = st.session_state['rag'].chain.invoke({'input': prompt},config.session_config)
        st.chat_message('assistant').write(response)
        st.session_state['message'].append({'role': 'assistant', 'content': response})
