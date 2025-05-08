from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    db_url: str = "postgresql://postgres:1234@localhost/whether_db"
    weather_api_key: str = "ERQTCK2RU333QPLSFKTSL83C8"
    redis_url: str = "redis://localhost:6379/0"
    cache_expire_time: int = 3600
    
    
settings = Setting()



