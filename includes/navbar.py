import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href="/about")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Insights:", header=True),
                dbc.DropdownMenuItem("Crime Against Women", href="caw"),
                dbc.DropdownMenuItem("Property Crimes", href="/#"),
            ],
            nav=True,
            in_navbar=True,
            label="Crime Insights",
        ),
    ],
    brand="CAD",
    brand_href="home",
    color="dark",
    dark=True,
    sticky="top",
)