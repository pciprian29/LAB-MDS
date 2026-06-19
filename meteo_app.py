import argparse
import os
import sys

import requests


API_KEY_ENV = "OPENWEATHER_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str, api_key: str, units: str = "metric") -> dict:
    params = {"q": city, "appid": api_key, "units": units, "lang": "ro"}
    resp = requests.get(BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def display_weather(data: dict) -> None:
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    print(f"\nVremea in {city}, {country}:")
    print(f"{'=' * 30}")
    print(f"  Temperatura:     {temp:.1f}°C")
    print(f"  Perceputa ca:   {feels_like:.1f}°C")
    print(f"  Umiditate:      {humidity}%")
    print(f"  Descriere:      {description.capitalize()}")
    print(f"  Vant:           {wind_speed} m/s\n")


def main():
    parser = argparse.ArgumentParser(description="Aplicatie Meteo - CLI")
    parser.add_argument("city", nargs="?", help="Orasul pentru care doriti vremea")
    parser.add_argument(
        "-k", "--api-key", help=f"Cheia API OpenWeather (sau variabila de mediu {API_KEY_ENV})"
    )
    parser.add_argument(
        "-u", "--units", choices=["metric", "imperial"], default="metric",
        help="Unitati de masura (metric: °C, imperial: °F)"
    )
    args = parser.parse_args()

    api_key = args.api_key or os.getenv(API_KEY_ENV)
    if not api_key:
        print(f"Eroare: Cheia API OpenWeather nu a fost furnizata.")
        print(f"Setati variabila de mediu {API_KEY_ENV} sau folositi flag-ul --api-key.")
        sys.exit(1)

    city = args.city
    if not city:
        city = input("Introduceti numele orasului: ").strip()
        if not city:
            print("Numele orasului nu poate fi gol.")
            sys.exit(1)

    try:
        data = get_weather(city, api_key, args.units)
        display_weather(data)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Orasul '{city}' nu a fost gasit.")
        elif e.response.status_code == 401:
            print("Cheia API este invalida.")
        else:
            print(f"Eroare HTTP: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Eroare de conexiune: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
