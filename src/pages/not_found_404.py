from dash import html
import dash_bootstrap_components as dbc

layout = html.Div(
    dbc.Container(
        [
            html.H1("404 - Not Found", className="text-danger"),
            html.Hr(className="my-2"),
            html.P(
                "The pathname {pathname)} was not recognised..."
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)