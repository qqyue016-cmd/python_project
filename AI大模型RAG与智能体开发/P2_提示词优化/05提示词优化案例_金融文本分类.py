from openai import OpenAI

client= OpenAI(
base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

example_data = {
    '新闻报道':'央行宣布降准0.5个百分点，释放长期资金约一万亿。',
    '财务报告':'工商银行上半年净利润1852亿元，同比增长1.1%。',
    '公司公告':'公司拟发行50亿元公司债券，用于补充营运资金。',
    '分析师报告':'维持银行板块"增持"评级，看好息差企稳与资产质量改善。',
}

example_types = ['新闻报道','财务报告','公司公告','分析师报告']

question = [
    '央视报道A股三大指数集体收涨，两市成交额突破1.2万亿元。',
    '报告期内不良贷款率降至1.2%，拨备覆盖率持续提升。',
    '关于拟收购券商10%股权的公告，尚待监管机构批准。',
    '预计美元指数下半年回落，人民币汇率或温和升值至7.1。',
    '小明喜欢小林'
]

message = [
    {"role":"system","content":"你是金融专家，将文本分类为['新闻报道'，'公司公告'，'财务报道'，'分析师报告']，不清楚回答不清楚类型"}

]

for key,value in example_data.items():
    message.append({"role":"user","content":value})
    message.append({"role":"assistant","content":key})

for q in question:
    response = client.chat.completions.create(
        model='qwen3-max',
        messages = message + [{"role": "user", "content": f'按照示例，回答这段文本的分类类别：{q}'}]
    )

    print(response.choices[0].message.content)