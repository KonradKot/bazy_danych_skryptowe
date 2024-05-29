import uvicorn
import json
from fastapi import FastAPI, Response
from pydantic import BaseModel



rooms={
    'P-01':'Pokoj goscinny',
    'P-02':'Szatnia',
    'P-03':'Laboratorium Fal i Anten',
    'P-04':'Pokoj kola naukowego Spektrum',
    'P-05':'Laboratorium Mikroprocesorow',
    'P-06':'Laboratorium Elektroniki',
    'P-07':'Sala wykladowa',
    'P-08':'Sala komputerowa sieci Cisco',
    'P-09':'Pomieszczenie techniczne',
    'P-10':'WC'
}

reservation_data = {
    'P-01': {
        '2024-03-20': 'Tomasz Lis',
        '2024-03-21': 'Andrzej Kowalski',
    },
    'P-02':{
        '2024-03-20':'Kamil Lis',
        '2024-03-21':'Waldek Kowalski',
    },
    'P-03':{
        '2024-03-20':'Konrad Stefczyk',
        '2024-03-21':'Adrian Seniuk',
    },
    'P-04':{
        '2024-03-20':'Konrad Stefczyk',
        '2024-03-21':'Jan Michas',
    },
    'P-05':{ 
        '2024-03-20':'Alicja Nowak', 
        '2024-03-21':'Piotr Kowalczyk', 
    }, 
    'P-06':{ 
        '2024-03-20':'None', 
        '2024-03-21':'None', 
    }, 
    'P-07':{ 
        '2024-03-20':'Natalia Szymańska', 
        '2024-03-21':'None', 
    }, 
    'P-08':{ 
        '2024-03-20':'Karolina Dąbrowska', 
        '2024-03-21':'Łukasz Jankowski', 
    }, 
    'P-09':{ 
        '2024-03-20':'Wiktoria Nowak', 
        '2024-03-21':'Bartosz Wojciechowski', 
    }, 
    'P-10':{},
    }


app=FastAPI() # aplikacja działa na fastappi

@app.get('/') # funkcja powitalna
def hello_world():
    return {"Hello":"Witaj w systemie rezerwacji !"}

@app.get('/get') # zwraca komunikat o systemie, dane o całkowitej liczbie pokoi oraz całkowitej licznie rezerwacji w formacie json
def get_json():
    all_rooms = len(rooms)
    all_reserv = int(0)
    for key in reservation_data:
        for value in reservation_data[key].values():
            if value is not None and value != 'None':
                all_reserv += 1

    system_info = {
        "message":"informacja o systemie",
        "total_rooms":all_rooms,
        "total_reserv":all_reserv,
    }
    return json.dumps(system_info)

@app.get('/get/clear') # kasuje wszystkie dane o pokojach i rezerwacjach, zwraca
def get_clear():
    for key in rooms:
        rooms[key]=None
    for key in reservation_data:
        for sub_key in reservation_data[key]:
            reservation_data[key][sub_key]=None

    return {"Deleted!"}

@app.get('/get/rooms') #zwraca listę pomieszczeń zarejestrowanych w systemie, 
def get_rooms():
    system_info=[]

    for key in rooms:
        system_info.append(key)
    return json.dumps(system_info)

@app.get('/get/reservations/{room}') #zwraca listę rezerwacji dla pomieszczenia {room}, np. { "state":"OK", "data": "who": "Adam", "when": "2024-03-21" }". 
def get_reserv_room(room: str):
    if room in reservation_data:
        reserv_list = []
        for date, name in reservation_data[room].items():
            if name is not None and name != 'None':
                reservation_info={
                    "who":name,
                    "when":date,
                }
                reserv_list.append(reservation_info)
        return {"state":"OK","data":reserv_list}
    else:
        return {"state":"ERROR","message":f"Pokoj {room} istnieje w systemie!"}

@app.get('/get/print/rooms') #zwraca status i listę pokojów wraz z opisami w czytelnym formacie: { "state":"OK", "data"=[ "Pokój P223 II piętro, 15PC" ] }
def get_print_room():
    room_info = [{"state":"OK", "data":[f"{key}:{value}"]} for key, value in rooms.items()]
    return room_info

@app.get('/get/print/reservations/{room}') #zwraca status i listę rezerwacji danego pomieszczenia w czytelnym formacie:{ "state":"OK","data":["Adam zarezerwował termin 18-02-2024"] }
def get_print_reserv_room(room: str):
    if room in reservation_data:
        reserv_list = []
        for date, name in reservation_data[room].items():
            if name is not None and name !='None':
                reserv_list.append(f"{name} zarezrwowal termin {date}")
        return [{"state":"OK","data":reserv_list}]
    else:
        return [{"state":"ERROR","message":f"Pokoj {room} nie istnieje w systemie! "}]


class New_room(BaseModel):
    # klasa do obsługi 
    name: str
    description: str

@app.post('/post/rooms/add')
def post_rooms_add(new_room: New_room):
    if new_room.name not in rooms:
        rooms[new_room.name] = json.dumps(new_room.description)
        return {"state":"OK", "data": {"room":new_room.name, "message": f"Pokoj {new_room.name} został dodany do systemu"}}
    else:
        return {"state":"ERROR", "data":{"room":new_room.name, "message": f"Pokoj {new_room.name} jest już w systemie"}}

class New_reservation(BaseModel):
    who: str
    when: str

@app.post('/post/reservations/{room}/add')
def post_reservations_room_add(room: str, new_reservation: New_reservation):
    if room in reservation_data:
        if new_reservation.when not in reservation_data[room]:
            reservation_data[room][new_reservation.when] = new_reservation.who
            return {"state":"OK","message":f"Rezerwacaja dla {new_reservation.who} na {new_reservation.when} w {room} zostala pomyslnie dodana! "}
        else:
            return {"state":"OK","message":f"Termin {new_reservation.when } jest niedostepny (ta sama osoba) niedostepny dla pokoju {room}"}
    else:
        return {"state":"ERROR", "data":{"room":room, "message": f"Pokoj {room} nie ma w systemie! "}}

if __name__ == '__main__':
    uvicorn.run(app)