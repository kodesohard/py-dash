from dash import Dash, dcc, Input, Output

import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

dataFrame = pd.read_csv(
    "/Users/dehang/hack/py-dash/dataset/atlanticHurricanes.csv")
print(dataFrame.head(), dataFrame['Date'])

# format various columns in csv data
dataFrame['Date'] = dataFrame['Date'].astype(str).str[:4].astype(int)

dataFrame['Name'] = dataFrame['Name'].str.strip()

dataFrame["Latitude"] = np.where(dataFrame["Latitude"].str.endswith(
    "N"), dataFrame["Latitude"].str[:-1].astype(float), -dataFrame["Latitude"].str[:-1].astype(float))

dataFrame["Longitude"] = np.where(dataFrame["Longitude"].str.endswith(
    "W"), -dataFrame["Longitude"].str[:-1].astype(float), dataFrame["Longitude"].str[:-1].astype(float))
print(dataFrame.head())

# Dash Components
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
title = dcc.Markdown(children="# Sample Graphs Built with Python Dash")
atlantic_hurricanes = dcc.Graph(figure={})
slider = dcc.RangeSlider(2000, 2015, 1,
                         value=[2003, 2008],
                         marks={2000: '2000', 2005: '2005',
                                2010: '2010', 2015: '2015'},
                         tooltip={"placement": "bottom",
                                  "always_visible": True},
                         id='range-slider')


@app.callback(
    Output(atlantic_hurricanes, 'figure'),
    [Input('range-slider', 'value')])
def update_graph(yearRange):
    start, end = yearRange
    filtered = dataFrame[dataFrame['Date'].between(start, end)]

    fig = px.density_mapbox(
        filtered,
        title='Atlantic Hurricanes ({}-{})'.format(start, end),
        lat='Latitude',
        lon='Longitude',
        z='Maximum Wind',
        labels={'Maximum Wind': 'Max Wind Speed (KN)'},
        hover_data=['Latitude', 'Longitude', 'Maximum Wind', 'Date', 'Name'],
        radius=10,
        custom_data=['Date'],
        center=dict(lat=18, lon=-50),
        zoom=3,
        mapbox_style="stamen-terrain",
        height=800)

    return fig


app.layout = dbc.Container([title, atlantic_hurricanes, slider])

# Run app
if __name__ == '__main__':
    # app.run_server(port=8051)
    app.run_server(debug=True, port=8051)
