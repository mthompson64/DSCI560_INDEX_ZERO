from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import geopandas as gpd
from app import app

# Mapbox Token
token = open(".mapbox_token").read()

# Read in data somewhere else (getting some warnings on this)
data_df = pd.read_csv('data/agg_stats.csv')
data_df = data_df.sort_values(by=['median_rent'])

census_data = gpd.read_file('data/census_tracts_2010.geojson')

data_df['geoid10'] = data_df['geoid2'].apply(lambda x: '0' + str(x))
geo_df = census_data.merge(data_df, on='geoid10').set_index('geoid')

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

    # Content container
    dbc.Container([
        html.Br(),
        # Dropdown menu
        dcc.Dropdown(id = 'dropdown',
            options = [
                {'label':'Ozone', 'value':'Ozone' },
                {'label': '# Oil Wells', 'value':'well_count'},
                {'label': 'Pollution (PM25 value)', 'value':'PM25'},
                {'label': 'Total Population', 'value': 'TotalPopulation'},
                {'label': 'Drinking Water Quality', 'value': 'DrinkingWater'},
                {'label': 'Traffic', 'value': 'Traffic'}
                ],
            value = 'well_count'),
        
        # Graph (change, add more graphs here)
        dcc.Graph(id = 'data_exploration_histogram'),
        dcc.Graph(id = 'data_exploration_choropleth')
        ])
    ])
    
    
@app.callback(Output(component_id='data_exploration_histogram', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(dropdown_value):
    log_y = False

    # Change labels
    if dropdown_value == 'well_count':
        label = '# Oil Wells'
        log_y = True    # use a log scale for the # of wells only
    elif dropdown_value == 'PM25':
        label = 'Pollution (PM25)'
    elif dropdown_value == 'TotalPopulation':
        label = 'Total Population'
    elif dropdown_value == 'DrinkingWater':
        label = 'Drinking Water Quality'
    else:
        label = str(dropdown_value)

    fig = px.histogram(x=data_df['{}'.format(dropdown_value)], labels={'x': label}, log_y=log_y)
    fig.update_layout(bargap=0.2)

    return fig  


# Choropleth graph
@app.callback(
    Output("data_exploration_choropleth", "figure"), 
    Input("dropdown", "value"))
def display_choropleth(dropdown):
    if dropdown == 'well_count':
        label = '# Oil Wells'
    elif dropdown == 'PM25':
        label = 'Pollution (PM25)'
    elif dropdown == 'TotalPopulation':
        label = 'Total Population'
    elif dropdown == 'DrinkingWater':
        label = 'Drinking Water Quality'
    else:
        label = str(dropdown)

    choropleth_df = geo_df

    fig = px.choropleth_mapbox(
        choropleth_df,
        geojson = choropleth_df.geometry,
        locations = choropleth_df.index,
        color = choropleth_df['{}'.format(dropdown)],
        range_color=(0, max(choropleth_df['{}'.format(dropdown)])),
        zoom=8.5, center = {"lat": 34.0522, "lon": -118.2437},
        opacity=0.5,
        labels={'{}'.format(dropdown): label},
        # hover_name = choropleth_df.geoid2,
        # hover_data = [choropleth_df.median_rent, choropleth_df.TotalPopulation, choropleth_df.well_count]
    )

    # Add mapbox access token
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken = token)

    return fig