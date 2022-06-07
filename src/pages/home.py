from dash import dcc, Input, Output, callback
import dash.html as html
import dash_bootstrap_components as dbc
from pages.constants import TITLE_STYLE, PARAGRAPH_STYLE, IMG_STYLE
from pages.sentiment import sentiment_plotter
import plotly.express as px

from utils.utils import UtilsCRUD

# sentiment_plotter = SentimentCRUD()

df = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

utils_crud = UtilsCRUD()

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
    html.Br(),
    # Contains
    dbc.Row(
        [
            html.P('''
            Barack Obama won the US presidency in November 2008 and November 2012 and was in office from 2009 to 2017. 
            Team Kuwait explore Obama's speeches during his presidential terms and election periods to find the variables that explain his speeches. 
            For this, we mainly focus on the topic and sentiment parts of the speeches and see the variables for these two aspects. 
            This app collects the findings from our analysis using NLP techniques on Python and Neo4j as well as some statistical tools such as mixed models. 
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
            dcc.Graph(figure=sentiment_plotter.plot_sentiment_location(
                stanza=False, color='country'))
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
            dcc.Graph(figure=utils_crud.plot_popularity())
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
            dcc.Markdown('''

**Research Theme: What are the variables affecting Obama's speeches?**

With this research theme, our study aims to answer the following research questions regarding Obama's speeches delivered during his mandate.

1.  What are the topics and sentiments of the speeches?

2.  What affects the topics and the sentiments of the speeches?

    -   Location, Time, Obama's popularity, Gun Deaths, Financial and Job market Situation


3.  What is the relation between sentiment & topic for the speeches?

'''
                   )
        ],
        justify='center',
        align='center',
    )
], style={'height': '100%'})

layout = html.Div([
    body
])
