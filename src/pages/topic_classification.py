from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages.constants import TITLE_STYLE, PARAGRAPH_STYLE
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

topic_presence_accordion=[
    'This is the topics for the accordion',
    dcc.Graph(id='topic-presence-figure')
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
            "This is the content of the third section", title="Word relevance"
        ),
        dbc.AccordionItem(
            "This is the content of the third section", title="Important topics by speach"
        ),
        # dbc.AccordionItem(
        #     "This is the content of the third section", title="Item 6"
        # ),
        # dbc.AccordionItem(
        #     "This is the content of the third section", title="Item 7"
        # ),
        # dbc.AccordionItem(
        #     "This is the content of the third section", title="Item 8"
        # ),
    ],
    start_collapsed=True,
    always_open= True,
    flush= True
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
    html.Br(),
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