import requests
import os
from django.shortcuts import render
from django.conf import settings
from openai import OpenAI

def home(request):
    city = request.GET.get('city', 'Moscow')

    weather_data = get_weather(city)
    recommendation = get_outfit_recommendation(weather_data)

    return render(request, 'home.html', {
        'city': city,
        'weather': weather_data,
        'recommendation': recommendation
    })


def get_weather(city):
    api_key = settings.OPENWEATHER_API_KEY
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en'
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or 'main' not in data:
        return {'error': 'City not found'}

    return {
        'temp': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }


def get_outfit_recommendation(weather):
    if 'error' in weather:
        return 'Cannot provide recommendation.'

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = (
        f"The weather is {weather['description']} and {weather['temp']}°C. "
        "Give a short outfit recommendation (2–3 sentences)."
        "Answer in russian." \
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
