from pymongo import MongoClient
from pymongo.server_api import ServerApi

def create_connection(db_url):
    client = MongoClient(db_url)
    return client, client['builder_Konrad']

db_url = "mongodb://localhost:27017" # podnanie linku do lokalnej bazy danych
client, db = create_connection(db_url) # stworzenie zmiennych client i db

try:
    client.admin.command('ping') # sprawdzam czy uzyskałem połaczenie do bazy danych za pomocą ping
    print("Pinged your deployment. You successfully connected to MongoDB!") # pomyślne połączenie
except Exception as e:
    print(e) # nieudane połączenie

def create_collection(db, collection_name):
    return db[collection_name]

cities = create_collection(db, 'cities') # stworzenie kolekcji miasta w bazie danych 
buildings = create_collection(db, 'buildings') # stworzenie kolekcji budynków w bazie danych 

def create_city(collection, city):
    result = collection.insert_one(city) # dodanie nowego miasta do kolekcji, nie ma potrzeby dodawania nowego
    return result.inserted_id # zwraca ID nowego miasta

city_id = create_city(cities, {'name': "Poznan",'latitude': 52.2,'longitude': 17.0})
print(f'ID nowego miasta {city_id}') # kazde miasto ma sowje id


cursor = cities.find()
for doc in cursor:
    print(doc) # wypisuję miasta na ekranie

poznan = cities.find_one({'name': 'Poznan'}) # szuka jednego miasta
poznan_id = poznan['_id'] # tworzę zmieną ,która przechowuje id mista z kolekcji 
print('Poznan ma ID:', poznan_id)

def create_building(collection, building):
    result = collection.insert_one(building)
    return result.inserted_id

building_1 = create_building(buildings, {'city_id': poznan_id, "name":"Galeria", 'height': 17.0, 'build_year': 2010})
building_2 = create_building(buildings, {'city_id': poznan_id, "name":"Teatr", 'height': 25.5, 'build_year': 1950})

print('Wstawiono Galerię o ID:', building_1)
print('Wstawiono Teatr o ID:', building_2)

cursor = buildings.find()
for doc in cursor:
    print(doc)

result = buildings.aggregate([ # ropoczęcie agregacji
    {
        "$lookup": { # element agregacji służący do łączenia danych z innej kolekcji
            "from": "cities",
            "localField": "city_id",
            "foreignField": "_id",
            "as": "city"
        }
    }
])
for doc in result:
    print(doc)

def update_building_height(buildings, building_id, height):
    buildings.update_one({"_id": building_id}, {"$set": {"height": height}})

galeria = buildings.find_one({"name": "Galeria"})
update_building_height(buildings, galeria['_id'], 25.4)



def delete_building(buildings, building_id):
    buildings.delete_one({"_id": building_id})

teatr = buildings.find_one({"name": "Teatr"})
delete_building(buildings, teatr['_id'])

#client.close()

import json
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

@app.get('/cities')
def cities_get():
    all_cities = cities.find()
    output = [city for city in all_cities]
    for city in output:
        city['_id'] = str(city['_id']) #
    return output

# zamień
all_cities = cities.find()
# na 
all_cities = cities.find({}, {'_id': False})

# do kodu
all_cities = cities.find()
output = [city for city in all_cities]
# dodaj
for city in output:
    city['_id'] = str(city['_id'])

@app.get('/buildings')
def buildings_get():
    all_buildings = buildings.find()
    output = []
    for building in all_buildings:
        building['_id'] = str(building['_id'])  # Convert ObjectId to string
        output.append(building)
    return output


class Building(BaseModel):
    city_id: str
    name: str
    height: float
    build_year: int

@app.post('/buildings/add')
def add_building(building: Building):
    building_id = create_building(
        buildings,
        building.model_dump()
    )
    return str(building_id)

@app.get('/buildings/update/{building_id}/{height}')
def building_update_height(building_id, height):
    update_building_height(buildings, building_id, height)
    return True

@app.get('/buildings/delete/{building_id}')
def building_delete(building_id):
    delete_building(buildings, building_id)
    return True

if __name__=='__main__':
    uvicorn.run(app)

#client.close()