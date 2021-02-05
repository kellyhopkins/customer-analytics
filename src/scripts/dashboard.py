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

external_stylesheets = [os.path.join('style.css'), 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])




app.layout = dbc.Container(container, fluid=True, style={"background-color": "#644d77"})
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)