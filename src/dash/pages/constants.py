header_height, footer_height = "6rem", "10rem"
sidebar_width, adbar_width = "12rem", "12rem"

TITLE_STYLE = {
    'text-align': 'center'
}

PARAGRAPH_STYLE = {
    'text-align': 'justify'   
}

HEADER_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "right": 0,
    "height": header_height,
    "padding": "2rem 1rem",
    "background-color": "white",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": header_height,
    "left": 0,
    "bottom": footer_height,
    "width": sidebar_width,
    "padding": "1rem 1rem",
    "background-color": "lightgreen",
}

ADBAR_STYLE = {
    "position": "fixed",
    "top": header_height,
    "right": 0,
    "bottom": footer_height,
    "width": adbar_width,
    "padding": "1rem 1rem",
    "background-color": "lightblue",
}

FOOTER_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "left": 0,
    "right": 0,
    "height": footer_height,
    "padding": "1rem 1rem",
    "background-color": "gray",
}

CONTENT_STYLE = {
    "margin-top": header_height,
    "margin-left": sidebar_width,
    "margin-right": adbar_width,
    "margin-bottom": footer_height,
    "padding": "1rem 1rem",
}