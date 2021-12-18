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


erlt_df = pd.read_csv("data/idle_df_final.csv")

erlt_df_long = (
    erlt_df.set_index(["Area", "yearid"]).stack().reset_index()
)

erlt_df_long_fil = erlt_df_long.rename(
    columns={
        "Area": "Area",
        "yearid": "Year",
        "Processtype": "Process Type",
        "level_2": "Pollutants",
        0: "Idling Emission Rate (grams/hour)",
    }
)


plt_df = erlt_df_long_fil.loc[(erlt_df_long_fil.Pollutants=="CO")]

ord_area = plt_df.loc[plt_df.Year==2020].sort_values("Idling Emission Rate (grams/hour)")["Area"].values
fig = px.line(
    plt_df,
    color="Area",
    line_dash="Area",
    x="Year",
    y="Idling Emission Rate (grams/hour)",
    color_discrete_sequence=sns.color_palette("husl", 13).as_hex(),
    category_orders=dict(Area=ord_area)
)
import plotly.io as pio
pio.renderers.default = "browser"




layout = dbc.Container(html.P("Idling"))
