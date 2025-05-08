import time
from fastapi import APIRouter, Query, HTTPException
from service.weather import WeatherClient

router = APIRouter(prefix="/weather", tags=["weather"])

client = WeatherClient()

@router.get("/")
def get_weather(location: str = Query(..., example="Kyiv"), date: str = Query(None, example="2025-05-01")):
    start_time = time.time()  # Початок

    try:
        data = client.get_weather(location, date)
        duration = round(time.time() - start_time, 4)  # Час виконання в секундах

        return {
            "location": location,
            "date": date or data["days"][0]["datetime"],
            "temperature": data["days"][0]["temp"],
            "conditions": data["days"][0]["conditions"],
            "duration": f"{duration} сек"
        }
    except Exception as e:
        # Перевіряємо, чи проблема саме з локацією
        error_message = str(e)
        if "Invalid location parameter value" in error_message:
            raise HTTPException(
                status_code=422,
                detail="Невідома локація. Спробуй уточнити назву або використати координати."
            )
        raise HTTPException(status_code=500, detail="Помилка сервера або API: " + error_message)
