import requests, json
# from config import *
from bs4 import BeautifulSoup as bs


def get_access_token():
    payload = {"scope": "GIGACHAT_API_PERS"}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": "RqUID",
        "Authorization": "GIGACHAT_AUTH_TOKEN"
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
            "content": "Ты - метеоролог, твоя задача - на основе данных посоветовать что надеть людям в зависимости от погоды!"
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


def find_locate():
    city = input("Введите город")

    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={weather_API}")
    data = json.loads(r.content)
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    print(lat, lon)

    r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=5&appid={weather_API}")
    data = json.loads(r.content)
    print(data)

    # access_token = get_access_token()
    # answer = get_answer(access_token, f"Погода: {data}")
    # print(answer)


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
        desc = temp.get("data-tooltip")
        print(f"День: {day}, Макс: {max}, Мин: {min} {desc}")
        print()

free_temp_history()