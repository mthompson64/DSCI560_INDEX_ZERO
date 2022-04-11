from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app import app

# Read in data somewhere else (getting some warnings on this)
data_df = pd.read_csv('data/agg_stats.csv')
data_df = data_df.sort_values(by=['median_rent'])
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

# Read in models here

# Read in figures here
fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

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
    # UI container
    dbc.Container([
        html.Br(),
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
        dcc.RangeSlider(
            id='price_range_slider',
            min=0,
            max=5000,
            step=500,
            marks={
                0: '$0',
                500: '$500',
                1000: '$1,000',
                1500: '$1,500',
                2000: '$2,000',
                2500: '$2,500',
                3000: '$3,000',
                3500: '$3,500',
                4000: '$4,000',
                4500: '$4,500',
                5000: '$5,000'
            },
            value=[2000, 3000]),

        html.Br(),
        dcc.Graph(figure=fig)
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