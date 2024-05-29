import requests
from datetime import datetime, timedelta
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import FastAPI

# Połączenie z bazą danych MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["earthquake_db"]
collection = db["earthquakes"]

class Earthquake(BaseModel):
    id: str
    latitude: float
    longitude: float
    title: str
    timestamp: datetime
    magnitude: float

def fetch_recent_earthquakes():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
    starttime = datetime.utcnow() - timedelta(days=7)
    endtime = datetime.utcnow().isoformat()  # Pobierz aktualny czas w formacie ISO8601
    params = {
    "format": "geojson",
    "starttime": starttime.isoformat(),  # Pobierz aktualny czas jako starttime
    "endtime": datetime.utcnow().isoformat()  # Pobierz aktualny czas jako endtime
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("1",data)

    earthquakes = []
    for feature in data["features"]:
        prop = feature["properties"]
        geom = feature["geometry"]["coordinates"]
        earthquake = Earthquake(
            id=feature["id"],
            latitude=geom[1],
            longitude=geom[0],
            title=prop["title"],
            timestamp=datetime.fromtimestamp(prop["time"] / 1000.0),
            magnitude=prop["mag"]
        )
        earthquakes.append(earthquake)

    return earthquakes


if __name__ == "__main__":
    earthquakes = fetch_recent_earthquakes()
    print(earthquakes)
    for eq in earthquakes:
        collection.insert_one(eq.dict())
