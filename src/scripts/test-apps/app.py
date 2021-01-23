# Import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import plotly.express as px
import pandas as pd

import sg

# Read style of internet (css file)
external_stylesheets = [os.path.join('style.css'), 'https://codepen.io/chriddyp/pen/bWLwgP.css']


# Init my app dash and define my style CSS
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

wawa = sg.get_sg_data("wawa", "oct")
store = wawa.iloc[0]
data = sg.calc_visits_by_day(store).reset_index()


# Define my layout
# Adding more CSS styles
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

colors = {
    'background': 'white',
    'text': 'black'
}

# Define LAYOUT
#This use HTML tags
# html.H1 : The <h1> to <h6> tags are used to define HTML headings.
# html.Div : The <div> tag defines a division or a section in an HTML document.
#app.layout = html.Div(children=[
app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    
    html.H1(children=["Analyzing Foot Traffic Data"], style={"color":"black"}),

    html.Div(children=[
        html.H4("Visits by Day"),
        dcc.Graph(
            figure= px.line(data, 'index', 'visits')
        )
    ]),

    html.Div(children=[
        html.Label("Dropdown"),
        dcc.Dropdown(
            options= [{'label': i, 'value': i} for i in list(data['index'].values)],
            multi = True
        )
    ])

])

# Configuring APP running as Web 
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)