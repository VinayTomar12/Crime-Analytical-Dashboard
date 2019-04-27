import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

home = dbc.Container(
    [
       html.Br(),
       dbc.Container(
           [
           html.H1("Crime Analytical Dashboard", className="display-3"),
           html.P(
                "A dasboard for complete insights about Crimes in India. "
                "For Crime Analysts, researchers, law enforcement agencies",
                 className="lead",
           ),
           html.Hr(className="my-2"),
           html.P(
               "Provides Interactive and"
               " Exploratory visualizations."
           ),
         
        ])
],style={'height':'100%'})