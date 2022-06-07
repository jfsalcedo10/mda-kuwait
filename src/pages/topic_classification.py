from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages.constants import TITLE_STYLE, PARAGRAPH_STYLE
from utils.topic_crud import TopicCRUD

topic_plotter = TopicCRUD()

topic_2_accordion = [
    dcc.Graph(id='second-topic-figure')
]

topics_by_city_accordion = [
    'This is the topics for the accordion',
    dcc.Graph(id='topic-cities-figure')
]

topic_keywords_accordion = [
    'Number of keywords',
    html.Div([
        dcc.Slider(min=5, max=25, step=5,
                   id='keywords-topic-slider',
                   value=10,
                   tooltip={"placement": "bottom", "always_visible": True}
                   )]),
    dcc.Graph(id='topic-keywords-figure')
]

topic_word_relevance = [
    'This is the topics for the accordion',
    dbc.Input(
        placeholder='Write a word (i.e. \'gun\')',
        id='word-presence-input',
        type='text'),
    dcc.Graph(id='topic-words-figure')
]

topic_speech_topics = [
    'Number of topics',
    html.Div([
        dcc.Slider(min=1, max=10, step=1,
                   id='speech-topic-slider',
                   value=5,
                   tooltip={"placement": "bottom", "always_visible": True}
                   )]),
    dbc.Select(
        id='speech-select',
        options= topic_plotter.get_speech_titles(),
        value='Cairo_University'
    ),
    dcc.Graph(id='topic-speeches-figure')
]

accordion = dbc.Accordion(
    [
        dbc.AccordionItem(
            topic_keywords_accordion, title="Topic - Key words"
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
        # dbc.AccordionItem(
        #     "This is the content of the third section", title="Item 6"
        # ),
    ],
    start_collapsed=True,
    always_open=True,
    flush=True
)

body = dbc.Container([
    # Title page
    dbc.Row(
        [
            html.H1('Topic classification', style=TITLE_STYLE)
        ],
        justify='center',
        align='center',
    ),
    dbc.Row(
        [
            dcc.Graph(figure=topic_plotter.get_neo4j_graph())
        ],
        justify='center',
        align='center'
    ),
    dbc.Row(
        [
            html.P([
                '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''
            ]),
        ],
        justify='center',
        align='center'
    ),
    html.Br(),
    # Image of obama,
    dbc.Row(
        [
            'Select a topic to analyze:',
            html.Div([
                dcc.Slider(min=1, max=25, step=1,
                        id='second-topic-slider',
                        value=10,
                        tooltip={"placement": "bottom", "always_visible": True}
                        )]),
        ]
    ),
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

# Callback functions


@callback(
    Output('second-topic-figure', 'figure'),
    Input('second-topic-slider', 'value'))
def update_graph_topic_2(sliderValue):
    fig = topic_plotter.get_second_topic(sliderValue)
    return fig


@callback(
    Output('topic-cities-figure', 'figure'),
    Input('second-topic-slider', 'value'))
def update_topic_location(sliderValue):
    fig = topic_plotter.get_topic_cities(sliderValue, False)
    return fig

@callback(
    Output('topic-words-figure', 'figure'),
    Input('word-presence-input', 'value'))
def update_topic_presence(word_input):
    if word_input == None or word_input == '':
        word_input = 'gun'
    fig = topic_plotter.get_token_influence(word_input)
    return fig

@callback(
    Output('topic-keywords-figure', 'figure'),
    Input('second-topic-slider', 'value'),
    Input('keywords-topic-slider', 'value'))
def update_topic_keywords(slider_value, no_keywords):
    fig = topic_plotter.get_top_tokens_per_topic(slider_value, no_keywords)
    return fig

@callback(
    Output('topic-speeches-figure', 'figure'),
    Input('speech-select', 'value'),
    Input('speech-topic-slider', 'value'))
def update_topic_speech(selected_value, no_topics):
    fig = topic_plotter.get_speech_topics(selected_value, no_topics)
    return fig