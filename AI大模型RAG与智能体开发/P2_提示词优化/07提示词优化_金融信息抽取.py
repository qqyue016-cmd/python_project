from openai import OpenAI
import json

client= OpenAI(
base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

example_data = [
    {
        'content':'2023-01-10,股市震荡，股票强大科技A股既然开盘价100人民币，一度飙升至105人民币，随后回落至98人民币，最终以102人民币收盘，成交量达到520000。',
        'answers':{
            '日期':'2023-01-10',
            '股票名称':'强大科技A股',
            '开盘价':'100人民币',
            '收盘价':'102人民币',
            '成交量':'520000'
        }
    },
    {
        'content': '2024-05-16,股市利好，股票英伟达美股今日开盘价105美元，一度飙升至109美元，随后回落到100美元，最终以116美元收盘，成交量达到3560000。',
        'answers': {
            '日期': '2024-05-16',
            '股票名称': '英伟达美股',
            '开盘价': '105美元',
            '收盘价': '116美元',
            '成交量': '3560000'
        }
    }
]



question = [
    '2025-06-16,股市利好，股票传智慧教育A股今日开盘价66人民币，一度飙升至70人民币，随后回落到65人民币，最终以68人民币收盘，成交量达到12300。',
    '2025-06-06,股市利好，股票黑马程序员A股今日开盘价200人民币，一度飙升至211人民币，随后回落到201人民币，最终以206人民币收盘，成交量达到12300。'
]

messages = [
    {'role':'system','content':f'你帮我完成信息抽取，我给你句子，你抽取[schema]信息，按JSON字符输出，如果最终信息不存在，用‘原文未提及’表示，请参考如下示例：'},
]

for exmaples in example_data:
    messages.append({'role':'user','content':exmaples['content']})
    messages.append({'role':'assistant','content':json.dumps(exmaples['answers'],ensure_ascii=False)})

for s in question:
    response = client.chat.completions.create(
        model='qwen3-max',
        messages = messages + [{'role':'user','content':f'按照上述示例抽取这个句子的信息：{s}'}]
    )

    print(response.choices[0].message.content)