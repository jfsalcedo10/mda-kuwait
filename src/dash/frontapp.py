import dash
from dash import dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
from pages import home, not_found_404, sentiment, topic_classification, conclusions

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
OBAMA_LOGO = "https://img.icons8.com/color/452/barack-obama.png"

app = dash.Dash(
    __name__, title='Obama\'s speeches - Kuwait group', external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)
server = app.server

offcanvas = html.Div(
    [
        dbc.Button(
            [
                html.I(className="bi bi-list me-2")
            ], 
            id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            [
                # html.P('this will have all the menu options for each of the pages'),
                dbc.Row(dcc.Link('Home', href='/home')),
                dbc.Row(dcc.Link('Sentiment Analysis', href='/sentiment')),
                dbc.Row(dcc.Link('Topic classification', href='/topic-classification')),
                dbc.Row(dcc.Link('Conclusions', href='/conclusions'))
            ],
            id="offcanvas",
            scrollable = True,
            title="Obama speeches",
            is_open=False,
        ),
    ],
    className="my-3"
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Col(offcanvas),
            dbc.Col(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=OBAMA_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Obama Speeches", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                width= 'auto'
            )
        ]
    ),
    color="dark",
    dark=True,
)

app.layout = dbc.Container(
    [
        navbar, 
        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ])
    ],
    fluid=True,
    style={'height': '100vh'}
)

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    elif pathname == '/sentiment':
        return sentiment.layout
    elif pathname == '/topic-classification':
        return topic_classification.layout
    elif pathname == '/conclusions':
        return conclusions.layout
    else:
        return not_found_404.layout

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)