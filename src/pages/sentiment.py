from dash import dcc,html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages.constants import TITLE_STYLE, PARAGRAPH_STYLE
from utils.sentiment_crud import SentimentCRUD

sentiment_plotter = SentimentCRUD()

acc_sentiment_time = [
    html.P('Sentiment over time'),
    dcc.Graph(figure= sentiment_plotter.plot_sentiment_over_time())
]

accordion = dbc.Accordion(
        [
            dbc.AccordionItem(
                acc_sentiment_time, title="Sentiment over time"
            ),
            dbc.AccordionItem(
                "This is the content of the second section", title="Sentiment per location"
            ),
            dbc.AccordionItem(
                "This is the content of the third section", title="Popularity tracker"
            ),
        ],
        start_collapsed=True,
        flush= True
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