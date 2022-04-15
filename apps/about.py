from dash import dcc, html
import dash_bootstrap_components as dbc

from app import app

layout = html.Div([
    # Header container
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Predicting House Prices'))
        ]),
        dbc.Row([
            dbc.Col(html.Div('Cameron Yap, Emily Christiansen, Madeleine Thompson, and Stefan Lin'))
        ]),
        html.Br()
    ]),

    # Content container
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3('Title'))
        ]),
        dbc.Row([
            dbc.Col(html.Div('Text'))
        ]),
    ])
])