import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input,Output,State
from datetime import datetime
import pandas as pd 
import plotly.graph_objs as go 

app = dash.Dash()
df = pd.read_csv('crimeAgainstWomeninIndia.csv')
# print(df.head())

# Year list:
year_options = []
for year in df['Year'].unique():
    year_options.append({'label':str(year),'value':year})

#Crime head dictionary-LIST:
#With Sum aggr:
crimeDictS = {'Rape':sum, 'Kidnapping & Abduction':sum,'Dowry Deaths':sum,'Assault on women with intent to outrage her modesty ':sum,'Insult to modesty of women':sum,'Cruelty by Husband or his Relatives':sum,'Importation of Girls from foreign country':sum,'Immoral Traffic (P) Act':sum,'Dowry Prohibition Act':sum,'Indecent Representation of Women(P) Act':sum,'Commission of Sati Prevention Act':sum}
#Without aggr list:
crimeDict = ['Rape', 'Kidnapping & Abduction', 'Dowry Deaths','Assault on women with intent to outrage her modesty ','Insult to modesty of women', 'Cruelty by Husband or his Relatives','Importation of Girls from foreign country', 'Immoral Traffic (P) Act','Dowry Prohibition Act', 'Indecent Representation of Women(P) Act','Commission of Sati Prevention Act']


# New df: removing year:
totalc = df.groupby(["State/UT"], as_index=False).agg(crimeDictS)
totalc['Total'] = totalc[crimeDict].sum(axis=1)
print(totalc.columns)

app.layout = html.Div(children=[
    # Plot 1:
    html.Div(children=[
        html.H1('Total Crime against Women in India',style={'textAlign':'center'}),
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



















if __name__ == '__main__':
    app.run_server(debug=True)