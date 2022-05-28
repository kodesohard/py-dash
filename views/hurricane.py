from dash import dcc, Input, Output, callback
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

hurr_df = pd.read_csv("dataset/atlanticHurricanes.csv")

# format various columns in csv data
hurr_df['Date'] = hurr_df['Date'].astype(str).str[:4].astype(int)
hurr_df['Name'] = hurr_df['Name'].str.strip()
hurr_df["Latitude"] = np.where(hurr_df["Latitude"].str.endswith(
    "N"), hurr_df["Latitude"].str[:-1].astype(float), -hurr_df["Latitude"].str[:-1].astype(float))
hurr_df["Longitude"] = np.where(hurr_df["Longitude"].str.endswith(
    "W"), -hurr_df["Longitude"].str[:-1].astype(float), hurr_df["Longitude"].str[:-1].astype(float))


atlantic_hurricanes = dcc.Graph(figure={})
slider = dcc.RangeSlider(2000, 2015, 1,
                         value=[2003, 2008],
                         marks={2000: '2000', 2005: '2005',
                                2010: '2010', 2015: '2015'},
                         tooltip={"placement": "bottom",
                                  "always_visible": True},
                         id='range-slider')


@callback(
    Output(atlantic_hurricanes, 'figure'),
    [Input('range-slider', 'value')])
def update_hurr_graph(yearRange):
    start, end = yearRange
    filtered = hurr_df[hurr_df['Date'].between(start, end)]

    fig = px.density_mapbox(
        filtered,
        title='Year(s) {} - {}'.format(start, end),
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


atlantic_hurricanes_tab = dbc.Card(
    dbc.CardBody(
        [atlantic_hurricanes, slider]
    ), class_name="mt-3",
)
