import requests


class WeatherForecastService:
    def __init__(self, api_key="5cb008bf3b6e4cf0af250142240701"):
        self.api_key = api_key
        self.base_url = "https://api.worldweatheronline.com/premium/v1/weather.ashx"

    def get_weather_details(self, location, num_of_days=1, format='json'):
        params = {
            'key': self.api_key,
            'q': location,
            'num_of_days': num_of_days,
            'format': format,
            'cc': 'yes',  # Include current weather conditions
            'fx': 'yes'   # Include weather forecast
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Check for any request errors

            data = response.json()

            # Extracting relevant information for the current condition
            current_condition = data.get('data', {}).get('current_condition', [])[0]
            temp_C = current_condition.get('temp_C')
            feels_like_C = current_condition.get('FeelsLikeC')
            weather_desc = current_condition.get('weatherDesc', [])[0].get('value')

            return {'temp_C': temp_C, 'feelsLikeC': feels_like_C, 'weatherDesc': weather_desc}

        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"

        except ValueError as ve:
            return f"Error parsing JSON response: {ve}"

    def get_all_weather_details(self, location):
        params = {
            'key': self.api_key,
            'q': location,
            'num_of_days': 1,
            'format': 'json',
            'cc': 'yes',  # Include current weather conditions
            'fx': 'yes'  # Include weather forecast
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Check for any request errors

            data = response.json()

            # Extracting all provided information into variables
            current_condition = data.get('data', {}).get('current_condition', [])[0]
            temp_C = current_condition.get('temp_C')
            feels_like_C = current_condition.get('FeelsLikeC')
            weather_desc = current_condition.get('weatherDesc', [])[0].get('value')
            windspeed_miles = current_condition.get('windspeedMiles')
            windspeed_kmph = current_condition.get('windspeedKmph')
            winddir_degree = current_condition.get('winddirDegree')
            winddir_16point = current_condition.get('winddir16Point')
            weather_code = current_condition.get('weatherCode')
            precip_mm = current_condition.get('precipMM')
            precip_inches = current_condition.get('precipInches')
            humidity = current_condition.get('humidity')
            visibility_km = current_condition.get('visibility')
            visibility_miles = current_condition.get('visibilityMiles')
            pressure_mb = current_condition.get('pressure')
            pressure_inches = current_condition.get('pressureInches')
            cloud_cover = current_condition.get('cloudcover')

            return {
                'temp_C': temp_C,
                'feelsLikeC': feels_like_C,
                'weatherDesc': weather_desc,
                'windspeedMiles': windspeed_miles,
                'windspeedKmph': windspeed_kmph,
                'winddirDegree': winddir_degree,
                'winddir16Point': winddir_16point,
                'weatherCode': weather_code,
                'precipMM': precip_mm,
                'precipInches': precip_inches,
                'humidity': humidity,
                'visibility': visibility_km,
                'visibilityMiles': visibility_miles,
                'pressure': pressure_mb,
                'pressureInches': pressure_inches,
                'cloudcover': cloud_cover
            }

        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"

        except ValueError as ve:
            return f"Error parsing JSON response: {ve}"