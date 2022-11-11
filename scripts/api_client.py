import requests


def get_returns_for_fq(fq: int):
    response = requests.get(f"http://localhost:8000/api/returns/returns-for-quarter/{fq}")
    if response:
        return response.json()


data = get_returns_for_fq(1)

for x in data:
    key = x['datamapline']['key']
    project = x['parent']['project']['name']
    if x['value_str']:
        value = x['value_str']
        label = "STR"
    elif x['value_int']:
        value = x['value_int']
        label = "INT"
    elif x['value_float']:
        value = x['value_float']
        label = "FLOAT"
    elif x['value_date']:
        value = x['value_date']
        label = "DATE"
    elif x['value_datetime']:
        value = x['value_datetime']
        label = "DATETIME"
    elif x['value_phone']:
        value = x['value_phone']
        label = "PHONE"
    d = dict(project=project, key=key, value=value)
    print(d)



# pprint.pprint(data[0])
