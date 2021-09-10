import requests

api_key = "e02e9c785a4576b3193a7f007e83625e" #please create an account on the openweather website and replace your api key with this one


def search(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    try:
        response = requests.get(url)
    except:
        return 404

    if response.status_code == 200:
        res = response.json()
        weather_info = res.get("weather")
        weather_condition = weather_info[0].get("main")
        weather_description = weather_info[0].get("description")

        city = res.get("name")

        temp = res.get("main")
        temp_kelvin = temp.get("temp")
        temp_celcius = round(int(temp_kelvin) - 273.15)

        humidity = temp.get('humidity')

        return weather_condition, weather_description, city, temp_celcius, humidity

    else:
        return "City not found", 404
