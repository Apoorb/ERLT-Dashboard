import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
### Import Dash Instance ###
from app import app
# needed only if running this as a single page app
# external_stylesheets = [dbc.themes.DARKLY]
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead

layout = html.Div("B")
