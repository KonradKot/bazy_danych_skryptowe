import dash
from dash import dcc, html
# biblioteki dash, dcc i html służa do tworzenia interfejsu użytkownika
import plotly.express as px # biblioteka ta służy do tworzenia interaktywnych wykresów
from pymongo import MongoClient # ważna bilioteka do nawiązywania połączenia z bazą danych MongoDB
import pandas as pd # umożliwia sprawną pracę z danymi

# Połączenie z bazą danych MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["earthquake_db"]
collection = db["earthquakes"]

#definuję układ aplikacji dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
# __name__ definuję nazwę bieżącego modułu
# suppress_callback_exceptions: Ten parametr ustawiam na True aby wyciszyć pewne wytjątki, które moga pojawic się w wywołaniach zwrotnych aplikacji Dash


def get_earthquake_data(limit=10): # funkcja zwraca max 10 danych
    earthquakes = list(collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(limit))
    # powyższa linia pobiera wszystkie dokumenty z kolekcji ok. 2tys, pomijając pole id(identyfikator dokumentu)
    #.sort("timestamp", -1) -> sortowanie wyników pola timestamp w kolenosci malejącej
    #.limit(limit) -> ograniczenie liczby wartości do liczby 10
    return earthquakes

def generate_table(dataframe, max_rows=10): # tworzy tabelę z 10 lokalizacjami na ziemi zawiarające dane o trzesieniach ziemi
    return html.Table( # tablica zawiera dane otrzęsieniach ziemi
        [html.Tr([html.Th(col) for col in dataframe.columns])] + #Ta linia tworzy wiersz ( <tr> ) w nagłówku tabeli ( <thead> ) zawierający nagłówki tabeli ( <th> ) dla każdej kolumny w obiekcie DataFrame. 
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns # Ta część generuje komórkę danych tabeli ( <td> ) dla każdej kolumny w obiekcie DataFrame dla określonego wiersza  i
        ]) for i in range(min(len(dataframe), max_rows))]
    )
    # wygląd całej aplikacji
    app.layout = html.Div(children=[
    html.H1(children='10 Latest Earthquakes'), # doaje tytuł na górze strony

    dcc.Graph(
        id='earthquake-magnitude', # dodaje wykres punktowy ze skalą trzesien
    ),

    dcc.Graph(
        id='earthquake-map', # dodaje mape ziemi z trzesieniami
    ),

    html.Button('Refresh', id='refresh-button'),  # Dodaj przycisk odświeżania

    html.H3(children='Earthquake Data Table:'),# dodaje tablę
    html.Div(id='table-div')
    ])

@app.callback(
    [dash.dependencies.Output('earthquake-magnitude', 'figure'),
     dash.dependencies.Output('earthquake-map', 'figure'),
     dash.dependencies.Output('table-div', 'children')],
    [dash.dependencies.Input('refresh-button', 'n_clicks')]
)
def update_output(n_clicks):
    data = get_earthquake_data()

    df = pd.DataFrame(data)
    fig = px.scatter(x=df["timestamp"], y=df["magnitude"], labels={"x": "Time", "y": "Magnitude"},
                     title="Earthquake Magnitude Over Time")

    map_fig = px.scatter_geo(df, lat='latitude', lon='longitude', size='magnitude', color='magnitude',
                              title="Earthquake Map", # tworze projekcję ziemi z odpowiednimi kolorami gdzie występują trzęsienia
                              projection="natural earth", template="plotly", size_max=30)

    table = generate_table(df) # tworzy tablę trzesień ziemi ponizej

    return fig, map_fig, table

if __name__ == '__main__':
    app.run_server(debug=True)
