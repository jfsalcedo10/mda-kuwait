from dash import dcc, Input, Output, callback
import dash.html as html
import dash_bootstrap_components as dbc
from pages.constants import TITLE_STYLE, PARAGRAPH_STYLE, IMG_STYLE
from utils.topic_crud import TopicCRUD

import plotly.express as px

df = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

topic_plotter = TopicCRUD()

item_1 = [
    "This is the content of the first section",
    dcc.Graph(figure=fig)
]

topic_2_accordion = [
    'This is the topics for the accordion',
    html.Div([
        dcc.Slider(min=1, max=25, step=1,
                   id='second-topic-slider',
                   value=10,
                   tooltip={"placement": "bottom", "always_visible": True}
                   )]),
    dcc.Graph(id='second-topic-figure')
]

topics_by_city_accordion = [
    'This is the topics for the accordion',
    dcc.Graph(id='topic-cities-figure')
]

topic_presence_accordion = [
    'This is the topics for the accordion',
    dcc.Graph(id='topic-presence-figure')
]

topic_word_relevance = [
    'This is the topics for the accordion',
    dcc.Input(id='word-presence-input'),
    dcc.Graph(id='topic-words-figure')
]

topic_speech_topics = [
    'This is the topics for the accordion',
    dcc.Dropdown(),
    dcc.Graph(id='topic-speeches-figure')
]
accordion = dbc.Accordion(
    [
        dbc.AccordionItem(
            item_1, title="Topic - Key words"
        ),
        dbc.AccordionItem(
            topic_2_accordion, title="Secondary topic"
        ),
        dbc.AccordionItem(
            topics_by_city_accordion, title="Topic location"
        ),
        dbc.AccordionItem(
            topic_word_relevance, title="Word relevance"
        ),
        dbc.AccordionItem(
            topic_speech_topics, title="Important topics by speach"
        ),
    ],
    start_collapsed=True,
    always_open=True,
    flush=True
)


body = dbc.Container([
    # Title page
    dbc.Row(
        [
            html.H1(
                'Conclusions', style=TITLE_STYLE)
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
        accordion
    )
], style={'height': '100%'})

layout = html.Div([
    body
])
