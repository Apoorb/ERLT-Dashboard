import pandas as pd
import numpy as np
import plotly.express as px
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
from dash import dash_table
import sys

erlt_df_2014b_3 = pd.read_csv("data/extnidle_mvs_2014b_3.csv", index_col=0)
rename_map = {
    "moves": "MOVES",
    "District": "District",
    "year_id": "Year",
    "month": "Month",
    "day": "Day",
    "hour_id": "Hour",
    "source_type_name": "Source Type",
    "fuel_type_desc": "Fuel Type",
    "pollutant_short_name": "Pollutant",
    "per_diff": "Percent Change in MOVES 3 Emissions",
    "rate_per_hour": "Extended Idling Emission Rate (grams/hour)",
}
hours = erlt_df_2014b_3.hour_id.unique()
hours_lab = "_".join([str(hour) for hour in hours])
erlt_df_2014b_3["moves"] = erlt_df_2014b_3.moves.map(
    {"MOVES 2014b": "2014b", "MOVES 3": "3"}
)
erlt_df_2014b_3["source_type_name"] = erlt_df_2014b_3.source_type_name.map(
    {"Passenger Car": "PC", "Combination Long-haul Truck": "CLhT"}
)
erlt_df_2014b_3["fuel_type_desc"] = erlt_df_2014b_3.fuel_type_desc.map(
    {"Gasoline": "Gas", "Diesel Fuel": "Diesel"}
)
# Only has hour 9 in it
erlt_df_2014b_3_1 = erlt_df_2014b_3.rename(columns=rename_map).filter(
    items=rename_map.values()
)
sut_label_value = [
    {"label": sut, "value": sut} for sut in erlt_df_2014b_3_1["Source Type"].unique()
]
fuel_label_value = [
    {"label": fuel_ty, "value": fuel_ty}
    for fuel_ty in erlt_df_2014b_3_1["Fuel Type"].unique()
]
pollutants_label_value = [
    {"label": pollutant, "value": pollutant}
    for pollutant in erlt_df_2014b_3_1.Pollutant.unique()
]
year_values = erlt_df_2014b_3_1["Year"].unique()
year_label_dict = [
    {"label": year, "value": year} for year in erlt_df_2014b_3_1.Year.unique()
]
title_1 = html.H3("MOVES 2014b vs. MOVES 3 Idling Emission Comparison")
dropdown_2 = dcc.Dropdown(
    id="pollutant-dropdown",
    options=pollutants_label_value,
    value="CO",
    multi=False,
    className="dbc_dark",
    optionHeight=20,
)


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


layout = dbc.Container(
    [
        dbc.Row(title_1, className="mb-0"),
        dbc.Row(dbc.Col(dropdown_2, width=3, align="left")),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "El Paso MOVES 2014b vs. 3 Extended Idling Emission Comparison "
                    f"for Hour {hours_lab} – {int(hours_lab)+1} AM",
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
                        id="erlt_comp_line_extidle", style={"width": "100%", "height": "400px"}
                    ),
                    className="mb-2 col-md-8",
                )
        ),
        dbc.Row(
            [
                dbc.Col(html.P("Select Vehicle Type:"), width=2),
                dbc.Col(
                    dbc.RadioItems(
                        id="sut-radio", options=sut_label_value, value="CLhT", inline=True
                    ),
                    width=10,
                ),
            ],
            justify="fuel-radio-extidle",
            no_gutters=True,
            style={"height": "1.5rem", "font-size": "1rem"},
        ),
        dbc.Row(
            [
                dbc.Col(html.P("Select Fuel Type:"), width=2),
                dbc.Col(
                    dbc.RadioItems(
                        id="fuel-radio-extidle",
                        options=fuel_label_value,
                        value="Gasoline",
                        inline=True,
                    ),
                    width=10,
                ),
            ],
            justify="fuel-radio-extidle",
            no_gutters=True,
            style={"height": "1.5rem", "font-size": "1rem"},
        ),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "El Paso MOVES 2014b vs. 3 Idling Emission "
                    f"Comparison Data for Hour "
                    f"{hours_lab} – {int(hours_lab)+1} AM",
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
                    {"name": i, "id": i, "type": table_type(erlt_df_2014b_3_1[i])}
                    for i in erlt_df_2014b_3_1.columns
                ],
                data=erlt_df_2014b_3_1.to_dict("records"),
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
                style_filter={"height": "25px"},
                css=[{"selector": "table", "rule": "table-layout: fixed"}],  # Wrap text
            ),
            className="dbc_dark",
        ),
    ],
    fluid=True,
    style={"padding-right": "40px", "padding-left": "40px"}
)


@app.callback(Output("fuel-radio-extidle", "options"), Input("sut-radio", "value"))
def set_fuel_options(selected_sut):
    fuel_sut_type_comb = (
        erlt_df_2014b_3_1[["Fuel Type", "Source Type"]]
        .drop_duplicates()
        .set_index("Source Type")
    )
    return [
        {"label": i, "value": i}
        for i in np.ravel(fuel_sut_type_comb.loc[selected_sut].values)
    ]


@app.callback(Output("fuel-radio-extidle", "value"), Input("fuel-radio-extidle", "options"))
def set_fuel_value(available_options):
    return available_options[0]["value"]


@app.callback(
    Output("erlt_comp_line_extidle", "figure"),
    [
        Input("sut-radio", "value"),
        Input("fuel-radio-extidle", "value"),
        Input("pollutant-dropdown", "value"),
    ],
)
def update_bar_chart(sut_val, fuel_val, pollutant_val):
    max_em = erlt_df_2014b_3_1.loc[
        lambda df: (df.Pollutant == pollutant_val), "Extended Idling Emission Rate (grams/hour)"
    ].values.max()

    min_em = 0

    erlt_df_2014_2014b_1_fil = erlt_df_2014b_3_1.loc[
        lambda df: (
            (df["Source Type"] == sut_val)
            & (df["Fuel Type"] == fuel_val)
            & (df.Pollutant == pollutant_val)
        )
    ].assign(Year=lambda df: df.Year.astype(int))

    fig = px.bar(
        data_frame=erlt_df_2014_2014b_1_fil,
        x="Year",
        y="Extended Idling Emission Rate (grams/hour)",
        hover_data=rename_map.values(),
        color="MOVES",
        barmode="group",
        pattern_shape_sequence=["+", "x"],
        template="plotly_dark",
    )

    fig.update_layout(
        font=dict(family="Time New Roman", size=16, color="white"),
        yaxis=dict(
            range=(min_em, max_em * 1.2), showexponent="all", exponentformat="e"
        ),
        xaxis=dict(showexponent="all", exponentformat="e", title_text="Year"),
        hoverlabel=dict(font_size=16, font_family="Rockwell"),
    )
    return fig






