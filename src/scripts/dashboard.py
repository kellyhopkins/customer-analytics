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
        dbc.Col([
            html.H1("Demographic Profile: Gender", className="text-center"),
            dcc.Graph(
                id='gender-graph',
                figure= px.bar(sg.calc_gender(['wawa', 'starbucks', '7_eleven']), x='brand', y=['est_male', 'est_female'])
            )
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.H1("Demographic Profile: Race and Ethnicity", className="text-center"),
            dcc.Graph(
                id='race-graph',
                figure= px.bar(sg.calc_race(['wawa', 'starbucks', '7_eleven']), x='brand', y=[f"est_{i}" for i in ['white', 'black', 'asian', 'other']])
            )
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.H1("Demographic Profile: Age Group", className="text-center"),
            dcc.Graph(
                id='age-graph',
                figure= px.bar(sg.calc_age(['wawa', 'starbucks', '7_eleven']), x='brand', y=[f"est_{i}" for i in ['20_29', '30_39', '40_49', '50_59', '60_69', '70+']])
            )
        ])
    ]),



#end
])






app.layout = dbc.Container(container, fluid=True)
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)