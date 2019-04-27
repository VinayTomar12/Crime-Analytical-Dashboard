import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'CAD'
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href="/about")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Insights:", header=True),
                dbc.DropdownMenuItem("Crime Against Women", href="/page-1"),
                dbc.DropdownMenuItem("Property Crimes", href="/page-2"),
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


about = dbc.Container([
    html.Div(
        html.Div([
            html.H1("About"),
            html.P("There’s a lot of crime data. For almost every reported crime, there’s a paper or digital record of it somewhere, which means hundreds of thousands of data points – number of thefts, break-ins, assaults, and homicides as well as where and when the incidents occurred."),
        ])
        
    )
])
# define content for page 1
page1 = dbc.Card(
    [
        dbc.CardTitle("Page 1 contents"),
        html.Div([
            html.H1('Page 1')
        ]),

    ],
    body=True,
)

# define content for page 2

tab1 = dbc.Card(
    [
        dbc.CardTitle("Page 2, tab 1 contents"),
        dbc.CardText("You can replace this with whatever you like"),
    ],
    body=True,
)

tab2 = dbc.Card(
    [
        dbc.CardTitle("Page 2, tab 1 contents"),
        dbc.CardText("Let's write something different here for fun"),
    ],
    body=True,
)

page2 = dbc.Tabs(
    [
        dbc.Tab(tab1, label="Tab 1", className="mt-3"),
        dbc.Tab(tab2, label="Tab 2", className="mt-3"),
    ]
)

# define page layout
app.layout = html.Div(
    [        
        dcc.Location(id="url", pathname="/home"),
        navbar,
        dbc.Container(id="content", style={"padding": "20px"}),
      
    ]
)


# create callback for modifying page layout
@app.callback(Output("content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/home":
        return home
    if pathname == "/about":
        return about
    if pathname == "/page-1":
        return page1
    if pathname == "/page-2":
        return page2
    # if not recognised, return 404 message
    return html.P("404 - page not found")


if __name__ == "__main__":
    app.run_server(debug=True)