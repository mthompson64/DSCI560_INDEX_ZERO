from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import pandas as pd
from app import app

# Read in data somewhere else (getting some warnings on this)
data_df = pd.read_csv('data/agg_stats.csv')
data_df = data_df.sort_values(by=['median_rent'])

# Read in models here (?)


layout = html.Div([
    # Header container
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Predicting House Prices'))
        ]),
        dbc.Row([
            dbc.Col(html.Div('Cameron Yap, Emily Christiansen, Madeleine Thompson, and Stefan Lin'))
        ]),
    ]),

    dbc.Container([
        ### Add stuff to the page here
    ])
])