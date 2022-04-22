from dash import dcc, html
import dash_bootstrap_components as dbc

from app import app

cameron_yap = dbc.Card([
    dbc.CardImg(src='assets/cameron_yap_cropped.jpg'),
    dbc.CardBody([
        html.H4(
            html.A('Cameron Yap', href='https://www.linkedin.com/in/cameron-yap-9b8234119'),
            style={'text-align': 'center'})
    ])
])

emily_christiansen = dbc.Card([
    dbc.CardImg(src='assets/squidward.jpeg'),
    dbc.CardBody([
        html.H4(
            html.A('Emily Christiansen', href='https://www.linkedin.com/in/emily-christiansen-65a644117/'),
            style={'text-align': 'center'})
    ])
])

madeleine_thompson = dbc.Card([
    dbc.CardImg(src='assets/madeleine_thompson.png'),
    dbc.CardBody([
        html.H4(html.A('Madeleine Thompson', href='https://www.linkedin.com/in/madeleine-jane-thompson/'),
        style={'text-align': 'center'})
    ])
])

stefan_lin = dbc.Card([
    dbc.CardImg(src='assets/stefan_lin_cropped.jpeg'),
    dbc.CardBody([
        html.H4(
            html.A('Stefan Lin', href='https://www.linkedin.com/in/stefanemoses'),
            style={'text-align': 'center'})
    ])
])

layout = html.Div([
    # Header container
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Predicting House Prices'))
        ]),
        dbc.Row([
            dbc.Col(html.Div(
                'Cameron Yap, Emily Christiansen, Madeleine Thompson, and Stefan Lin'))
        ]),
        html.Br()
    ]),

    # Content container
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3('About us'))
        ]),
        dbc.Row([
            dbc.Col(html.Div("""
            Index Zero is a data analytics consulting team at the University of Southern California. Our members are ​​Cameron Yap, Emily Christiansen, Madeleine Thompson, and Stefan Lin. We are experts in technical data analytics and want to help you, residential renters, to find your next home in Los Angeles County.
            """))
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(cameron_yap),
            dbc.Col(emily_christiansen),
            dbc.Col(madeleine_thompson),
            dbc.Col(stefan_lin),
        ]),

        html.Br(),
        dbc.Row([
            dbc.Col(html.H3('About our project'))
        ]),
        dbc.Row([
            dbc.Col(html.Div("""
            We have developed predictive models to accurately forecast rent prices and analyze local rent level trends in relation to environmental quality metrics in Los Angeles County. This tool will serve as a predictive reference and could prove to be advantageous for a company to gain an informational edge over all other housing agencies. Our tool could also encourage state or local governments to pay attention to environmental trends in order to support the housing market in Los Angeles County.
            """))
        ]),

        html.Br(),
        dbc.Row([
            dbc.Col(html.H3("What's in this tool?"))
        ]),
        dbc.Row([
            dbc.Col(html.Div("""
            For all your rental needs, we have incorporated socio-environmental factors into our prediction model. What are your main concerns when renting a home? Do you worry about the surrounding socio-environmental issues such as safety, education, oil wells, air quality, and water pollution that can impact you and your partner, children and beloved furry friends? Our tool takes in your specific needs and concerns and helps you find the best locations and predicted price for your next rented home!
            """))
        ]),
    ])
])
