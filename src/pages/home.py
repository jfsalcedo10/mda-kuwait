from dash import dcc, Input, Output, callback
import dash.html as html
import dash_bootstrap_components as dbc
from pages.constants import TITLE_STYLE, PARAGRAPH_STYLE, IMG_STYLE

import plotly.express as px

df = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")


item_1 = [
    "This is the content of the first section",
    dcc.Graph(figure=fig)
]

body = dbc.Container([
    # Title page
    dbc.Row(
        [
            html.H1(
                'Obama\'s Rise and Fall: A text analysis of his speeches', style=TITLE_STYLE)
        ],
        justify='center',
        align='center',
    ),
    # Image of obama,
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Img(
                        src='assets/bobama-front.jpg',
                        style=IMG_STYLE
                    ),
                ],
                align='center'
            )
        ],
        align='center'
    ),
    # Contains
    dbc.Row(
        [
            html.P('''
            Barack Obama was the U.S President for two twerms: 2008-2012 and re-elected on 2012-2016.
            During his administration, the mandatary gave many speeches regarding the country situation
            and whatnot. Also, [INSERT HERE GLOBAL TOPICS]. This app then collects the findings from the
            Kuwait group for his speeches, by using NLP techniques on Python and Neo4j. 
            ''',
                   style=PARAGRAPH_STYLE)
        ],
        justify='center',
        align='center',
    ),
    dbc.Row(
        [
            html.H2('Speeches location')
        ],
        justify='center',
        align='center',
    ),
    dbc.Row(
        [
            dcc.Graph(figure= fig)
        ],
        justify='center',
        align='center',
    ),
    dbc.Row(
        [
            html.H2('Obama\'s popularity')
        ],
        justify='center',
        align='center',
    ),
    dbc.Row(
        [
            dcc.Graph(figure= fig)
        ],
        justify='center',
        align='center',
    ),
    dbc.Row(
        [
            html.H2('Study objectives')
        ],
        justify='center',
        align='center',
    ),
    dbc.Row(
        [
            'Here go the objectives'
        ],
        justify='center',
        align='center',
    )
], style={'height': '100%'})

layout = html.Div([
    body
])
