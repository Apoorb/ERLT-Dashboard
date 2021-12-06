import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

### Import Dash Instance ###
from app import app

# needed only if running this as a single page app
# external_stylesheets = [dbc.themes.DARKLY]
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# keep as layout when running in multi-page app.
# change to app.layout if running as single page app instead

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Project Report", className="card-title"),
            html.H5("Emission rate lookup table (ERLT) project report"),
            dbc.Button(
                "Report",
                href="https://ftp.txdot.gov/pub/txdot-info/env/toolkit/200-01-rpt.pdf",
                target="_blank",  # open in new page
                color="primary",
            ),
        ]
    )
)

second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3("ERLT Resources", className="card-title"),
            html.H5("ERLT data, report and other relevant resources."),
            dbc.Button(
                "Resources",
                href="https://www.txdot.gov/inside-txdot/division/environmental/compliance-toolkits/air-quality.html",
                target="_blank",  # open in new page
                color="primary",
            ),
        ]
    )
)

third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Code", className="card-title"),
            html.H5("Access code/ github repository for building this " "dashboard."),
            dbc.Button(
                "Github",
                href="https://github.com/Apoorb/multipage_faster_erlt_2",
                target="_blank",  # open in new page
                color="primary",
            ),
        ]
    )
)


cards = dbc.Row(
    dbc.CardGroup(
        [
            dbc.Col(first_card, width=4),
            dbc.Col(third_card, width=4),
            dbc.Col(second_card, width=4),
        ]
    ),
    justify="center",
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H2(
                        "Texas On-Road Emission Rate Lookup Table " "Dashboard",
                        className="text-center",
                    ),
                    className="mb-5 mt-5",
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H5(
                        children="This dashboard presents the "
                        "emission rates for nine Texas "
                        "districts. Emission rates are for "
                        "running, start, idling, "
                        "and extended idling processes. "
                        "Emissions are computed using MOVES "
                        "2014b."
                    ),
                    className="mb-4",
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H5(
                        children="It also presents a comparison of "
                        "emission rates between MOVES 2014b "
                        "and 3."
                    ),
                    className="mb-5",
                )
            ]
        ),
        cards,
        html.A(
            "Special thanks to Meredith Wan for providing a clear "
            "example of building multi-page dashboard with DASH.",
            href="https://towardsdatascience.com/beginners-guide-to-building-a-multi-page-dashboard-using-dash-5d06dbfc7599",
            target="_blank",  # open in new page
        ),
    ]
)

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)
