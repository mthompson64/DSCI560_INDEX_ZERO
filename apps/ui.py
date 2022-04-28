from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import geopandas as gpd
from app import app

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'models/'))
# from ANN import load_model

# Load output from model
# Load base case: no environmental features are changed, get predicted price per zip code
base_pred_price = pd.read_csv('data/avg_zip_pred_price.csv', names=['ZIP', 'pred_price'], header=0)
predictions_df = pd.read_csv('data/90001.csv')
predictions_df = predictions_df.rename({'PredictedPrice': 'pred_price'}, axis=1)
# print(test_df)

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
        dcc.Dropdown(options=zip_list, value='All', clearable=False, id='zip_code'), # Input - value

        # Features:
        # Ozone
        # Oil wells
        # PM25
        # Total population
        # Drinking water
        # Traffic
        # Lead
        # Hazardous waste
        html.Br(),
        html.Label('Select Important Enviornmental Features'),
        dcc.Dropdown(
            options = [
                {'label':'Ozone', 'value':'Ozone' },
                {'label': '# Oil Wells', 'value':'well_count'},
                {'label': 'Pollution (PM25 value)', 'value':'PM25'},
                # {'label': 'Total Population', 'value': 'TotalPopulation'},
                {'label': 'Drinking Water Quality', 'value': 'DrinkingWater'},
                {'label': 'Traffic', 'value': 'Traffic'},
                {'label': 'Lead', 'value': 'Lead'},
                {'label': 'Hazardous Waste', 'value': 'HazWaste'}
            ], multi=True, clearable=True, id='environment_features'
        ), 

        html.Br(),
        # Add button to calculate price
        dbc.Container([
            dbc.Button("Calculate Price", id="calculate_price", color="primary", className="me-1"),
            html.Span(id="price_output")
        ]),

        html.Br(),
        dcc.Graph(id='choropleth') # Output - figure
    ])
])

# Choropleth graph
@app.callback(
    Output("choropleth", "figure"), 
    Input("zip_code", "value"))
def display_choropleth(zip_code):
    # Output the dataframe for the choropleth map based on the zip code input
    if zip_code == 'All':
        choropleth_df = geo_df
    else:
        list_geoids = zip_data.loc[zip_data['ZIP'] == zip_code, 'geoid'].tolist()
        # print(list_geoids)
        choropleth_df = geo_df.loc[geo_df['geoid2'].isin(list_geoids)]

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

        # Hover data: Median rent, Total population, oil well count, Asthma, low birth, cardio, education, poverty, unemployment
        # Format this to look better
        hover_data = [choropleth_df.median_rent, choropleth_df.TotalPopulation, choropleth_df.well_count, choropleth_df.Asthma, choropleth_df.LowBirthWeight, choropleth_df.CardiovascularDisease, choropleth_df.Education, choropleth_df.Poverty, choropleth_df.Unemployment, choropleth_df.HousingBurden]
    )

    # Add mapbox access token
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken = token)

    return fig

# Calculate price callback
# Want the button to read in the user input for zip code and features when clicked
@app.callback(
    Output("price_output", "children"),
    Input("calculate_price", "n_clicks"),
    State("zip_code", "value"),
    State("environment_features", "value")
)
def on_button_click(n, zip_code, environment_features):
    total_features = ['DrinkingWater','HazWaste','Lead','Ozone','PM25','Traffic','well_count']
    # Check environmental features input
    if environment_features == None or environment_features == []:
        # Base case, no environmental features selected
        # Pull data from base_pred_price dataframe

        # Check zip code input
        if zip_code == 'All':
            output_df = base_pred_price
        else:
            output_df = base_pred_price.loc[base_pred_price['ZIP'] == int(zip_code)]
    else:
        # Case where environmental features are selected
        output_df = base_pred_price

        # Mask the dataframe based on the environment features selected
        masks = []
        for feature in total_features:
            if feature in environment_features:
                # Create mask
                m = predictions_df[f"{feature}"] == 1
            else:
                m = predictions_df[f"{feature}"] == 0
            masks.append(m)
        
        # Apply mask to predictions_df, save as masked_df
        masked_df = predictions_df[np.logical_and.reduce(masks)]

        # Check zip code input
        if zip_code == 'All':
            output_df = masked_df
        else:
            output_df = masked_df.loc[masked_df['ZIP'] == int(zip_code)]

    # Calculate the mean price (it should just be one value in the output_df except in the case of all zip codes being selected)
    price = output_df['pred_price'].mean()
    
    # Update on button click
    if n is None:
        return None
    else:
        return f"Predicted price: ${round(price, 2)}"