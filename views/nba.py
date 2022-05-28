from dash import dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


nba_df = pd.read_csv("dataset/nbaPlayers.csv")


nba_df['season'] = nba_df['season'].astype(str).str[:4]
nba_df = nba_df[~nba_df['country'].isin(['USA', 'Jamaica'])]
int_players_df = nba_df.merge(
    nba_df.groupby(["country", "season"]).size(
    ).reset_index().rename(columns={0: "count"}),
    on=["country", "season"],
).set_index(nba_df.index)


int_players = dcc.Graph(figure=px.area(
    int_players_df,
    title="# of Foreign Players by Country",
    x="season",
    y="count",
    hover_data=["country", "season"],
    color="country",
    pattern_shape="country",
    height=600
))

pts_country = dcc.Graph(figure=px.scatter(
    int_players_df,
    title="Points by Foreign Players",
    x="season",
    y="pts",
    size="count",
    color="country",
    hover_name="player_name",
    log_x=True,
    size_max=60
))

animated_bubble_map = dcc.Graph(figure=px.scatter_geo(
    int_players_df,
    locations="country",
    locationmode="country names",
    color="country",
    hover_name="country",
    size="count",
    animation_frame="season",
    projection="equirectangular",
    height=800,
    size_max=70
))

int_players_tab = dbc.Card(
    dbc.CardBody(
        [int_players]
    ),
    class_name="mt-3",
)

pts_country_tab = dbc.Card(
    dbc.CardBody(
        [pts_country]
    ),
    class_name="mt-3",
)

player_map_tab = dbc.Card(
    dbc.CardBody(
        [animated_bubble_map]
    ),
    class_name="mt-3",
)
