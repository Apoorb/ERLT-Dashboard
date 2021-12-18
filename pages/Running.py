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
        "level_4": "Pollutants",
        0: "Running Emission Rate (grams/mile)",
    }
)

erlt_df_long_fil["Road Description"].unique()

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

import plotly.io as pio

pio.renderers.default = "browser"
plt_test_df = erlt_df_long_fil.loc[
    (erlt_df_long_fil.Area == "Austin") & (erlt_df_long_fil.Pollutants == "CO")
]
fig = px.line_3d(
    plt_test_df,
    x="Average Speed (mph)",
    y="Year",
    z="Running Emission Rate (grams/mile)",
    line_group="Year",
    line_dash="Road Description",
    color="Road Description",
)
import plotly.graph_objects as go

# Filter to road type.
plt_test_df_filt = plt_test_df.loc[
    plt_test_df["Road Description"] == "Urban Restricted"
]
plt_test_df_filt_3d = plt_test_df_filt.pivot(
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
        y=plt_test_df_filt_3d.index,
        x=plt_test_df_filt_3d.columns,
        z=plt_test_df_filt_3d.values,
        colorscale=colorscale,
        colorbar=dict(lenmode="fraction", len=0.5),
    )
)
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    scene_camera_eye=dict(x=-2, y=-1, z=0.5),
    margin=dict(l=10, r=10, b=10, t=10),
)


fig = px.line(
    plt_test_df.loc[plt_test_df.Year == 2020],
    x="Average Speed (mph)",
    y="Running Emission Rate (grams/mile)",
    line_group="Road Description",
    color="Road Description",
    line_dash="Road Description",
)
fig = px.line(
    plt_test_df.loc[plt_test_df["Average Speed (mph)"] == 50],
    x="Year",
    y="Running Emission Rate (grams/mile)",
    line_group="Road Description",
    color="Road Description",
    line_dash="Road Description",
)


layout = dbc.Container(html.P("Running"))
