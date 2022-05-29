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
    title="# of International NBA Players by Country",
    x="season",
    y="count",
    hover_data=["country", "season"],
    color="country",
    pattern_shape="country",
    height=800
))

pts_country = dcc.Graph(figure=px.scatter(
    int_players_df,
    title="Points by International NBA Players",
    x="season",
    y="pts",
    size="count",
    color="country",
    hover_name="player_name",
    log_x=True,
    size_max=60,
    height=800
))

animated_bubble_map = dcc.Graph(figure=px.scatter_geo(
    int_players_df,
    title="Animated Timeline of International NBA Players",
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

points_draft = dcc.Graph(figure=px.scatter(
    nba_df,
    x="player_name",
    y="pts",
    facet_col="draft_round",
    hover_name="player_name",
    hover_data=["pts", "reb", "ast", "net_rating", "draft_number"],
    height=700
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

points_draft_tab = dbc.Card(
    dbc.CardBody(
        [points_draft]
    ),
    class_name="mt-3",
)
