import requests
import redis
import json
from core.config import settings


class WeatherClient:
    def __init__(self, api_key=settings.weather_api_key, unit_group="metric"):
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        self.api_key = api_key
        self.unit_group = unit_group
        self.content_type = "json"
        self.redis = redis.StrictRedis.from_url(settings.redis_url, decode_responses=True)
        self.cache_expire_time = settings.cache_expire_time

    def get_weather(self, location: str, date: str | None = None):
        cache_key = f"{location}-{date or 'today'}"

        cached_data = self.redis.get(cache_key)
        if cached_data:
            print("Використано кешований результат з Redis")
            return json.loads(cached_data)

        url = f"{self.base_url}/{location}"
        if date:
            url += f"/{date}"

        params = {
            "unitGroup": self.unit_group,
            "key": self.api_key,
            "contentType": self.content_type
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.redis.setex(cache_key, self.cache_expire_time, json.dumps(data)) 
            return data
        else:
            raise Exception(f"Помилка запиту: {response.status_code} — {response.text}")



