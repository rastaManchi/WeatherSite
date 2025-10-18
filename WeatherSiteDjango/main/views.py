from django.shortcuts import render, HttpResponse
from  django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup as bs
import json, requests

# Create your views here.
def home(request):
    return render(request, 'home.html')

@csrf_exempt
def get_month_temp(request):
    data = json.loads(request.body)
    city = data['city']
    result = free_temp_history(city)
    return HttpResponse(json.dumps(result))


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


def free_temp_history(city):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 YaBrowser/25.8.0.0 Safari/537.36"
    }
    r = requests.get(f"https://www.gismeteo.ru/weather-{city}-4364/month/", headers=headers)
    data = bs(r.content, "lxml")
    temps = data.findAll(class_="row-item-month-date")
    result = []
    for temp in temps:
        day = temp.find(class_="date").text
        day_temps = temp.findAll("temperature-value")
        max = day_temps[0]["value"]
        min = day_temps[1]["value"]
        result.append({
            "day": day,
            "max": int(max),
            "min": int(min)
        })
    return result