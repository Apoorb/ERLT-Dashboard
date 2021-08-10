import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


from app import server
from app import app
from pages import home, moves_2014b_3_running_comp, moves_2014b_2014_running_comp

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))

# building the navigation bar
# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem(
            "MOVES 2014b vs. 3 Running", href="/moves_2014b_3_running_comp"
        ),
        dbc.DropdownMenuItem(
            "MOVES 2014b vs. 2014 Running", href="/moves_2014b_2014_running_comp"
        ),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/emissions.png", height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "On-Road Emissions ERLT DASH", className="ml-2"
                            )
                        ),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [nav_item, dropdown],
                    className="ml-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
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
    elif pathname == "/moves_2014b_2014_running_comp":
        return moves_2014b_2014_running_comp.layout
    else:
        return home.layout


# embedding the navigation bar
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), navbar, html.Div(id="page-content")]
)

if __name__ == "__main__":
    # app.run_server(host="127.0.0.1", debug=True)
    app.run_server(debug=True)