from dash import dcc,html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages.constants import TITLE_STYLE, PARAGRAPH_STYLE

accordion = dbc.Accordion(
        [
            dbc.AccordionItem(
                "This is the content of the first section", title="Item 1"
            ),
            dbc.AccordionItem(
                "This is the content of the second section", title="Item 2"
            ),
            dbc.AccordionItem(
                "This is the content of the third section", title="Item 3"
            ),
        ],
        start_collapsed=True,
    )

body = dbc.Container([
    # Title page
    dbc.Row(
        [
            html.H1('Topic classification of each speech', style= TITLE_STYLE)
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