import json

d = {
    'name':'小林',
    'age':'18',
    'gener':'男'
}

print(json.dumps(d,ensure_ascii=False))

s = [
    {
        'name':'小林',
        'age':'18',
        'gener':'男'
    },
    {
        'name':'小元',
        'age':'19',
        'gener':'男'
    },
    {
        'name':'林',
        'age':'20',
        'gener':'男'
    }
]

print(json.dumps(s,ensure_ascii=False))

c = '{"name": "小林", "age": "18", "gener": "男"}'
print(json.loads(c))

e = '[{"name": "小林", "age": "18", "gener": "男"}, {"name": "小元", "age": "19", "gener": "男"}, {"name": "林", "age": "20", "gener": "男"}]'
print(json.loads(e))