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


erlt_df = pd.read_csv("data/starts_df_final.csv")

erlt_df_long = (
    erlt_df.set_index(["Area", "yearid", "VehicleType", "FUELTYPE"]).stack().reset_index()
)

erlt_df_long_fil = erlt_df_long.rename(
    columns={
        "Area": "Area",
        "yearid": "Year",
        "FUELTYPE": "Fuel Type",
        "VehicleType": "Vehicle Type",
        "level_4": "Pollutants",
        0: "Starts Emission Rate (grams/starts)",
    }
)
#erlt_df_long_fil["Vehicle Type"] = erlt_df_long.FUELTYPE + " " + erlt_df_long.VehicleType
vehtypes = erlt_df_long_fil["Vehicle Type"].unique()


pal = sns.color_palette("viridis", 13)
plt_df = erlt_df_long_fil.loc[(erlt_df_long_fil.Area=="Austin") & (erlt_df_long_fil.Pollutants=="CO")]
fig = px.line(
    plt_df,
    color="Vehicle Type",
    line_dash="Fuel Type",
    line_dash_sequence=["solid", "dash"],
    x="Year",
    y="Starts Emission Rate (grams/starts)",
    category_orders={
        "Fuel Type": ["Gasoline", "Diesel"],
        "Vehicle Type": ['Combination Long-haul Truck', 'Combination Short-haul Truck', 'Single Unit Long-haul Truck', 'Single Unit Short-haul Truck', 'Motor Home', 'Refuse Truck', 'Intercity Bus', 'School Bus', 'Transit Bus', 'Light Commercial Truck', 'Passenger Truck', 'Passenger Car', 'Motorcycle']
    },
    color_discrete_sequence=sns.color_palette("husl", 13).as_hex()
)


layout = dbc.Container(html.P("Starts"))
