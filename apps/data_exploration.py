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
        dbc.Row([
            dbc.Col([
                html.H3('Data Exploration')
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div('Select a feature to visualize the data:')
            ])
        ]),

        # Dropdown menu
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
        dcc.Dropdown(id = 'dropdown',
            options = [
                {'label': 'Ozone', 'value':'Ozone' },
                {'label': '# Oil Wells', 'value':'well_count'},
                {'label': 'Pollution (PM25 value)', 'value':'PM25'},
                {'label': 'Total Population', 'value': 'TotalPopulation'},
                {'label': 'Drinking Water Quality', 'value': 'DrinkingWater'},
                {'label': 'Traffic', 'value': 'Traffic'},
                {'label': 'Lead', 'value': 'Lead'},
                {'label': 'Hazardous Waste', 'value': 'HazWaste'}
                ],
            value = 'PM25'),
        
        html.Div(id="feature_explanation", style={'font-style': 'italic'}),
        
        # Graph (change, add more graphs here)
        # dbc.Row([
        #     dbc.Col(dcc.Graph(id = 'data_exploration_histogram')),
        #     dbc.Col(dcc.Graph(id = 'data_exploration_choropleth'))
        # ])
        html.Br(),
        html.H4('Choropleth Map'),
        dcc.Graph(id = 'data_exploration_choropleth'),
        html.Br(),
        dcc.Graph(id = 'data_exploration_histogram')
        ])
    ])
    

# Histogram callback
@app.callback(Output(component_id='data_exploration_histogram', component_property= 'figure'),
              Input(component_id='dropdown', component_property= 'value'))
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
    elif dropdown_value =='HazWaste':
        label = 'Hazardous Waste'
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
    elif dropdown =='HazWaste':
        label = 'Hazardous Waste'
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
        color_continuous_scale='viridis',
        mapbox_style='light'
        # hover_name = choropleth_df.geoid2,
        # hover_data = [choropleth_df.median_rent, choropleth_df.TotalPopulation, choropleth_df.well_count]
    )

    # Add mapbox access token
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken = token)

    return fig

@app.callback(
    Output("feature_explanation", "children"), 
    Input("dropdown", "value"))
def add_explanation(dropdown):
    # Want to add a feature explanation from the data dictionary for each selected feature

    # Possible features:
        # Ozone
        # Oil wells
        # PM25
        # Total population
        # Drinking water
        # Traffic
        # Lead
        # Hazardous waste
    if dropdown == 'Ozone':
        return "O3 concentration measured as parts per million (ppm). In 2015, the EPA established 0.070 ppm as the standard."
    elif dropdown == 'well_count':
        return "Count of oil well sites within the area's boundaries."
    elif dropdown == 'PM25':
        return "Annual mean of particulate matter concentrations, measured in micrograms per cubic meter of air."
    elif dropdown == 'TotalPopulation':
        return "Total number of individuals residing within the area's boundaries."
    elif dropdown == 'DrinkingWater':
        return "Average concentrations of 14 commonly identified contaminants in region's primary drinking water supply."
    elif dropdown == 'Traffic':
        return "Density of vehicles on the roads, measured in vehicle-kilometers per hour per road length."
    elif dropdown == 'Lead':
        return "Risk for lead exposure, based on children, high-poverty populations, and older housing structures being more prone to lead contamination."
    elif dropdown == 'HazWaste':
        return "Count of hazardous waste facilities within the area's boundaries, weighted by proximity to residential areas."
    else:
        return "None selected!"