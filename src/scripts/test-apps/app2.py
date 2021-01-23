import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os
import plotly.express as px
import pandas as pd
import sg

data_path = '../../data'

df = pd.read_csv(f"{data_path}/processed/cbg_visits.csv").head(10)

df2 = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})


external_stylesheets = [os.path.join('style.css'), 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

container = html.Div([

    dbc.Row([
        dbc.Col(html.Div([
            dbc.Jumbotron([
                html.H1("Using Customer Demographics in Brand Analysis", className="display-4"),
                html.H3("Analyzing foot traffic data from SafeGraph", className='lead'),
                html.Hr(className='my-2'),
                html.P("What factors draw customers to visit their favorite stores, even in a pandemic? In an new era of reduced travel and extra safety precautions, which brands have prevailed so far? These are some of the questions our team sought to answer through our capstone project as considered the economic impacts of the COVID-19 pandemic. By analyzing consumer shopping behavior, we hope to find trends about how people spend money in their communities."),
                html.P(dbc.Button("Read the Report", color="primary"))
            ])
        ]))
    ]),

    dbc.Row([
        dbc.Col(html.Div([
            html.H1("Visualizing visits over time", className="text-center"),
            html.P(dash_table.DataTable(
                id='table',
                columns= [{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records')
            ), style={"width": "85%", "margin": "auto"}, className='text-center')
        ]))
    ]),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(f"Brand Name: {i}"),
            dbc.CardBody([
                html.H5("Card title", className='card-title'),
                html.P("This is some card content", className="card-text"),
                html.P(dcc.Graph(figure=px.bar(df2, x="Fruit", y="Amount", color="City", barmode="group")))
            ])
        ], className='mb-4'), width=6) for i in [f"Brand: {x}" for x in range(1,7)]
    ], className="my-2")

])






app.layout = dbc.Container(container, fluid=True)
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)