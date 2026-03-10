from langchain.tools import tool
import requests
API_KEY = "10432ed37cb8491fb66140452260903"
city = "Pune"

@tool
def get_weather(city: str) -> str:
    """
    Get current weather of a city. Input should be a city name.
    """

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

    response = requests.get(url)
    data = response.json()

    temp = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]
    humidity = data["current"]["humidity"]

    return f"Weather in {city}: {temp}°C, {condition}, Humidity {humidity}%"

# weather_info = get_weather(city)
# print(weather_info)