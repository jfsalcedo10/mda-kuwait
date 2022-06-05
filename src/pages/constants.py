header_height, footer_height = "6rem", "3.5rem"
sidebar_width, adbar_width = "12rem", "12rem"

TITLE_STYLE = {
    'textAlign': 'center'
}

PARAGRAPH_STYLE = {
    'textAlign': 'justify'   
}

MENU_ITEM_STYLE = {
    'textDecoration': 'none',
    'size': '20'
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

FOOTER_STYLE = {
    "position": "absolute",
    "display": "flex",
    "justifyContent": "spaceBetween",
    "alignItems": "center",
    "bottom": "0",
    "width": "100%",
    "height": footer_height,
    "color": "white",
    "backgroundColor": "var(--bs-secondary)",
}


IMG_STYLE = {
    'display': 'block',
    'margin-left': 'auto',
    'margin-right': 'auto',
    'width': '60%',
}

CONTENT_STYLE = {
    "paddingBottom": footer_height,
}