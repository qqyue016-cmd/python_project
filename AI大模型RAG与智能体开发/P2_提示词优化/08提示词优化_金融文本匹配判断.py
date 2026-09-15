from openai import OpenAI

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 匹配示例（"是"=语义匹配，"不是"=语义不匹配）
examples_data = {
    "是": [
        ("公司ABC发布了季度财报，显示盈利增长。", "财报披露，公司ABC利润上升。"),
        ("公司ITCAST发布了年度财报，显示盈利大幅度增长。", "财报披露，公司ITCAST更赚钱了。"),
    ],
    "不是": [
        ("黄金价格下跌，投资者抛售。", "外汇市场交易额创下新高。"),
        ("央行降息，刺激经济增长。", "新能源技术的创新。"),
    ],
}

# 待判断的句子对
questions = [
    ("利率上升，影响房地产市场。", "高利率对房地产有一定的冲击。"),
    ("油价大幅度下跌，能源公司面临挑战。", "未来智能城市的建设趋势愈加明显。"),
    ("股票市场今日大涨，投资者乐观。", "持续上涨的市场让投资者感到满意。"),
]

# 构造 few-shot 提示
messages = [
    {"role": "system", "content": "你帮我完成文本匹配，我给你2个句子，被[]包围，你判断它们是否匹配，回答是或不是，请参考下方示例："},
]

for label, pairs in examples_data.items():
    for s1, s2 in pairs:
        messages.append({"role": "user", "content": f"句子1：[{s1}]句子2：[{s2}]"})
        messages.append({"role": "assistant", "content": label})

# 逐题调用大模型判断
for i, (q1, q2) in enumerate(questions, 1):
    prompt = f"按照上述示例，回答这2个句子的情况。句子1：[{q1}]句子2：[{q2}]"
    response = client.chat.completions.create(
        model="qwen3-max",
        messages=messages + [{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content
    print(f"\n===== 第 {i} 题 =====")
    print(f"句子1：{q1}")
    print(f"句子2：{q2}")
    print(f"判断：{answer}")