from openai import OpenAI


# 1.获取client对象，OpenAI类对象
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
# 2.调用模型
response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role":"system","content":"你是一个ai助理，并且不说废话简单回答"},  
        {"role":"user","content":"小明有两条狗"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"小明有三只猫"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"小明有多少只宠物"},
    ]
)
# 3.处理对象
print(response.choices[0].message.content)