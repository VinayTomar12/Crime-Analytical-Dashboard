from includes.about import about
from includes.navbar import navbar
from includes.home import home
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go 
from dash.dependencies import Input,Output,State
import dash_table
import io
import base64
import datetime



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,external_stylesheets])
app.config['suppress_callback_exceptions']=True
app.title = 'CAD'
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# ========================== Data Processing ===============================================
df = pd.read_excel('Data/crime2014.xlsx')
tf = df
# print(df.head())
cols = df.columns
# Year list:
year_options = []
for year in df['Year'].unique():
    year_options.append({'label':str(year),'value':year})
state_options = []
for state in df['State/UT'].unique():
    state_options.append({'label':str(state),'value':state})

minYear = df['Year'].min()
maxYear = df['Year'].max()
#Crime head dictionary-LIST:
#With Sum aggr:
crimeDictS = {'Rape':sum, 'Kidnapping & Abduction':sum,'Dowry Deaths':sum,'Assault on women with intent to outrage her modesty ':sum,'Insult to modesty of women':sum,'Cruelty by Husband or his Relatives':sum,'Importation of Girls from foreign country':sum,'Immoral Traffic (P) Act':sum,'Dowry Prohibition Act':sum,'Indecent Representation of Women(P) Act':sum,'Commission of Sati Prevention Act':sum}
#Without aggr list:
crimeDict = ['Rape', 'Kidnapping & Abduction', 'Dowry Deaths','Assault on women with intent to outrage her modesty ','Insult to modesty of women', 'Cruelty by Husband or his Relatives','Importation of Girls from foreign country', 'Immoral Traffic (P) Act','Dowry Prohibition Act', 'Indecent Representation of Women(P) Act','Commission of Sati Prevention Act']
# crime list:
crimes = ['Rape', 'Kidnapping & Abduction', 'Dowry Deaths','Assault on women with intent to outrage her modesty ','Insult to modesty of women', 'Cruelty by Husband or his Relatives','Importation of Girls from foreign country', 'Immoral Traffic (P) Act','Dowry Prohibition Act', 'Indecent Representation of Women(P) Act','Commission of Sati Prevention Act']


# New df: removing year:
totalc = df.groupby(["State/UT"], as_index=False).agg(crimeDictS)
totalc['Total'] = totalc[crimeDict].sum(axis=1)
print(totalc.columns)
# ==========================  plots =============================================
plottab1 = html.Div(children=[
    # Plot 1:
    html.Div(children=[
        html.H1(style={'textAlign':'center'},children=[
            "Total Crime against Women in India",
        ]),           
        html.P(style={'textAlign':'center'},children=["("+str(minYear)+" - "+str(maxYear)+")"]),
        dcc.Graph(id='totalYear',
              figure={
                  'data':[go.Bar(
                      x=totalc['State/UT'],
                      y=totalc['Total'],
                  )],
                  'layout':go.Layout(title='State wise total crime against women',xaxis={'title':'States/UT'})
              })
    ]),
    # Plot 2:
    html.Div(children=[
        html.Hr(),
        html.H1('Total C.A.W in States per year',style={'textAlign':'center'}),
        html.Div(children=[
           html.Label('Select Year:'),  
           dcc.Dropdown(id='year-picker',options=year_options,value=df['Year'].min(),style={'width':'500px'})
        ]),
        html.Div(children=[
            dcc.Graph(id='perYear')
        ])
    ])
])
plottab2 =  html.Div([
    html.Div(className='row',children=[
        html.Div(className="col",children=[ 
        # Figure 2.1
           html.Div([
               html.Label('Select State/UT:'),
               dcc.Dropdown(id='selectState',options=state_options,value=df['State/UT'][0])
           ]),
           html.Div([
               html.Label('Select Sub-Crime:'),
               dcc.Dropdown(id='selectCrime',options=[{'label':i,'value':i} for i in crimes],value='Rape')
           ]),
         # Figure 2.2 
           html.H2("Forecast:"),
           dcc.Markdown(id='forecast'),
        ]),
        html.Div(className="col",children=[
           dcc.Graph(id="stateCrime"),
        ]),
    ]),
],style={'padding':10})

plottab3 =  html.Div([
    html.Div(className="row", children=[
        html.Div(className="col", children=[
             html.Div([
                html.Label("Select State: "),
                dcc.Dropdown(id='statez',options=state_options,value='Andhra Pradesh'),
                html.Label("Select Crime 1: "),
                dcc.Dropdown(id='crimex',options=[{'label':i,'value':i} for i in crimeDict ],value='Rape'),
                html.Label("Select Crime 2: "),
                dcc.Dropdown(id='crimey',options=[{'label':i,'value':i} for i in crimeDict ],value='Dowry Deaths'),
                html.Hr(),
                html.P(id='corrRes1',children=[
                        "Correlation value: ",
                    html.B(id='corrRes'),
                    html.Br(),
                        "Correlation degree: ",
                    html.B(id='corrType')
                ],style={'width':'30%','display':'inline-block'})
            ]),
        ]),
        html.Div(className='col',children=[
            dcc.Graph(id='corr-graphic')
        ])
    ])
    
  
],style={'padding':10})

plottab4 =  html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])


# ========================== Routes: ============================================
# Nav bar:
navbar = navbar
# home:
home = home
# about
about = about

# ========================== TABS ===============================================

tab1 = dbc.Card(
    [
      plottab1,
    ],
    body=True,
)

tab2 = dbc.Card(
    [
      plottab2,
    ],
    body=True,
)
tab3 = dbc.Card(
    [
      plottab3,
    ],
    body=True,
)
tab4 = dbc.Card(
    [
        dbc.CardTitle("Add DataFrame"),
        html.P('DataFrame columns names must be same as given below:'),
        html.P(['State/UT, Rape, Kidnapping & Abduction, Dowry Deaths,Assault on women with intent to outrage her modesty,Insult to modesty of women', 'Cruelty by Husband or his Relatives,Importation of Girls from foreign country, Immoral Traffic (P) Act,Dowry Prohibition Act', 'Indecent Representation of Women(P) Act, Commission of Sati Prevention Act,Total']),
        plottab4,
        html.P("Restart app after uploading.")
    ],
    body=True,
)

caw = dbc.Tabs(
    [ 
          dbc.Tab(tab1, label="Total C.A.W", className="mt-3"),
          dbc.Tab(tab2, label="States and Sub-Crimes", className="mt-3"),
          dbc.Tab(tab3, label="Crimes Correlation", className="mt-3"),
          dbc.Tab(tab4, label="Add DataFrame", className="mt-3"),

    ]
)



# ========================= page layout =========================================
app.layout = html.Div(
    [        
        dcc.Location(id="url", pathname="/home"),
        navbar,
        html.Div(className="container-fluid", id="content", style={"padding": "20px"}),
      
    ]
)

# ====================== Plotngs ============================================

# TAB 1 : STARTS
@app.callback(Output(component_id='perYear',component_property='figure'),
             [Input(component_id='year-picker',component_property='value')])
def update_figure(selected_year):
    filtered_df = df[df['Year']==selected_year]
    traces = [go.Bar(
        x = filtered_df['State/UT'],
        y = filtered_df['Total Crimes Against Women']
    )]
    return {
        'data':traces,
        'layout':go.Layout(title='Total crime in the year '+str(selected_year),xaxis={'title':'States/UT'})
    }
# TAB 1 ENDS
# TAB 2 : STARTS
@app.callback(Output('stateCrime','figure'),
            [Input('selectState','value'),
            Input('selectCrime','value')])
def state_crime_graph(sstate,scrime):
    filter_state = df[df['State/UT']==sstate]
    traces = [go.Scatter(
        x = filter_state['Year'],
        y = filter_state[scrime],
        name = scrime,
        fill = 'tonexty',
        mode = 'lines+markers'
    )]
    return {
        'data':traces,
        'layout':go.Layout(title ='{} cases in {}'.format(scrime,sstate),
                           xaxis={'title':'Year'},
                           yaxis={'title':'cases of '+scrime},
                           hovermode='closest')
    }

# Forecast:
def pattern(a,b,c):
    if(a == 1):
            if(b == 1):
                if(c==1):return "Higher chances of an increase"
                else:return "Medium chances of an decrease"
            elif(b == 0):
                if(c == 1):return "Medium chances of an increase"      
                else:return "High chances of an decrease"
    elif(a == 0):
            if(b == 0):
                if(c == 0):return "Higher chances of decrease"
                else:return "Lower chances of increase"
            elif(b==1):
                if(c == 0):return "Lower chances of decrease"
                else:return "Higher chances of increase"

@app.callback(Output('forecast','children'),
             [Input('selectState','value'),
              Input('selectCrime','value')])
def forecast_update(sstate,scrime):
    y1 = df['Year'].max()
    y2 = y1-1
    y3 = y2-1
    y4 = y3-1
    x1 = list(df[(df['State/UT']==sstate) & (df['Year']==y1)][scrime])
    x2 = list(df[(df['State/UT']==sstate) & (df['Year']==y2)][scrime])
    x3 = list(df[(df['State/UT']==sstate) & (df['Year']==y3)][scrime])
    x4 = list(df[(df['State/UT']==sstate) & (df['Year']==y4)][scrime])
    if((sstate=='Telangana') & (y1 == 2015)):
         s1=0
         s2=0
         if((x1[0] - x2[0]) > 0):
              s3 = 1
         else:
              s3 = 0
    else:
         if((x3[0] - x4[0]) > 0):
              s1 = 1
         else:
              s1 = 0
         if((x2[0] - x3[0]) > 0):
              s2 = 1
         else:
              s2 = 0
         if((x1[0] - x2[0]) > 0):
              s3 = 1
         else:
              s3 = 0
    res = pattern(s1,s2,s3)
    cast = "> {} has {} in {} in the year {} ,considering constant current policies.".format(sstate,res,scrime,str(y1+1))
    return cast
# TAB 2 ENDS
# TAB 3 STARTS
@app.callback(Output('corr-graphic','figure'),
             [Input('crimex','value'),
              Input('crimey','value'),
              Input('statez','value')])
def update_graph(xaxis_name,yaxis_name,state_name):
    filter_tf = tf[tf['State/UT']==state_name]
    total = filter_tf['Total Crimes Against Women'].sum()
    return {'data':[go.Scatter(x = filter_tf[xaxis_name],
                               y = filter_tf[yaxis_name],
                               text = filter_tf['Year'],
                               mode = 'markers',
                               marker=dict(size=(filter_tf['Total Crimes Against Women']/total)*1000,color=filter_tf['Total Crimes Against Women'],showscale=True)
                               )],
           'layout':go.Layout(title =  'Crime correlation in '+state_name, 
                              xaxis = {'title':xaxis_name},
                              yaxis = {'title':yaxis_name},
                              hovermode='closest')
            }

@app.callback(Output('corrRes','children'),
             [Input('crimex','value'),
              Input('crimey','value'),
              Input('statez','value')])
def corr_result(xvalue,yvalue,zvalue):
    filter_tf = tf[tf['State/UT']==zvalue]
    Correlation = filter_tf[xvalue].corr(filter_tf[yvalue])
    strcorr = str(round(Correlation,1))
    if(strcorr != 'nan'):
        r = strcorr
    else:
        r = '0'
    return r

def corr_check(corr):
    if(corr > 0.0):
        if(corr >= 0.5 and corr < 2.0):
            return 'Highly Positive'
        elif(corr >= 0.3 and corr < 0.5):
            return 'Moderately Positive'
        elif(corr < 0.3):
            return'Low positive'    
    elif(corr == 0):
        return 'No correlation'
    else:
        return 'Negative'

@app.callback(Output('corrType','children'),
             [Input('crimex','value'),
              Input('crimey','value'),
              Input('statez','value')])
def corr_type(xvalue,yvalue,zvalue):
    filter_tf = tf[tf['State/UT']==zvalue]
    Correlation = filter_tf[xvalue].corr(filter_tf[yvalue])
    corri = round(Correlation,1)
    strcorr = str(corri)
    if(strcorr == 'nan'):
        rtype = 'No correlation'
    else:
        rtype = corr_check(corri)
    return rtype

# TAB 3 ENDS
# TAB 4 STARTS:
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            newdf = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            updatedf = df.append(newdf)
            updatedf.to_excel('Data/crime2014.xlsx',index=False)


        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            newdf = pd.read_excel(io.BytesIO(decoded))
            updatedf = df.append(newdf)
            updatedf.to_excel('Data/crime2014.xlsx',index=False)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.H4("Dataframe added!"),
        # dash_table.DataTable(
        #     data=updatedf.to_dict('rows'),
        #     columns=[{'name': i, 'id': i} for i in updatedf.columns]
        # ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



# TAB 4 ENDS:
# ========================== Route Controller ==================================
@app.callback(Output("content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/home":
        return home
    if pathname == "/about":
        return about
    if pathname == "/caw":
        return caw
  
    # if not recognised, return 404 message
    return html.P("Adding Soon")
# ========================== Server =============================================

if __name__ == "__main__":
    app.run_server(debug=True)