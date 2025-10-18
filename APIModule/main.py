import requests, json
from config import *
from bs4 import BeautifulSoup as bs



def get_access_token():
    payload = {"scope": "GIGACHAT_API_PERS"}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": RqUID,
        "Authorization": GIGACHAT_AUTH_TOKEN
    }
    r = requests.post('https://ngw.devices.sberbank.ru:9443/api/v2/oauth', data=payload, verify=False, headers=headers)

    access_token = json.loads(r.content)["access_token"]
    return access_token


def get_answer(access_token, text):
    payload = {
    "model": "GigaChat",
    "messages": [
            {
            "role":  "system",
            "content": "Ты - метеоролог, твоя задача - на основе данных посоветовать что надеть людям в зависимости от погоды! Отвечать строго ТОЛЬКО В JSON ФОРМАТЕ: {'верхняя одежда': 'что надеть', 'стоит ли выходить гулять': True/False}"
            },
            {
            "role": "user",
            "content": text
            }
    ],
    "stream": False,
    "repetition_penalty": 1
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    r = requests.post("https://gigachat.devices.sberbank.ru/api/v1/chat/completions", headers=headers, data=json.dumps(payload), verify=False)
    answer = json.loads(r.content)['choices'][0]['message']['content']
    return answer

access_token = get_access_token()
print(get_answer(access_token, "Температура: -5, Ветер: 1м\с"))
# answer = json.loads()
# print(answer)
# if answer['стоит ли выходить гулять']:
#     print(answer['верхняя одежда'])

def free_temp_history():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 YaBrowser/25.8.0.0 Safari/537.36"
    }
    r = requests.get("https://www.gismeteo.ru/weather-kazan-4364/month/", headers=headers)
    data = bs(r.content, "lxml")
    temps = data.findAll(class_="row-item-month-date")
    for temp in temps:
        day = temp.find(class_="date").text
        day_temps = temp.findAll("temperature-value")
        max = day_temps[0]["value"]
        min = day_temps[1]["value"]
        print(max)
        print(min)
        print(f"День: {day}, Макс: {max}, Мин: {min}")