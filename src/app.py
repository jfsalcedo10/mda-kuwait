import dash
from dash import dcc, Output, Input, State, callback
import dash.html as html
import dash_bootstrap_components as dbc
from pages.constants import CONTENT_STYLE, FOOTER_STYLE, MENU_ITEM_STYLE
from pages import home, not_found_404, sentiment, topic_classification, conclusions

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
OBAMA_LOGO = "https://img.icons8.com/color/452/barack-obama.png"

linkedInURL = OBAMA_LOGO
facebookURL = OBAMA_LOGO
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions= True,
    title='Obama\'s speeches - Kuwait group',
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.BOOTSTRAP
    ]
)
server = app.server

offcanvas = html.Div(
    [
        dbc.Button(
            [
                html.I(className="navbar-toggler-icon"),
            ],
            id="open-offcanvas",
            n_clicks=0,
            class_name='tests',
            color='primary'),
        dbc.Offcanvas(
            [
                # html.P('this will have all the menu options for each of the pages'),
                dbc.Row(
                    dbc.Col(
                        dcc.Link('Home', href='/home', style=MENU_ITEM_STYLE),
                    )
                ),
                dbc.Row(dcc.Link('Sentiment Analysis',
                        href='/sentiment', style=MENU_ITEM_STYLE)
                        ),
                dbc.Row(dcc.Link('Topic classification',
                        href='/topic-classification', style=MENU_ITEM_STYLE)
                        ),
                dbc.Row(dcc.Link('Conclusions', href='/conclusions',
                        style=MENU_ITEM_STYLE)
                        )
            ],
            id="offcanvas",
            scrollable=True,
            title="Menu",
            is_open=False,
            close_button=False
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
                        dbc.Col(dbc.NavbarBrand(
                            "Obama Speeches", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                width='auto'
            )
        ]
    ),
    color="dark",
    dark=True,
)

footer = html.Footer(
    [
        html.Div("Modern Data Analytics 2022 - KU Leuven", id='footer-text'),
        html.Div([
            html.P([' Github:'], id='find-me-on'),
            html.A([html.Img(src=app.get_asset_url('favicon.ico'), style={'height': '2rem'})],
               href=linkedInURL),
            html.A([html.Img(src=app.get_asset_url('favicon.ico'), style={'height': '2rem'})],
               href=facebookURL)
        ], id='footer-links',
        ),
    ],
    style=FOOTER_STYLE
)

app.layout = html.Div(
    [
        navbar,
        # conclusions.dashboard,
        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ],
            style=CONTENT_STYLE),
        footer
    ],
    # fluid=True,
    style={
        'minHeight': '100vh',
        'height': '100%',
        'position': 'relative'
    }
)

@callback(
    Output('page-content', 'children'),
    Output('offcanvas', 'is_open'),
    Input('url', 'pathname'),
    Input('open-offcanvas', 'n_clicks'),
    State('offcanvas', 'is_open')
)
def handle_page(pathname, n_clicks, is_open):
    if pathname == '/' or pathname == '/home':
        if n_clicks:
            return home.layout, not is_open
        return home.layout, is_open
    elif pathname == '/sentiment':
        if n_clicks:
            return sentiment.layout, not is_open
        return sentiment.layout, is_open
    elif pathname == '/topic-classification':
        if n_clicks:
            return topic_classification.layout, not is_open
        return topic_classification.layout, is_open
    elif pathname == '/conclusions':
        if n_clicks:
            return conclusions.layout, not is_open
        return conclusions.layout, is_open
    # In case an unknown route is specified
    return not_found_404.layout, is_open


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
