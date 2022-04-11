from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import geopandas as gpd
from app import app

### Read in data ###
data_df = pd.read_csv('data/agg_stats.csv')
census_data = gpd.read_file('data/census_tracts_2010.geojson')

# Merge data_df (NOT predicted data) and census_data
data_df['geoid10'] = data_df['geoid2'].apply(lambda x: '0' + str(x))
geo_df = census_data.merge(data_df, on='geoid10').set_index('geoid')

# Save file
geo_df.to_file('data/agg_stats.geojson', driver="GeoJSON")
data_df = data_df.sort_values(by=['median_rent'])

### Read in models here ###

### Read in figures here ###
# Want to make this part interactive with the proper Dash calls
# Want to format the hover text
# https://plotly.com/python/mapbox-county-choropleth/
choropleth = px.choropleth_mapbox(
    geo_df,
    geojson = geo_df.geometry,
    locations = geo_df.index,
    color = geo_df.median_rent,
    range_color=(0, max(data_df.median_rent)),
    zoom=8.5, center = {"lat": 34.0522, "lon": -118.2437},
    opacity=0.5
)
choropleth.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    mapbox_accesstoken = 'pk.eyJ1IjoibXRob21wc29uNjQiLCJhIjoiY2t2MDBubjN1N2hxdTJwbW4ydmpwZjJrOSJ9.9vnWqmcjY-SJjCX8PneymQ')

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
        dcc.Graph(figure=choropleth)
    ])
])