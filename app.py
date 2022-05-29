from dash import Dash, html
from views import hurricane, nba
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Sample Graphs Built with Dash & Plotly Express",
                    className="display-3 text-light"),
            html.P(
                "No Javascript needed, everything on this screen is written in Python with Dash framework and Plotly Express.",
                className="lead text-light",
            ),
            html.Hr(className="my-2 bg-white"),
            html.P(
                "Dash uses Plotly for graphing capabilities. Click the link below to see documentations from Dash.", className="text-light"
            ),
            html.P(
                dbc.Button("Learn more", color="info", external_link=True, href="https://dash.plotly.com"), className="lead"
            ),
        ],
        fluid=True,
        class_name="py-3",
    ),
    className="p-2 bg-primary rounded-3",
    style={"margin-top": "10px"}
)

tabs = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(hurricane.atlantic_hurricanes_tab,
                            label="Atlantic Hurricanes"),
                    dbc.Tab(nba.int_players_tab,
                            label="International NBA Players"),
                    dbc.Tab(nba.pts_country_tab,
                            label="Points by International Players"),
                    dbc.Tab(nba.player_map_tab,
                            label="Map of International Players"),
                    dbc.Tab(nba.points_draft_tab,
                            label="Points by Draft Round")

                ]
            )
        )
    ],
    style={"margin-top": "10px", "margin-bottom": "20px"}
)

app.layout = dbc.Container([jumbotron, tabs])

# Run app
if __name__ == '__main__':
    # app.run_server(port=8051)
    app.run_server(debug=True, port=8051)
