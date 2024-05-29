import json
import yaml
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

class Bill(BaseModel):
    data: str
    kwota: float
    tytul: str

app = FastAPI()

@app.get("/")
def hello_world():
    return {"Hello": "World"}

@app.get('/hello/{imie}')
def hello_name(imie: str):
    return {"Hello": imie}

@app.get('/hello/{imie}/{nazwisko}')
def hello_name(imie: str, nazwisko: str):
    return {"Hello": f"{imie} {nazwisko}"}

@app.get('/history/get/yaml')
def get_history_yaml():
    data = None
    with open('LAB_3/nowa_transkakcja.yaml', 'r') as file:
        data = yaml.safe_load(file)
    return data

@app.get('/history/get/json')
def get_history_json():
    data = None
    with open('LAB_3/nowa_transakcja.yaml', 'r') as file:
        data = yaml.safe_load(file)
    return json.dumps(data)

@app.post('/history/add')
def add_to_history(bill: Bill):
    with open('LAB_3/nowa_transakcja.yaml', 'r') as file:
        data = yaml.safe_load(file)
        data['historia'].append(bill.dict())
    with open('LAB_3/nowa_transakcja.yaml', 'w') as file:
        yaml.safe_dump(data, file)
    return {'status': 'ok'}

if __name__ == '__main__':
    uvicorn.run(app)