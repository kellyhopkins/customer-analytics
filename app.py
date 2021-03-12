import dash
import dash_core_components as dcc
import dash_html_components as html
# import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from whitenoise import WhiteNoise
# import sg

# File paths
data_path = 'data'
maps_dir = 'static/'

#Data
dtypes = {
    "poi_cbg": "object",
    "postal_code": "object",
}
# df = pd.read_csv(f"{data_path}/raw/safegraph/starbucks/oct/oct.csv", dtype=dtypes)[['location_name', 'street_address', 'city', 'region']]
popularity_by_hour = pd.read_csv(f"{data_path}/processed/popularity_by_hour.csv")
popularity_by_day = pd.read_csv(f"{data_path}/processed/popularity_by_day.csv")

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
days = {
    0: "Sunday",
    1:"Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}
hours = [*range(24)]

external_stylesheets = [os.path.join('style.css'), 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')

container = html.Div([

    dbc.Row([
        dbc.Col(html.Div([
            dbc.Jumbotron([
                html.H1("Using Customer Demographics in Brand Analysis", className="display-4"),
                html.H3("Analyzing foot traffic data from SafeGraph", className='lead'),
                html.Hr(className='my-2'),
                html.P("What factors draw customers to visit their favorite stores, even in a pandemic? In an new era of reduced travel and extra safety precautions, which brands have prevailed so far? These are some of the questions our team sought to answer through our capstone project as considered the economic impacts of the COVID-19 pandemic. By analyzing consumer shopping behavior, we hope to find trends about how people spend money in their communities."),
                html.P([
                    dbc.Button("Read the Report", color="outline-primary", href="https://s3.us-east-2.amazonaws.com/kelly-hopkins.com/Team+60+Final+Report.pdf", target="_blank"),
                    dbc.Button("Watch Presentation", color="outline-primary", href="https://youtu.be/a6cOmE1XzcY", target="_blank", className="mx-2"),
                    dbc.Button("View the Code", color="outline-primary", href="https://github.com/kellyhopkins/customer-analytics", target="_blank"),
                    ]),
            ])
        ], style={"color": "black"}))
    ]),

    dbc.Row([
        dbc.Col(width=1),
        dbc.Col([
            #################################################################################################################
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H1("Dunkin vs. Starbucks: Foot Traffic Share Oct-Dec 2020", className="text-center display-4")
                    ])
                ], width=12),
                dbc.Col([
                    html.Iframe(
                        height='800',
                        width='100%',
                        srcDoc= open(f"{maps_dir}test.html", 'r').read()
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                ])
            ]),

            dbc.Row([
                dbc.Col([html.Div([
                    html.H1("Popularity By Day", className="display-5 text-center"),
                    dcc.Graph(
                        figure= px.bar(
                            popularity_by_day,
                            x='day',
                            y='popularity',
                            color='brands',
                            barmode='group'
                        )
                    )
                ])], width=6),
                dbc.Col([html.Div([
                    html.H1("Popularity By Hour", className="display-5 text-center"),
                    dcc.Graph(
                        figure= px.line(
                            popularity_by_hour,
                            x='Hour',
                            y= ["Dunkin'", "Starbucks"],
                        )
                    )
                ])], width=6)
            ]),
            
            
            
            dbc.Row([
                dbc.Col([
                    html.Div(id='map'),
                    html.P("Filter Option: "),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Hour', 'value': 'Hour'},
                            {'label': 'Day', 'value': 'Day'},
                        ],
                        value='Day',
                        # labelStyle={'display': 'inline-block'},
                        id='filter-control'
                    ),
                    # html.Div(id='map'),
                    html.Div([
                        dcc.Slider(
                            id='slider',
                            min=0,
                            max=6,
                            value=0,
                            marks= days,
                            step=None
                        )
                    ], id='slider-control')
                ])
            ])

        #################################################################################################################
        ], width=10),
        dbc.Col(width=1)
    ]),

#end    
])


@app.callback(
    Output("slider-control", "children"),
    Input("filter-control", "value")
)
def slider_switch(value):
    if value == "Day":
        return dcc.Slider(
            id='slider',
            min=0,
            max=6,
            value= 0,
            marks= days,
            step=None
        )
    elif value == "Hour":
        return dcc.Slider(
            id='slider',
            min=0,
            max=23,
            value=0,
            marks = {x:str(x) for x in range(25)},
            step=None
        )


@app.callback(
    Output("map", "children"),
    Input("slider", "value"),
    Input("filter-control", "value")
)
def map_slider(selected, value):
    # if selected in list(days.keys()):
    if value == "Day":
        day = days[selected]
        map_file = f"{maps_dir}popularity_by_day_{day}.html"
        title = "Day"
        title2 = day
    else:
        map_file = f"{maps_dir}popularity_by_hour_{selected}.html"
        title = "Hour"
        title2 = selected
    frame = html.Iframe(
        height='600',
        width="100%",
        draggable="True",
        srcDoc=open(map_file, 'r').read()
    )
    return html.Div([
        html.H1(f"Popularity by {title}: {title2}", className='text-center'),
        frame
    ], className="mb-4")




# app.layout = dbc.Container(container, fluid=True, style={"background-color": "#644d77"})
app.layout = dbc.Container(container, fluid=True)
if __name__ == '__main__':
    # app.run_server(host="0.0.0.0", port="8050", debug=True)
    app.run_server(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), debug=True)