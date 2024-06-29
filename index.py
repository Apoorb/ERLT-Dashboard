from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


from my_app import server
from my_app import app
from pages import (
    Running,
    Starts,
    Idling,
    ExtendedIdling,
    home,
    moves_2014b_3_running_comp,
    moves_2014_3_starts_comp,
    moves_2014b_3_idling_comp,
    moves_2014b_3_extidle_comp,
)

# make a reuseable navitem for the different examples
nav_item_h = dbc.NavItem(dbc.NavLink("Home", href="/home"))
nav_item_r = dbc.NavItem(dbc.NavLink("Running", href="/Running"))
nav_item_s = dbc.NavItem(dbc.NavLink("Starts", href="/Starts"))
nav_item_i = dbc.NavItem(dbc.NavLink("Idling", href="/Idling"))
nav_item_ei = dbc.NavItem(dbc.NavLink("Extended Idling", href="/ExtendedIdling"))

# building the navigation bar
# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home", className="h5"),
        dbc.DropdownMenuItem(
            "MOVES 2014b vs. 3 Running",
            href="/moves_2014b_3_running_comp",
            className="h5",
        ),
        dbc.DropdownMenuItem(
            "MOVES 2014b vs. 3 Starts", href="/moves_2014_3_starts_comp", className="h5"
        ),
        dbc.DropdownMenuItem(
            "MOVES 2014b vs. 3 Idling",
            href="/moves_2014b_3_idling_comp",
            className="h5",
        ),
        dbc.DropdownMenuItem(
            "MOVES 2014b vs. 3\nExtended Idling",
            href="/moves_2014b_3_extidle_comp",
            className="h5",
        ),
    ],
    nav=True,
    in_navbar=True,
    label="ERLT Comparisons",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src="/assets/emissions.png", height="20px")),
                    dbc.Col(
                        dbc.NavbarBrand(
                            "On-Road ERLTs",
                            className="ml-2",
                            style={"font-size": "20px"},
                        )
                    ),
                ],
                align="center",
                className="g-0",
            ),
            href="/home",
        ),
        dbc.NavbarToggler(id="navbar-toggler2"),
        dbc.Collapse(
            dbc.Nav(
                # right align dropdown menu with ml-auto className
                [nav_item_h, nav_item_r, nav_item_s, nav_item_i, nav_item_ei, dropdown],
                navbar=True,
                className="ml-auto",
                style={
                    "padding-right": "100px",
                    "padding-left": "20px",
                },  # Remove large margins on left and right.
            ),
            id="navbar-collapse2",
            navbar=True,
        ),
    ],
    color="dark",
    dark=True,
    className="h5",
)


@app.callback(
    Output("navbar-collapse2", "is_open"),
    [Input("navbar-toggler2", "n_clicks")],
    [State("navbar-collapse2", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/moves_2014b_3_running_comp":
        return moves_2014b_3_running_comp.layout
    elif pathname == "/moves_2014_3_starts_comp":
        return moves_2014_3_starts_comp.layout
    elif pathname == "/moves_2014b_3_idling_comp":
        return moves_2014b_3_idling_comp.layout
    elif pathname == "/moves_2014b_3_extidle_comp":
        return moves_2014b_3_extidle_comp.layout
    elif pathname == "/Running":
        return Running.layout
    elif pathname == "/Starts":
        return Starts.layout
    elif pathname == "/Idling":
        return Idling.layout
    elif pathname == "/ExtendedIdling":
        return ExtendedIdling.layout
    else:
        return home.layout


# embedding the navigation bar
app.layout = dbc.Container(
    [dcc.Location(id="url", refresh=False), navbar, html.Div(id="page-content")],
    fluid=True,
    style={
        "padding-right": "0px",
        "padding-left": "0px",
    },  # Remove large margins on left and right.
)

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8000')
    # app.run_server(debug=True)
