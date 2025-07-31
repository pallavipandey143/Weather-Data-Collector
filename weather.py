from fastapi import FastAPI
from pymongo import MongoClient
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.responses import JSONResponse



API_KEY = "519a3f830e7ea95ba1631b7ec1edded2"
CITY_NAME = "Ranchi"
MONGO_URI = "mongodb://localhost:27017/"


client = MongoClient(MONGO_URI)
db = client["weather_db"]
collection = db["weather_data"]

app = FastAPI()

@app.get('/')
def fetch_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "city": CITY_NAME,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weather": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"]
        }
        collection.insert_one(weather_data)

        print("Weather data inserted.")

    else:
        print("Failed to fetch weather data", response.status_code)
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_weather, 'interval', minutes=1)
scheduler.start()

@app.get("/")
def get_latest_weather():
    data = collection.find_one(sort=[("timestamp", -1)])  # latest data
    if data:
        data_dict = dict(data)
        data_dict.pop("_id", None)
        return JSONResponse(content=data)
    else:
        return JSONResponse(content={"message": "No weather data found."}, status_code=404)







@app.get('/about')
def about():
    return {'page name':'about Page comming soon'}

@app.get('/contact')
def contact():
    return {'page name':'contact Page comming soon'}

