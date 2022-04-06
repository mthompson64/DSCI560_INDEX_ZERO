from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# import dash_table

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

    # Content container
    dbc.Container([
        # Dropdown menu
        dcc.Dropdown(id = 'dropdown',
            options = [
                {'label':'Ozone', 'value':'Ozone' },
                {'label': '# Oil Wells', 'value':'well_count'},
                {'label': 'Pollution (PM25 value)', 'value':'PM25'},
                ],
            value = 'well_count'),
        
        # Graph (change, add more graphs here)
        dcc.Graph(id = 'scatter_plot')
        ])
    ])
    
    
@app.callback(Output(component_id='scatter_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(dropdown_value):
    fig = go.Figure([go.Scatter(x = data_df['median_rent'], y = data_df['{}'.format(dropdown_value)],\
                     line = dict(color = 'firebrick', width = 4))
                     ])
    
    fig.update_layout(title = 'Data Exploration',
                      xaxis_title = 'Median Rent',
                      yaxis_title = str(dropdown_value)
                      )
    return fig  