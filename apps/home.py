import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
# import plotly.express as px
import pandas as pd
from app import app


### TO RUN:
### cd <this_directory>
### python app.py

# Add external stylesheet (change from BOOTSTRAP if you don't like it)
# app = dash.Dash(name='index_zero', external_stylesheets=[dbc.themes.BOOTSTRAP])

#df = px.data.stocks()
data_df = pd.read_csv('data/agg_stats.csv')
data_df = data_df.sort_values(by=['median_rent'])


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

    # Dropdown menu
    dcc.Dropdown(id = 'dropdown',
        options = [
            {'label':'Ozone', 'value':'Ozone' },
            {'label': '# Oil Wells', 'value':'well_count'},
            {'label': 'Pollution (PM25 value)', 'value':'PM25'},
            ],
        value = 'well_count'),
    
    # Graph (change)
    dcc.Graph(id = 'bar_plot')
    ])
    
    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(dropdown_value):
    #print(dropdown_value)
    fig = go.Figure([go.Scatter(x = data_df['median_rent'], y = data_df['{}'.format(dropdown_value)],\
                     line = dict(color = 'firebrick', width = 4))
                     ])
    
    fig.update_layout(title = 'Data Exploration',
                      xaxis_title = 'Median Rent',
                      yaxis_title = str(dropdown_value)
                      )
    return fig  