import dash
import dash_bootstrap_components as dbc
from flask import Flask

# bootstrap theme
# https://bootswatch.com/darkly/
external_stylesheets = [dbc.themes.DARKLY]

flask_server = Flask(__name__)
app = dash.Dash(__name__, server=flask_server, external_stylesheets=external_stylesheets)


server = app.server
app.config.suppress_callback_exceptions = True
