from pymongo import MongoClient
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import List
import uvicorn

# 0 stworzenie połączenia z bazą danych
def create_connection(db_url):
    client = MongoClient(db_url)
    return client, client["builder_123456"]

db_url = "mongodb://localhost:27017"
client, db = create_connection(db_url)

# 0_1 sprawdzanie połączenia z bazą danych
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# 0_2 Utworzenie nowej kolekcji
def create_collection(db, collection_name):
    return db[collection_name]

cars = create_collection(db, 'cars')

# 1 Przygotowanie funkcji kolekcji

# 1_1 dodanie dokumentu do kolekcji (dokument składa się z pól "id", "marka", "model", "rocznik", "polubienia")
def create_car(collection, car):
    result = collection.insert_one(car)
    return result.inserted_id

# Dodawanie kilku samochodów dla przykładu
cars.delete_many({})  # Usunięcie istniejących danych dla czystości
car_1 = create_car(cars, {
    'car_id': "audi_id","marka": "Audi","model": "A4","rocznik": "2010",
    "polubienia": 0
})
car_2 = create_car(cars, {'car_id': "bmw_id","marka": "BMW","model": "X5","rocznik": "2015",
    "polubienia": 0
})
car_3 = create_car(cars, {
    'car_id': "mercedes_id",
    "marka": "Mercedes",
    "model": "C-Class",
    "rocznik": "2018",
    "polubienia": 0
})

# 1_2 aktualizację dokumentu
def update_car_likes(cars, car_id, like):
    cars.update_one({"car_id": car_id}, {"$set": {"polubienia": like}})

# 1_3 pobranie jednego dokumentu (po id)
def get_car_by_id(collection, car_id):
    return collection.find_one({"car_id": car_id})

# 1_4 pobrania wszystkich dokumentów
def get_all_cars(collection):
    return collection.find()
# 1_5 usunięcia dokumentu
def delete_car_in_collect(collection, car_id):
    collection.delete_one({"car_id": car_id})

# 2 Przygotowanie końcowych punktów aplikacji
app = FastAPI()

class Car(BaseModel):
    car_id: str
    marka: str
    model: str
    rocznik: str
    polubienia: int

@app.get("/", response_class=HTMLResponse)
def display_cars(request: Request):
    car_list = """
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />
        <style>
            body { font-family: Arial, sans-serif; }
            .car { margin-bottom: 20px; }
            .car .info { display: inline-block; vertical-align: top; margin-left: 20px; }
            .car .actions { margin-top: 10px; }
        
            .car .actions a { margin-right: 10px; text-decoration: none; }
            .car .actions a.like { color: green; }
            .car .actions a.dislike { color: red; }
        </style>
    </head>
    <body>
        <h1>List of Cars</h1>
    """
    for car in cars.find():
        car_list += f"""
        <div class="car">
            <div class="info">
                <p>{car['marka']} {car['model']} ({car['rocznik']})</p>
                <p>Likes: {car['polubienia']}</p>
                <div class="actions">
                    <a href='/like/{car['car_id']}' class="like"><i class="fas fa-thumbs-up"></i> Like</a>
                    <a href='/dislike/{car['car_id']}' class="dislike"><i class="fas fa-thumbs-down"></i> Dislike</a>
                </div>
            </div>
        </div>
        """
    car_list += """
    </body>
    </html>
    """
    return HTMLResponse(content=car_list, status_code=200)

@app.get("/cars", response_model=List[Car])
def get_cars():
    return list(cars.find())

@app.get("/like/{car_id}", response_class=RedirectResponse)
def like_car(car_id: str):
    car = cars.find_one({"car_id": car_id})
    if car:
        cars.update_one({"car_id": car_id}, {"$inc": {"polubienia": 1}})
    return RedirectResponse(url='/') #powrót na stronę główną

@app.get("/dislike/{car_id}", response_class=RedirectResponse)
def dislike_car(car_id: str):
    car = cars.find_one({"car_id": car_id})
    if car:
        cars.update_one({"car_id": car_id}, {"$inc": {"polubienia": -1}})
    return RedirectResponse(url='/') 

@app.post("/cars/add", response_model=Car)
def add_car(car: Car):
    car_id = create_car(cars, car.dict())
    return get_car_by_id(cars, car.car_id)

if __name__ == '__main__':
    uvicorn.run(app)
