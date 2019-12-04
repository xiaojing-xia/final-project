# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px


file1 = "Seattle_Real_Time_Fire_911_Calls.csv"
data = pd.read_csv(file1, nrows=50000)
data['Year'] = pd.DatetimeIndex(data['Datetime']).year
year2019 = data['Year'] == 2019
test=data[year2019]
test['Month'] = pd.DatetimeIndex(test['Datetime']).month
available_indicators = test['Year'].unique()

medic = data['Type'] == "Medic Response"
car_fire = data['Type'] == "Car Fire"
brush_fire = data['Type'] == "Brush Fire"
auto_fire = data['Type'] == "Fire in Single Family Res"
#test=data[auto_fire | car_fire | brush_fire]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='map-graph'),
    html.Label('Year'),
    dcc.Dropdown(
                id='year-option',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=2019
            ),
    html.Label('Call Type'),
    dcc.RadioItems(
        id = 'type-option',
        options=[
            {'label': 'Medic Response', 'value': 'Medic Response'},
            {'label': 'MVI - Motor Vehicle Incident', 'value': 'MVI - Motor Vehicle Incident'},
            {'label': 'Fire in Single Family Res', 'value': 'Fire in Single Family Res'},
            {'label': 'Auto Fire Alarm', 'value': 'Auto Fire Alarm'},
            {'label': 'Aid Response', 'value': 'Aid Response'}
        ],
        value='Medic Response'
    ),
    html.Label('Month'),
    dcc.Slider(
        id = 'month-slider',
        min = test['Month'].min(),
        max = test['Month'].max(),
        value = test['Month'].min(),
        marks = {str(Month): str(Month) for Month in test['Month'].unique()},
        step=None),
],style={'columnCount': 2})
     

layout_map = dict(
    autosize=True,
    height=1000,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='911 Calls in Seattle',
    mapbox=dict(
        style = "open-street-map",
        center=dict(
            lon=-122.3,
            lat=47.5
        ),
        zoom=10,
    )
)

# functions
def gen_map(map_data):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(map_data['Latitude']),
                "lon": list(map_data['Longitude']),
                "mode": "markers",
                "name": list(map_data['Type']),
                "marker": {
                    "size": 6,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
    }



     
@app.callback(
    Output('map-graph', 'figure'),
    [Input('year-option', 'value'),
     Input('type-option', 'value'),
     Input('month-slider', 'value')])
          
def update_figure(year,selected_type,month_value):
    filtered_df = test[test.Type == selected_type]
    filtered_df = filtered_df[test.Month == month_value]

    return gen_map(filtered_df)

if __name__ == '__main__':
    app.run_server(debug=True)


