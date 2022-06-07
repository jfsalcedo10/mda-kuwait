from dash import Input, Output, callback
from dash import dcc
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
                        src='assets/obama-farewell.jpg',
                        style=IMG_STYLE
                    ),
                    dcc.Markdown('''_President Obama Caps Long Goodbye With Farewell Speech
Copyright: Copyright 2017 The Associated Press. All rights reserved._
                    ''', style=TITLE_STYLE)
                ],
                align='center',
            )
        ],
        align='center'
    ),
    # Contains
    dbc.Row(
        [
            dcc.Markdown('''
What are the variables of Obama\'s speeches? Our answers based on the analyses are:

- Obama tends to be more negative when he talks about foreign conflict and terrorism, gun violence, the economy, immigration, and civil rights.
- Obama tends to be more positive when he talks about elections, education, faith and family.
- The overall mean for the sentiment is more positive (0.1).
- All topics have a positive sentiment, the &quot;more negative&quot; topics are below the overall average, but their mean sentiment score is positive.
- Obama&#39;s job (dis)approval tracker does not have an impact on the sentiment of his speeches. But more dynamics in the tracker coincides with his 2nd presidential term (2013-2017).
- Gun deaths by assault has a negative effect on the sentiment of his speeches. More deaths associate with more negative sentiments in the speeches.
- The positively improving people&#39;s perception of the financial situation and job market in the US coincides with Obama&#39;s increasingly positive speeches related to economy.
            '''),
        ],
        justify='center',
        align='center',
    ),
    # dbc.Row(
    #     accordion
    # )
], style={'height': '100%'})

layout = html.Div([
    body
])
