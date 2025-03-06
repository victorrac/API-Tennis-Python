import requests
from datetime import datetime
import tkinter as tk

def fetch_weather_for_city(city, output_text):
    # Geocoding API to get latitude and longitude for the city
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid=5953693a5081c637199421e7af4f09ae"
    geo_response = requests.get(geocoding_url)

    if geo_response.status_code == 200:
        geo_data = geo_response.json()
        if geo_data:
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]

            # Weather API to get weather data
            weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid=5953693a5081c637199421e7af4f09ae"
            weather_response = requests.get(weather_url)

            if weather_response.status_code == 200:
                weather_data = weather_response.json()

                # Extract and display current weather
                current = weather_data.get("current", {})
                temp = kelvin_to_celsius(current.get("temp", "N/A"))
                feels_like = kelvin_to_celsius(current.get("feels_like", "N/A"))
                description = current.get("weather", [{}])[0].get("description", "N/A")
                sunrise = datetime.fromtimestamp(current.get("sunrise", 0)).strftime("%H:%M:%S")
                sunset = datetime.fromtimestamp(current.get("sunset", 0)).strftime("%H:%M:%S")

                # Clear previous weather output
                output_text.delete(1.0, tk.END)

                # Display current weather
                output_text.insert(tk.END, f"Current Weather in {city.title()}:\n")
                output_text.insert(tk.END, f"Temperature: {temp}°C (Feels like: {feels_like}°C)\n")
                output_text.insert(tk.END, f"Condition: {description.capitalize()}\n")
                output_text.insert(tk.END, f"Sunrise: {sunrise}, Sunset: {sunset}\n")

                # Extract and display daily weather summary
                daily = weather_data.get("daily", [])
                if daily:
                    output_text.insert(tk.END, "\n7-Day Weather Forecast:\n")
                    for day in daily[:7]:
                        date = datetime.fromtimestamp(day.get("dt", 0)).strftime("%A, %d %B %Y")
                        day_temp = kelvin_to_celsius(day.get("temp", {}).get("day", "N/A"))
                        night_temp = kelvin_to_celsius(day.get("temp", {}).get("night", "N/A"))
                        condition = day.get("weather", [{}])[0].get("description", "N/A")
                        rain = day.get("rain", 0)
                        output_text.insert(tk.END, f"{date}: Day {day_temp}°C, Night {night_temp}°C, Condition: {condition.capitalize()}, Rain: {rain}mm\n")

                # Extract and display alerts if any
                alerts = weather_data.get("alerts", [])
                if alerts:
                    output_text.insert(tk.END, "\nWeather Alerts:\n")
                    for alert in alerts:
                        sender = alert.get("sender_name", "Unknown")
                        event = alert.get("event", "N/A")
                        start = datetime.fromtimestamp(alert.get("start", 0)).strftime("%Y-%m-%d %H:%M:%S")
                        end = datetime.fromtimestamp(alert.get("end", 0)).strftime("%Y-%m-%d %H:%M:%S")
                        output_text.insert(tk.END, f"Alert from {sender}: {event} (Start: {start}, End: {end})\n")
                else:
                    output_text.insert(tk.END, "\nNo weather alerts for this location.\n")
            else:
                output_text.insert(tk.END, f"Error fetching weather data: {weather_response.status_code} - {weather_response.text}\n")
        else:
            output_text.insert(tk.END, f"City {city.title()} not found in OpenWeather geocoding data.\n")
    else:
        output_text.insert(tk.END, f"Error fetching geocoding data: {geo_response.status_code} - {geo_response.text}\n")

def kelvin_to_celsius(kelvin):
    try:
        return round(kelvin - 273.15, 2)
    except TypeError:
        return "N/A"