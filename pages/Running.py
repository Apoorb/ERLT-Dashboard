import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
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


erlt_df = pd.read_csv("data/running_df_final.csv", index_col=0)
erlt_df_long = (
    erlt_df.set_index(["Area", "yearid", "funclass", "avgspeed"]).stack().reset_index()
)
erlt_df_long_fil = erlt_df_long.rename(
    columns={
        "Area": "Area",
        "yearid": "Year",
        "funclass": "Road Description",
        "avgspeed": "Average Speed (mph)",
        "level_4": "Pollutant",
        0: "Running Emission Rate (grams/mile)",
    }
)
map_rdtype = {
    i: j
    for i, j in zip(
        ["Rural-Arterial", "Rural-Freeway", "Urban-Arterial", "Urban-Freeway"],
        [
            "Rural Restricted",
            "Rural Unrestricted",
            "Urban Restricted",
            "Urban Unrestricted",
        ],
    )
}
erlt_df_long_fil["Road Description"] = erlt_df_long_fil["Road Description"].map(
    map_rdtype
)

Pollutant_label_value = [
    {"label": pollutant, "value": pollutant}
    for pollutant in erlt_df_long_fil.Pollutant.unique()
]

rdtype_label_value = [
    {"label": rdtype, "value": rdtype} for rdtype in map_rdtype.values()
]

area_label_value = [
    {"label": area, "value": area} for area in erlt_df_long.Area.unique()
]


title_1 = html.H3("MOVES 2014b Daily Composite Running Emission Rates")
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
dropdown_3 = dcc.Dropdown(
    id="rdtype-dropdown",
    options=rdtype_label_value,
    value="Rural Restricted",
    multi=False,
    className="dbc_dark",
    optionHeight=20,
)

layout = dbc.Container(
    [
        dbc.Row(title_1, className="mb-0"),
        dbc.Row(
            [
                dbc.Col(dropdown_1, width=3),
                dbc.Col(dropdown_2, width=3),
                dbc.Col(dropdown_3, width=3),
            ]
        ),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "MOVES 2014b Running Emission Rates Plots",
                    className="text-center text-light bg-dark",
                ),
                body=True,
                style={"padding": "6px"},
            ),
            className="mt-3 mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="run_erlt_3d", style={"width": "100%", "height": "600px"}
                    ),
                    className="col-md-8",
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            dcc.Graph(
                                id="run_erlt_by_spd",
                                style={"width": "100%", "height": "296px"},
                            ),
                            className="mb-2",
                        ),
                        dbc.Row(
                            dcc.Graph(
                                id="run_erlt_by_yr",
                                style={"width": "100%", "height": "296px"},
                            )
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "MOVES 2014b Running Emission Rates Table",
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
    Output("run_erlt_3d", "figure"),
    [
        Input("area-dropdown", "value"),
        Input("pollutant-dropdown", "value"),
        Input("rdtype-dropdown", "value"),
    ],
)
def update_3d_surf(area_val, pol_val, rdtype_val):
    erlt_df_area_pol = erlt_df_long_fil.loc[
        (erlt_df_long_fil.Area == area_val) & (erlt_df_long_fil.Pollutant == pol_val)
    ]
    erlt_df_area_pol_rdtype = erlt_df_area_pol.loc[
        erlt_df_area_pol["Road Description"] == rdtype_val
    ]
    erlt_df_area_pol_rdtype_3d = erlt_df_area_pol_rdtype.pivot(
        index="Year",
        columns="Average Speed (mph)",
        values="Running Emission Rate (grams/mile)",
    )
    colorscale = [[0, "gold"], [0.5, "mediumturquoise"], [1, "lightsalmon"]]
    fig = go.Figure(
        go.Surface(
            contours={
                "z": {
                    "show": True,
                    "usecolormap": True,
                    "highlightcolor": "limegreen",
                    "project_z": True,
                }
            },
            y=erlt_df_area_pol_rdtype_3d.index,
            x=erlt_df_area_pol_rdtype_3d.columns,
            z=erlt_df_area_pol_rdtype_3d.values,
            colorscale=colorscale,
            colorbar=dict(lenmode="fraction", len=0.5, x=0.9),
        )
    )
    fig.update_layout(
        uniformtext_minsize=12,
        font=dict(family="Time New Roman", size=14, color="white"),
        scene=dict(
            camera_eye=dict(x=-2, y=-1, z=0.5),
            xaxis_title="Year",
            yaxis_title="Average Speed (mph)",
            zaxis_title="Running Emission (gram/mile)",
        ),
        template="plotly_dark",
        margin=dict(l=2, r=2, b=2, t=2),
    )
    return fig


@app.callback(
    Output("run_erlt_by_spd", "figure"),
    [
        Input("run_erlt_3d", "clickData"),
        Input("area-dropdown", "value"),
        Input("pollutant-dropdown", "value"),
    ],
)
def update_run_erlt_by_spd(clickdata, area_val, pol_val):
    if clickdata is None:
        x_speed = 2.5
    else:
        x_speed = clickdata["points"][0]["x"]
    erlt_df_area_pol_rdtype_spd = erlt_df_long_fil.loc[
        lambda df: (
            (df["Area"] == area_val)
            & (df.Pollutant == pol_val)
            & (df["Average Speed (mph)"] == x_speed)
        )
    ]
    fig = px.line(
        erlt_df_area_pol_rdtype_spd,
        x="Year",
        y="Running Emission Rate (grams/mile)",
        line_group="Road Description",
        color="Road Description",
        line_dash="Road Description",
        template="plotly_dark",
    )
    fig.update_layout(
        uniformtext_minsize=12,
        font=dict(family="Time New Roman", size=14, color="white"),
        xaxis=dict(title=""),
    )
    fig.add_annotation(
        text=f"Average Speed: {x_speed}",
        xref="paper",
        yref="paper",
        x=0,
        y=1,
        showarrow=False,
        font_size=16,
    )
    return fig


@app.callback(
    Output("run_erlt_by_yr", "figure"),
    [
        Input("run_erlt_3d", "clickData"),
        Input("area-dropdown", "value"),
        Input("pollutant-dropdown", "value"),
    ],
)
def update_run_erlt_by_yr(clickdata, area_val, pol_val):
    if clickdata is None:
        y_year = 2020
    else:
        y_year = clickdata["points"][0]["y"]
    erlt_df_area_pol_rdtype_yr = erlt_df_long_fil.loc[
        lambda df: (
            (df["Area"] == area_val)
            & (df.Pollutant == pol_val)
            & (df["Year"] == y_year)
        )
    ]
    fig = px.line(
        erlt_df_area_pol_rdtype_yr,
        x="Average Speed (mph)",
        y="Running Emission Rate (grams/mile)",
        line_group="Road Description",
        color="Road Description",
        line_dash="Road Description",
        template="plotly_dark",
    )
    fig.update_layout(
        uniformtext_minsize=12,
        font=dict(family="Time New Roman", size=14, color="white"),
        xaxis=dict(title=""),
    )
    fig.add_annotation(
        text=f"Year: {y_year}",
        xref="paper",
        yref="paper",
        x=0,
        y=1,
        showarrow=False,
        font_size=16,
    )
    return fig
