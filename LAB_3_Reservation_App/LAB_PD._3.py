import yaml
import uvicorn
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

rooms={
    'P-21':'Laboratory room for all',
    'P-22':'Kitchen with microvawe',
    'P-23':'Antena Laboratory (Attention!)',
    'P-24':'Lecture room',
    'P-25':'Meetings Rroom',
    'P-26':'Profesor Room',
    'P-27':'Student Classroom',
}

reservations={
    'P-21':{
        'who':'Adam Glapinski',
        'when':'2024-03-20',
        },
    'P-22':{
        'who': 'Dominik Jachaś',
        'when': '2024-03-21',
    },
    'P-23':{
        'who': 'Bogusław Dyko',
        'when': '2024-03-22',
    },
    'P-24':{
        'who': 'Arek Kowalski',
        'when': '2024-03-23',
    },
    'P-25':{
        'who':None,
        'when': None,
    },
    'P-26':{
        'who': None,
        'when': None,
    },
    'P-27':{
        'who': 'Michalina Kowalska',
        'when': '2024-03-26',
    },
}

data_list={}

@app.get('/')
def hello_world():
    return("Witaj w systemie rezerwacji")

@app.get('/get') #print basic data
def get_json():
    total_rooms = len(reservations)
    total_reservations = 0
    status = 'FULL'

    for i in reservations.values():
        if i['when'] is not None and i['who'] is not None:
            total_reservations+=1
        if i['when'] == None: status='OK'
    
    status_dict={"state": status}
    data_dict={"rooms": int(total_rooms),"reservations":int(total_reservations), "message":"system information"}
    data_list=[status_dict,data_dict]
    return data_list

@app.get('/get/clear') #delete data
def get_clear():
    try:
        rooms.clear()
        reservations.clear()
        status_dict={"state":'OK'}
        data_dict={"rooms":int(0),"reservations": int(0), "message":"system delete"}
        data_list=[status_dict,data_dict]
        return data_list
    except:
        status_dict={"state":"ERROR"}
        return status_dict

@app.get('/get/rooms')
def get_rooms():
    list_rooms=list()
    if rooms is not None:
        status_dict={"state":"OK"}
        list_rooms.append(status_dict)
    else:
        status_dict={"state":"ERROR"}
        list_rooms.append(status_dict)
        return list_rooms
    tab_rooms=[]
    for v,i in enumerate(rooms):
        tab_rooms.append(i)
    list_rooms.append(tab_rooms)
    return list_rooms
@app.get('/get/reservations/{room}')
def get_reserv_room(room: str):
    if room in reservations:
        
        reserv = reservations[room]
        if reserv['when'] is not None and reserv['who'] is not None:
            return {"state": "OK", "data": {"who": reserv['who'], "when": reserv['when']}}
        else:
            return {"state": "ERROR", "message": "Brak rezerwacji dla tego pokoju."}
    else:
        return {"state": "ERROR", "message": "Podany pokoj nie istnieje w systemie."}
 
@app.get('/get/print/rooms')
def get_print_room(): ### ????
    list_room=list()
    tab_data=[]
    for j in reservations.values():
        if j['when'] is not None and j['who'] is not None:
            status_dict={"state":"OK"}
        else:
            status_dict={"state":"FREE"}
        list_room.append(status_dict)
        

@app.get('/get/print/reservations/{room}')
def get_print_reserv_room(room: str):
    if room in reservations and reservations[room]['who'] is not None and reservations[room]['when'] is not None:
        reservation_info = f"{reservations[room]['who']} zarezerwował termin {reservations[room]['when']}"
        return {"state": "OK", "data": [reservation_info]}
    else:
        return {"state": "ERROR", "message": "Brak rezerwacji dla tego pokoju."}

@app.get('/post/rooms/add')
def post_rooms_add(room_data: dict):
    room_name = room_data.get('name')
    room_description = room_data.get('description')

    if room_name in rooms:
        return {"state": "ERROR", "data": {"room": room_name, "message": f"Pokój {room_name} jest już w systemie"}}
    else:
        rooms[room_name] = room_description
        return {"state": "OK", "data": {"room": room_name, "message": f"Pokój {room_name} został dodany do systemu"}}

@app.get('/post/reserv/{room}/add')
def add_reservation(room: str, reservation_data: dict):
    if room not in rooms:
        raise HTTPException(status_code=404, detail="Podane pomieszczenie nie istnieje w systemie.")
    
    if room in reservations and reservations[room]['when'] is not None:
        raise HTTPException(status_code=400, detail="Podane pomieszczenie jest już zarezerwowane.")
    
    reservations[room] = {
        'who': reservation_data.get('who'),
        'when': reservation_data.get('when')
    }
    
    return {"state": "OK", "data": {"room": room, "message": f"Rezerwacja dla pokoju {room} została dodana."}}


if __name__ == '__main__':
    uvicorn.run(app) # uruchamiam aplikacje na koncu
