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


erlt_df = pd.read_csv("data/idle_df_final.csv")
erlt_df_long = erlt_df.set_index(["Area", "yearid"]).stack().reset_index()
erlt_df_long_fil = erlt_df_long.rename(
    columns={
        "Area": "Area",
        "yearid": "Year",
        "Processtype": "Process Type",
        "level_2": "Pollutant",
        0: "Idling Emission Rate (grams/hour)",
    }
)


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

title_1 = html.H3("MOVES 2014b Daily Composite Idling Emission Rates")


layout = dbc.Container(
    [
        dbc.Row(title_1, className="mb-0"),
        dbc.Row([dbc.Col(dropdown_1, width=3), dbc.Col(dropdown_2, width=3)]),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "MOVES 2014b Idling Emission Rates Plots",
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
                    id="idling_erlt_line", style={"width": "100%", "height": "600px"}
                ),
                className="col-md-8",
            )
        ),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "MOVES 2014b Idling Emission Rates Table",
                    className="text-center text-light bg-dark",
                ),
                body=True,
                style={"padding": "6px"},
            ),
            className="mt-4 mb-4",
        ),
        dbc.Row(
            dash_table.DataTable(
                id="datatable_interactivity",
                columns=[
                    {"name": i, "id": i, "type": table_type(erlt_df_long_fil[i])}
                    for i in erlt_df_long_fil.columns
                ],
                data=erlt_df_long_fil.to_dict("records"),
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
    Output("idling_erlt_line", "figure"), [Input("pollutant-dropdown", "value")]
)
def update_idling_erlt_line(pol_val):
    plt_df = erlt_df_long_fil.loc[(erlt_df_long_fil.Pollutant == pol_val)]
    ord_area = (
        plt_df.loc[plt_df.Year == 2020]
        .sort_values("Idling Emission Rate (grams/hour)")["Area"]
        .values
    )
    fig = px.line(
        plt_df,
        color="Area",
        line_dash="Area",
        x="Year",
        y="Idling Emission Rate (grams/hour)",
        color_discrete_sequence=sns.color_palette("husl", 13).as_hex(),
        category_orders=dict(Area=ord_area),
        template="plotly_dark",
    )
    fig.update_layout(
        uniformtext_minsize=12,
        font=dict(family="Time New Roman", size=14, color="white"),
    )
    return fig
