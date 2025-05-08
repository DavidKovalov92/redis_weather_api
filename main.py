from fastapi import FastAPI
from api_v1.weather.views import router as weather_router

app = FastAPI()
app.include_router(weather_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}