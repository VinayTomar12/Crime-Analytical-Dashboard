import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input,Output,State
from datetime import datetime
import pandas as pd 
import plotly.graph_objs as go 
app = dash.Dash()

df = pd.read_csv('crimeAgainstWomeninIndia.csv')
print(df.head())
state_options = []
for state in df['State/UT'].unique():
    state_options.append({'label':str(state),'value':state})

crimes = ['Rape', 'Kidnapping & Abduction', 'Dowry Deaths','Assault on women with intent to outrage her modesty ','Insult to modesty of women', 'Cruelty by Husband or his Relatives','Importation of Girls from foreign country', 'Immoral Traffic (P) Act','Dowry Prohibition Act', 'Indecent Representation of Women(P) Act','Commission of Sati Prevention Act']

app.layout = html.Div([
    # Figure 2.1
    html.Div([
        html.Label('Select State/UT:'),
        dcc.Dropdown(id='selectState',options=state_options,value=df['State/UT'][0])
    ],style={'width':'48%','display':'inline-block'}),
    html.Div([
        html.Label('Select Sub-Crime:'),
        dcc.Dropdown(id='selectCrime',options=[{'label':i,'value':i} for i in crimes],value='Rape')
    ],style={'width':'48%','display':'inline-block'}),
    dcc.Graph(id="stateCrime"),
    
    # Figure 2.2 
    html.H2("Forecast:"),
    dcc.Markdown(id='forecast'),
    html.Hr(),
    html.Div([
        html.Div([
              html.H1('Compare Sub-crimes:'),
        ],style={'width':'48%','display':'inline-block'}),
        html.Div([
              html.H1('Compare Sub-crimes:'),
        ],style={'width':'48%','display':'inline-block'}),
    ])
],style={'padding':10})


# Figure 1
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
    cast = "> **{}** has {} in **{}** in the year **{}** ,considering constant current policies.".format(sstate,res,scrime,str(y1+1))
    return cast




if __name__ == '__main__':
    app.run_server(debug=True)