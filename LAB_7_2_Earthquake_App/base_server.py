from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from datetime import datetime
from bson import ObjectId
import uvicorn

# Połączenie z bazą danych MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["earthquake_db"]
collection = db["earthquakes"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Model danych do przechowywania informacji o trzęsieniu ziemi
class Earthquake(BaseModel):
    id: str
    latitude: float
    longitude: float
    title: str
    timestamp: datetime
    magnitude: float

app = FastAPI()

@app.post("/add/single")
def add_single_earthquake(earthquake: Earthquake):
    try:
        collection.insert_one(earthquake.dict())
        return {"message": "Earthquake added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add/list")
def add_list_of_earthquakes(earthquakes: List[Earthquake]):
    try:
        result = collection.insert_many([eq.dict() for eq in earthquakes])
        return {"received": len(earthquakes), "added": len(result.inserted_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get")
def get_earthquakes(limit: int = 10):
    try:
        earthquakes = list(collection.find().sort("timestamp", -1).limit(limit))
        for eq in earthquakes:
            eq['_id'] = str(eq['_id'])
        return earthquakes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app)
