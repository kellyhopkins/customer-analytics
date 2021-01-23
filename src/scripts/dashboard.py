import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sg

data_path = '../../data'

df = pd.read_csv(f"{data_path}/processed/cbg_visits.csv").head(10)
median_ages = sg.calc_median_age(['wawa', 'starbucks']).set_index('brand')
age_groups = sg.calc_age(['wawa', 'starbucks']).set_index('brand')

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
        dbc.Col(width=1),
        dbc.Col([
        ##############################################################################################
            dbc.Row([
                ##### Title
                dbc.Col([html.H1("Demographic Panel 1", className='text-center display-4 mb-4')], width=12),
                html.Hr(style={"color":'black'}),
                ##### Left Column
                dbc.Col([
                    html.Div([
                        dbc.Card([
                            dbc.CardHeader("Wawa"),
                            dbc.CardBody([
                                html.H4(median_ages.median(axis=1)['wawa'].round(2), className='card-title'),
                                html.P("Median Age", className="card-text")
                            ])
                        ], className="text-center", color="primary", outline=True),
                        dcc.Graph(
                            id='pie-chart2',
                            figure = go.Figure(data=[go.Pie(labels= age_groups.loc['wawa'].keys(), values=age_groups.loc['wawa'].values, hole=.5)])
                        )
                    ])
                ], width=4, align="center"),
                ##### Middle Column
                dbc.Col([
                    dbc.Card([
                            dbc.CardHeader("Age"),
                            dbc.CardBody([
                                html.H4(median_ages.median().median().round(2), className='card-title'),
                                html.P("Median Age", className="card-text")
                            ])
                        ], className="text-center", color="dark", outline=True),
                    dcc.Graph(
                        id='age-graph',
                        figure= px.bar(median_ages.reset_index(), x='brand', y=['male_median_age', 'female_median_age'], barmode='group', width=800).update_layout(showlegend=False)
                    )
                ], width=4),
                ##### Right Column
                dbc.Col([
                    dbc.Card([
                            dbc.CardHeader("Starbucks"),
                            dbc.CardBody([
                                html.H4(median_ages.median(axis=1)['starbucks'].round(2), className='card-title'),
                                html.P("Median Age", className="card-text")
                            ])
                        ], className="text-center", color="danger", outline=True),
                    dcc.Graph(
                        id='pie-chart',
                        figure = go.Figure(data=[go.Pie(labels= age_groups.loc['starbucks'].keys(), values=age_groups.loc['starbucks'].values, hole=.5)])
                    )
                ], width=4)
            ], style={"background": "white"}, className="mb-4"),
            dbc.Row([
                dbc.Col([html.H1("Demographic Panel 2", className='text-center')], width=12),
                dbc.Col([html.P("Race Demographics", className='text-center')],width=3)
            ], style={"background": "white"}),
        ##############################################################################################
        ], width=10),
        dbc.Col(width=1)
    ])



#end
])



app.layout = dbc.Container(container, fluid=True, style={"background-color": "#644d77"})
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)