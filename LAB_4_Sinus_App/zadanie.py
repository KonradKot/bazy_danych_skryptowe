import numpy as np
from dash import Dash, html
from dash import dcc, Output, Input, callback
import plotly.express as px

app = Dash(__name__)

AMPLITUDA_MIN=-1
AMPLITUDA_MAX=1

app.layout = html.Div([
html.Div("Wykres sinusa"),
html.Label("Amplituda"),
dcc.Slider(
    id="amplituda-slider",
    min=0,
    max=1,
    step=0.1,
    value=0.5,
    marks={i /10: str(i / 10) for i in range(11)}
),
html.Label("Czestotliwosc (Hz): "),
dcc.Slider(
    id="czestotliwosc-slider",
    min=1,
    max=100,
    step=1,
    value=10,
    marks={i:str(i) for i in range (0,101,10)}
),
    dcc.Graph(id="sinus-graph")
])

@app.callback(
    Output("sinus-graph","figure"),
    [Input("amplituda-slider","value"),
    Input("czestotliwosc-slider","value")]
)
def update_graph(A, f):

    t = np.linspace(0,1,1000)
    y = A* np.sin(2*np.pi * t * f)

    fig = px.line(x=t, y=y, labels={'x':'Czas(s)','y':'Amplituda'}, title="Wykres sinusa")

    fig.update_yaxes(range=[AMPLITUDA_MIN,AMPLITUDA_MAX])

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)