from dash import dcc,html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages.constants import TITLE_STYLE, PARAGRAPH_STYLE
from utils.sentiment_crud import SentimentCRUD

sentiment_plotter = SentimentCRUD()

acc_sentiment_time = [
    html.P('Sentiment over time'),
    dcc.Graph(figure= sentiment_plotter.plot_sentiment_over_time())
]

acc_sentiment_location = [
    html.P('Sentiment and location'),
    dcc.Graph(figure= sentiment_plotter.plot_sentiment_location())
]

acc_popularity_tracker = [
    html.P('Sentiment and location'),
    dcc.Graph(figure= sentiment_plotter.plot_sentiment_popularity_tracker()),
    html.P('Gun deaths vs sentiment across time'),
    dcc.Graph(figure= sentiment_plotter.plot_gun_popularity_tracker())
]

accordion = dbc.Accordion(
        [
            dbc.AccordionItem(
                acc_sentiment_time, title="Sentiment over time"
            ),
            dbc.AccordionItem(
                acc_sentiment_location, title="Sentiment per location"
            ),
            dbc.AccordionItem(
                acc_popularity_tracker, title="Popularity tracker"
            ),
        ],
        start_collapsed=True,
        flush= True,
        always_open= True
    )

body = dbc.Container([
    # Title page
    dbc.Row(
        [
            html.H1('Sentiment analysis of the speeches', style= TITLE_STYLE)
        ],
        justify='center',
        align='center',
    ),
    dbc.Row(
        [
            html.P('''Sentimental analysis was carried out with three different NLP techniques: 
            TextBlob, Stanza and Vader. A fourth one, not hosted by python packages, was also used:
            AWS Sentimental analysis. This section represents the different scores of the three main 
            techniques used. We also present the areas where the different speeches were pronounced as
            well as some graphs showing the links between some external variables and the sentiments of the speeches.''',
            style=PARAGRAPH_STYLE
            )
        ]
    ),
    # Image of obama,
    dbc.Row(
        [
            accordion
        ],
        align='center'
    ),
],
style={'height': '100%'}
)

layout = html.Div([
    body
])