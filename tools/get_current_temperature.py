import requests
from google.genai import types
schema_get_current_temperature = types.FunctionDeclaration(
    name="get_current_temperature",
    description="Gets the current temperature for a given location.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "city": types.Schema(
                type=types.Type.STRING,
                description="The city name, e.g. San Francisco",
            ),
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base directory from which to execute the function. This is automatically provided and should not be specified by the user."
            ),
        },
        required=["working_directory", "city"],
    ),
)

def get_current_temperature(working_directory: str, city: str) -> float:
    """
    Returns current temperature in Celsius for a city, using only no-key services.
    Uses:
      - A geocoding service to convert city name to lat/lon
      - Open-Meteo to get current temp from lat/lon
    Raises exception if something fails.
    """
    # Step 1: Geocode city name to lat/lon
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    params_geo = {
        "name": city,
        "count": 1,          # we only need the top result
    }
    geo_resp = requests.get(geocode_url, params=params_geo)
    geo_data = geo_resp.json()
    if "results" not in geo_data or len(geo_data["results"]) == 0:
        raise ValueError(f"Could not geocode city: {city}")
    loc = geo_data["results"][0]
    lat = loc["latitude"]
    lon = loc["longitude"]

    # Step 2: Call Open-Meteo current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params_weather = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "temperature_unit": "celsius"  # optional; default might already be Celsius
    }
    weather_resp = requests.get(weather_url, params=params_weather)
    weather_data = weather_resp.json()
    if "current_weather" not in weather_data:
        raise RuntimeError("Could not fetch current weather data")

    temp = weather_data["current_weather"]["temperature"]
    return temp

# Example usage:
# if __name__ == "__main__":
#     city = "State College"
#     try:
#         t = get_current_temperature(city)
#         print(f"Current temperature in {city}: {t}°C")
#     except Exception as e:
#         print("Error:", e)
