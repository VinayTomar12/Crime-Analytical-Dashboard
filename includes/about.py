
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
about = dbc.Container([
    html.Div(
        html.Div([
            html.H1("About"),
            html.P("There’s a lot of crime data. For almost every reported crime, there’s a paper or digital record of it somewhere, which means hundreds of thousands of data points – number of thefts, break-ins, assaults, and homicides as well as where and when the incidents occurred."),
        ])
        
    )
])