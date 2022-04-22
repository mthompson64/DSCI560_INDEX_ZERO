from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import geopandas as gpd
from app import app

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'models/'))
# from ANN import load_model

# load_model()

# Mapbox Token
token = open(".mapbox_token").read()

### Read in data ###
data_df = pd.read_csv('data/agg_stats.csv')
census_data = gpd.read_file('data/census_tracts_2010.geojson')
zip_data = pd.read_csv('data/ZIP_tract_reference.csv')

# Merge data_df (NOT predicted data) and census_data
zip_data = zip_data.astype({'ZIP': str})

# get all of the unique zip codes
zip_list = ['All']
for ZIP in zip_data['ZIP'].unique().tolist():
    zip_list.append(ZIP)

data_df['geoid10'] = data_df['geoid2'].apply(lambda x: '0' + str(x))
geo_df = census_data.merge(data_df, on='geoid10').set_index('geoid')

# Save file
# geo_df.to_file('data/agg_stats.geojson', driver="GeoJSON")
data_df = data_df.sort_values(by=['median_rent'])

### Read in models here ###

### Read in figures here ###
# Want to make this part interactive with the proper Dash calls
# Want to format the hover text

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
        html.Label('Zip Code'),
        dcc.Dropdown(options=zip_list, value='All', id='zip_code'), # Input - value

        html.Br(),
        html.Label('Select Important Enviornmental Features'),
        dcc.Dropdown(['CES Score', 'Ozone', 'Diesel Emissions', "Drinking Water Contaminants", "Lead", "Pesticides", "Airborne Toxic Release", "Traffic", "Cleanup Sites", "Groundwater Threats", "Hazardous Waste", "Impaired Water Bodies", "Solid Waste"],
                     multi=True, id='dropdown'),

        html.Br(),
        html.Label('Individual Health and Wellbeing Factors'),
        dcc.Checklist(
        options = ['Asthma', 'Low Birth Weight', 'Cardiovascular Disease', "Education", "Linguistic Isolation", "Poverty", "Unemployment", "Housing Burden"],
        value = ['Asthma'],
        inline=False, id='checklist'
        ),

        # Don't make this part of the input, change so we get the price out when giving all of these inputs
        html.Br(),
        html.Label('Price Range'),
        dcc.RangeSlider(
            id='price_range',
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
            value=[0, 5000]), # Input - value

        html.Br(),
        dcc.Graph(id='choropleth') # Output - figure
    ])
])

# Choropleth graph
@app.callback(
    Output("choropleth", "figure"), 
    Input("zip_code", "value"),
    Input("price_range", "value"))
def display_choropleth(zip_code, price_range):
    def update_price(df, price):
        lower_bound = float(price[0])
        upper_bound = float(price[1])

        # Filter the dataframe on the rent being in the price range specified
        filtered_df = df.loc[(df['median_rent'] >= lower_bound) & (df['median_rent'] <= upper_bound)]
        return filtered_df

    # Output the filtered dataframe based on geo_df
    filtered_df = update_price(geo_df, price_range)

    # Output the dataframe for the choropleth map based on the zip code input
    if zip_code == 'All':
        choropleth_df = filtered_df
    else:
        list_geoids = zip_data.loc[zip_data['ZIP'] == zip_code, 'geoid'].tolist()
        # print(list_geoids)
        choropleth_df = filtered_df.loc[filtered_df['geoid2'].isin(list_geoids)]

    # Calls zip code here, want to do something with updating data based on zip code
    # Update this so that it doesn't reset the zoom every time you update something
    fig = px.choropleth_mapbox(
        choropleth_df,
        geojson = choropleth_df.geometry,
        locations = choropleth_df.index,
        color = choropleth_df.median_rent,
        range_color=(0, max(geo_df.median_rent)),
        zoom=8.5, center = {"lat": 34.0522, "lon": -118.2437},
        opacity=0.5, labels={'median_rent': 'Median Rent'},
        # hover_name = choropleth_df.geoid2,
        hover_data = [choropleth_df.median_rent, choropleth_df.TotalPopulation, choropleth_df.well_count]
    )

    # Add mapbox access token
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken = token)

    return fig