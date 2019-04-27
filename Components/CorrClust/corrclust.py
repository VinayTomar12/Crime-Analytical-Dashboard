import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input,Output,State
from datetime import datetime
import pandas as pd 
import plotly.graph_objs as go 
import plotly.offline as py
import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

app = dash.Dash()
df = pd.read_csv('crimeAgainstWomeninIndia.csv')
li = df['Assault on women with intent to outrage her modesty '].values.tolist()
trace = go.Heatmap(z= li,
                   y=df['Year'],
                   x=df['State/UT'])
data=[trace]
layout = go.Layout(title='title')
fig = go.Figure(data=data,layout=layout)
py.plot(fig)


if __name__ == '__main__':
    app.run_server(debug=True)