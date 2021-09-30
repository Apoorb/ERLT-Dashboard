import pandas as pd
import numpy as np
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import dash_table
import sys
# needed only if running this as a single page app
# external_stylesheets = [dbc.themes.DARKLY]
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead


erlt_df_2014b_3 = pd.read_csv("data/running_mvs_2014b_3.csv", index_col=0)
rename_map = {
    "moves": "MOVES",
    "District": "District",
    "year_id": "Year",
    "month": "Month",
    "day": "Day",
    "road_desc": "Road Description",
    "source_type_name": "Source Type",
    "fuel_type_desc": "Fuel Type",
    "pollutant_short_name": "Pollutant",
    "avg_bin_speed": "Average Speed (mph)",
    "avg_speed_bin_desc": "Average Speed Bin Description",
    "per_diff": "Percent Change in MOVES 3 Emissions",
    "rate_per_distance": "Running Emission Rate (grams/mile)",
}
hours = erlt_df_2014b_3.hour_id.unique()
hours_lab = "_".join([str(hour) for hour in hours])

erlt_df_2014b_3 = erlt_df_2014b_3.drop(columns="hour_id")
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


avgspeed_values = erlt_df_2014b_3_1["Average Speed (mph)"].unique()
avgspeed_values_marks_dict = {
    int(avg_speed) if avg_speed % 1 == 0 else avg_speed: f"{avg_speed}"
    for avg_speed in avgspeed_values
    if avg_speed % 5 == 0
}

avgspeed_values_marks_dict[2.5] = "2.5"
min_avgspeed = min(avgspeed_values)
max_avgspeed = max(avgspeed_values)

year_values = erlt_df_2014b_3_1["Year"].unique()

year_label_dict = [
    {"label": year, "value": year} for year in erlt_df_2014b_3_1.Year.unique()
]


title_1 = html.H3("MOVES 2014b vs. MOVES 3 Running Emission Comparison")
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
        return 'any'
    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime',
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype) or
            pd.api.types.is_string_dtype(df_column)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype) or
            pd.api.types.is_numeric_dtype(df_column)):
        return 'numeric'
    else:
        return 'any'


layout = dbc.Container(
    [
        dbc.Row(title_1, className="mb-0"),
        dbc.Row(dbc.Col(dropdown_2, width=3, align="left")),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "El Paso MOVES 2014b vs. 3 Running Emission Comparison by "
                    f"Road Type for Hour {hours_lab} – {int(hours_lab)+1} AM",
                    className="text-center text-light bg-dark",
                ),
                body=True,
                style={"padding": "6px"}
            ),
            className="mt-3 mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="erlt_comp_line", style={'width':'100%','height':'400px'}), className="mb-2 col-md-8"),
                dbc.Col(dcc.Graph(style={'width':'100%','height':'400px'}), className="mb-2 col-md-4"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.P("Select Vehicle Type:"), width=2),
                dbc.Col(
                    dbc.RadioItems(
                        id="sut-radio",
                        options=sut_label_value,
                        value="Passenger Car",
                        inline=True,
                    ),
                    width=10,
                ),
            ],
            justify="start",
            no_gutters=True,
            style={"height": "1.5rem", "font-size": "1rem"},
        ),
        dbc.Row(
            [
                dbc.Col(html.P("Select Fuel Type:"), width=2),
                dbc.Col(
                    dbc.RadioItems(
                        id="fuel-radio",
                        options=fuel_label_value,
                        value="Gasoline",
                        inline=True,
                    ),
                    width=10,
                ),
            ],
            justify="start",
            no_gutters=True,
            style={"height": "1.5rem", "font-size": "1rem"},
        ),
        dbc.Row(
            [
                dbc.Col(html.P("Select Analysis Year:"), width=2),
                dbc.Col(
                    dbc.RadioItems(
                        id="year-radio",
                        options=year_label_dict,
                        value=2020,
                        inline=True,
                    ),
                    width=4,
                ),
            ],
            justify="start",
            no_gutters=True,
            style={"height": "1.5rem", "font-size": "1rem"},
        ),
        dbc.Row(
            dbc.Card(
                html.H4(
                    "El Paso MOVES 2014b vs. 3 Running Emission "
                    f"Comparison Data for Hour "
                    f"{hours_lab} – {int(hours_lab)+1} AM",
                    className="text-center text-light bg-dark",
                ),
                body=True,
                style={"padding": "6px"}
            ),
            className="mt-4 mb-4",
        ),
        dbc.Row(
            dash_table.DataTable(
                    id='datatable_interactivity',
                    columns=[
                        {"name": i, "id": i, 'type': table_type(erlt_df_2014b_3_1[i])} for i in erlt_df_2014b_3_1.columns
                    ],
                    data=erlt_df_2014b_3_1.to_dict('records'),
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                    page_size=10,
                    style_header={'backgroundColor': 'rgb(30, 30, 30)',  'color': 'white'},
                    style_cell={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white',
                            'whiteSpace': 'normal',
                            'textAlign': 'center',
                            'height': 'auto'
                        },
                    style_filter={"height": "25px"},
                    css=[{
                            'selector': 'table',
                            'rule': 'table-layout: fixed'
                        }], # Wrap text

                ), className="dbc_dark"
        )
    ],
    fluid=True,
    style={"padding-right": "40px", "padding-left": "40px"}
    # Remove large margins on left and right.
)


@app.callback(Output("fuel-radio", "options"), Input("sut-radio", "value"))
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


@app.callback(Output("fuel-radio", "value"), Input("fuel-radio", "options"))
def set_fuel_value(available_options):
    return available_options[0]["value"]


@app.callback(
    Output("erlt_comp_line", "figure"),
    [
        Input("sut-radio", "value"),
        Input("fuel-radio", "value"),
        Input("pollutant-dropdown", "value"),
        Input("year-radio", "value"),
    ],
)
def update_line_chart(sut_val, fuel_val, pollutant_val, year_val):
    max_em = erlt_df_2014b_3_1.loc[
        lambda df: (df.Pollutant == pollutant_val), "Running Emission Rate (grams/mile)"
    ].values.max()

    min_em = 0

    erlt_df_2014_2014b_1_fil = erlt_df_2014b_3_1.loc[
        lambda df: (
            (df["Source Type"] == sut_val)
            & (df["Fuel Type"] == fuel_val)
            & (df.Pollutant == pollutant_val)
            & (df["Year"] == year_val)
        )
    ].assign(Year=lambda df: df.Year.astype(int))
    fig = px.line(
        data_frame=erlt_df_2014_2014b_1_fil,
        x="Average Speed (mph)",
        y="Running Emission Rate (grams/mile)",
        hover_data=rename_map.values(),
        line_dash="MOVES",
        color="MOVES",
        facet_col="Road Description",
        facet_col_wrap=2,
        template="plotly_dark",
    )

    fig.update_layout(
        font=dict(family="Time New Roman", size=17, color="white"),
        yaxis=dict(
            range=(2 * min_em, max_em * 1.2),
            showexponent="all",
            exponentformat="e",
            title_text="",
        ),
        xaxis=dict(
            range=(0, 80), showexponent="all", exponentformat="e", title_text=""
        ),
        yaxis3=dict(showexponent="all", exponentformat="e", title_text=""),
        xaxis2=dict(showexponent="all", exponentformat="e", title_text=""),
        hoverlabel=dict(font_size=14, font_family="Rockwell"),
    )
    fig.add_annotation(
        {
            "showarrow": False,
            "text": "Average Speed (mph)",
            "x": 0.5,
            "xanchor": "center",
            "xref": "paper",
            "y": 0,
            "yanchor": "top",
            "yref": "paper",
            "yshift": -30,
        }
    )
    fig.add_annotation(
        {
            "showarrow": False,
            "text": "Running Emission Rates (grams/mile)",
            "textangle": 270,
            "x": 0,
            "xanchor": "left",
            "xref": "paper",
            "y": 0.5,
            "yanchor": "middle",
            "yref": "paper",
            "xshift": -80,
        }
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
