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
    html.Div(children=[

        html.Label('Zip Code Input'),
        dcc.Input(value='90017', type='text'),

        html.Br(),
        html.Label('Select Important Enviornmental Features'),
        dcc.Dropdown(['CES Score', 'Ozone', 'Diesel Emissions', "Drinking Water Contaminants", "Lead", "Pesticides", "Airborne Toxic Release", "Traffic", "Cleanup Sites", "Groundwater Threats", "Hazardous Waste", "Impaired Water Bodies", "Solid Waste"],
                     multi=True),

        html.Br(),


        html.Label('Individual Health and Wellbeing Factors'),
        dcc.Checklist(
        ['Asthma', 'Low Birth Weight', 'Cardiovascular Disease', "Education", "Linguistic Isolation", "Poverty", "Unemployment", "Housing Burden"],
        ['Asthma', 'Low Birth Weight', 'Cardiovascular Disease', "Education", "Linguistic Isolation", "Poverty", "Unemployment", "Housing Burden"],
        inline=False
        ),
    
        # html.Label('Radio Items'),
        # dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),






        html.Br(),
        html.Label('Price Range'),
        dcc.RangeSlider(100, 10000, 1000, count=10, value=[2000, 4000])
    ])
])

# layout = html.Div([
#     # Header container
#     dbc.Container([
#         dbc.Row([
#             dbc.Col(html.H1('Predicting House Prices'))
#         ]),
#         dbc.Row([
#             dbc.Col(html.Div('Cameron Yap, Emily Christiansen, Madeleine Thompson, and Stefan Lin'))
#         ]),
#     ]),

#     dbc.Container([
#             dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal')

#     ])
# ])