from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from apps import ui, home, about

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Data Exploration", href="/home"),
        dbc.DropdownMenuItem("User Interface", href="/ui"),
        dbc.DropdownMenuItem("About", href="/about"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/IO_logo_white.png", height="60px")),
                        dbc.Col(dbc.NavbarBrand("Index Zero")),
                    ],
                    align="center",
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', style={'padding': 10, 'flex': 1, 'margin-bottom': 10})
])

# Index Callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/ui':
        return ui.layout
    elif pathname == '/about':
        return about.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)