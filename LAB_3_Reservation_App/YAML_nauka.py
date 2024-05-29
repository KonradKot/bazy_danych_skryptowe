import yaml

data = None

with open('LAB_3/historia.yaml','r') as file:
    data=yaml.safe_load(file) #wczytywanie pliku yaml

print(data)

#wyswietlam historie transakcji w czytelny sposób
print('Konto',data['wlasciciel']['imie'], data['wlasciciel']['nazwisko'],f'({data["numer"]})')

for i, j in enumerate(data['historia']):
    print(j['data'],j['kwota'],'za',j['tytul'])


# dodam dwa nowe wisy do wczytanej struktury danych
przelew_a = {
    "data":"2024-02-01",
    "kwota":12.0,
    "tytul":"telefon"
}
data['historia'].append(przelew_a)

przelew_b = {
    "data":"2024-02-02",
    "kwota":60.0,
    "tytul":"internet"
}
data['historia'].append(przelew_b)

#oblicze wynik konta i wynik dodam do struktury danych
saldo=[]

for i,v in enumerate(data['historia']):
    saldo.append(v['kwota'])

saldo = sum(saldo)

print('Konto:',data['wlasciciel']['imie'],data['wlasciciel']['nazwisko'],f'({data["numer"]})')

print("sado: ",saldo)

for i,j in enumerate(data['historia']):
    print(j['data'],j['kwota'],'za',j['tytul'])

with open('LAB_3/nowa_transakcja.yaml','w') as file:
    yaml.safe_dump(data,file)