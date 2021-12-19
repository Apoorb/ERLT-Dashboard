import pandas as pd
import numpy as np
import plotly.express as px
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import seaborn as sns
from dash.dependencies import Input, Output, State
from app import app
from dash import dash_table
import sys


def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0

    if sys.version_info < (3, 0):  # Pandas 1.0.0 does not support Python 2
        return "any"
    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return ("datetime",)
    elif (
        isinstance(df_column.dtype, pd.StringDtype)
        or isinstance(df_column.dtype, pd.BooleanDtype)
        or isinstance(df_column.dtype, pd.CategoricalDtype)
        or isinstance(df_column.dtype, pd.PeriodDtype)
        or pd.api.types.is_string_dtype(df_column)
    ):
        return "text"
    elif (
        isinstance(df_column.dtype, pd.SparseDtype)
        or isinstance(df_column.dtype, pd.IntervalDtype)
        or isinstance(df_column.dtype, pd.Int8Dtype)
        or isinstance(df_column.dtype, pd.Int16Dtype)
        or isinstance(df_column.dtype, pd.Int32Dtype)
        or isinstance(df_column.dtype, pd.Int64Dtype)
        or pd.api.types.is_numeric_dtype(df_column)
    ):
        return "numeric"
    else:
        return "any"


erlt_df = pd.read_csv("data/starts_df_final.csv")
erlt_df_long = (
    erlt_df.set_index(["Area", "yearid", "VehicleType", "FUELTYPE"])
    .stack()
    .reset_index()
)
erlt_df_long_fil = erlt_df_long.rename(
    columns={
        "Area": "Area",
        "yearid": "Year",
        "FUELTYPE": "Fuel Type",
        "VehicleType": "Vehicle Type",
        "level_4": "Pollutant",
        0: "Starts Emission Rate (grams/starts)",
    }
)
vehtypes = erlt_df_long_fil["Vehicle Type"].unique()

Pollutant_label_value = [
    {"label": pollutant, "value": pollutant}
    for pollutant in erlt_df_long_fil.Pollutant.unique()
]
area_label_value = [
    {"label": area, "value": area} for area in erlt_df_long.Area.unique()
]
dropdown_1 = dcc.Dropdown(
    id="area-dropdown",
    options=area_label_value,
    value="Austin",
    multi=False,
    className="dbc_dark",
    optionHeight=20,
)
dropdown_2 = dcc.Dropdown(
    id="pollutant-dropdown",
    options=Pollutant_label_value,
    value="CO",
    multi=False,
    className="dbc_dark",
    optionHeight=20,
)

title_1 = html.H3("MOVES 2014b Daily Composite Starts Emission Rates")


layout = dbc.Container(
    [
        dbc.Row(title_1, className="mb-0"),
        dbc.Row([dbc.Col(dropdown_1, width=3), dbc.Col(dropdown_2, width=3)]),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "MOVES 2014b Starts Emission Rates Plots",
                    className="text-center text-light bg-dark",
                ),
                body=True,
                style={"padding": "6px"},
            ),
            className="mt-3 mb-2",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id="starts_erlt_line", style={"width": "100%", "height": "600px"}
                ),
                className="col-md-8",
            )
        ),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "MOVES 2014b Starts Emission Rates Table",
                    className="text-center text-light bg-dark",
                ),
                body=True,
                style={"padding": "6px"},
            ),
            className="mt-4 mb-4",
        ),
        dbc.Row(
            dash_table.DataTable(
                id="datatable_interactivity_starts",
                columns=[
                    {"name": i, "id": i, "type": table_type(erlt_df_long_fil[i])}
                    for i in erlt_df_long_fil.columns
                ],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=20,
                style_header={"backgroundColor": "rgb(30, 30, 30)", "color": "white"},
                style_cell={
                    "backgroundColor": "rgb(50, 50, 50)",
                    "color": "white",
                    "whiteSpace": "normal",
                    "textAlign": "center",
                    "height": "auto",
                },
                style_cell_conditional=[
                    {"if": {"column_id": "Road Description"}, "width": "11%"},
                    {"if": {"column_id": "Average Speed Bin (mph)"}, "width": "10%"},
                ],
                style_filter={"height": "25px"},
                css=[{"selector": "table", "rule": "table-layout: fixed"}],
                # Wrap text
            ),
            className="dbc_dark",
        ),
    ],
    fluid=True,
    style={"padding-right": "40px", "padding-left": "40px"},
)


@app.callback(
    Output("datatable_interactivity_starts", "data"),
    [Input("area-dropdown", "value"), Input("pollutant-dropdown", "value")],
)
def update_table(area_val, pol_val):
    erlt_df_area_pol = erlt_df_long_fil.loc[
        (erlt_df_long_fil.Area == area_val) & (erlt_df_long_fil.Pollutant == pol_val)
    ]
    return erlt_df_area_pol.to_dict("records")


@app.callback(
    Output("starts_erlt_line", "figure"),
    [Input("area-dropdown", "value"), Input("pollutant-dropdown", "value")],
)
def update_starts_erlt_line(area_val, pol_val):
    plt_df = erlt_df_long_fil.loc[
        (erlt_df_long_fil.Area == area_val) & (erlt_df_long_fil.Pollutant == pol_val)
    ]
    fig = px.line(
        plt_df,
        color="Vehicle Type",
        line_dash="Fuel Type",
        line_dash_sequence=["solid", "dash"],
        x="Year",
        y="Starts Emission Rate (grams/starts)",
        category_orders={
            "Fuel Type": ["Gasoline", "Diesel"],
            "Vehicle Type": [
                "Combination Long-haul Truck",
                "Combination Short-haul Truck",
                "Single Unit Long-haul Truck",
                "Single Unit Short-haul Truck",
                "Motor Home",
                "Refuse Truck",
                "Intercity Bus",
                "School Bus",
                "Transit Bus",
                "Light Commercial Truck",
                "Passenger Truck",
                "Passenger Car",
                "Motorcycle",
            ],
        },
        template="plotly_dark",
        color_discrete_sequence=sns.color_palette("husl", 13).as_hex(),
    )
    fig.update_layout(
        uniformtext_minsize=12,
        font=dict(family="Time New Roman", size=14, color="white"),
    )
    return fig
