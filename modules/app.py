from dash import dcc, html


def declare_export_block(walls_type, style_block):
    font_color = style_block["font_color"]
    # setting export block
    if walls_type:
        export_block = html.Div(
            children=[
                html.Label(
                    "Choose export method",
                    style={"padding": 10, "color": font_color},
                ),
                html.Br(),
                dcc.RadioItems(
                    ["lines representation"], "lines representation", id="radio-export"
                ),
                html.Button(
                    "Export",
                    id="export_button",
                    n_clicks=0,
                    style={"color": font_color},
                ),
                dcc.Download(id="download_repr"),
            ]
        )
    else:
        export_block = html.Div(
            children=[
                html.Label(
                    "Choose export method",
                    style={"padding": 10, "color": font_color},
                ),
                html.Br(),
                dcc.RadioItems(
                    [
                        "lines representation",
                        "hashtag representation",
                        "bitmap representation",
                    ],
                    "lines representation",
                    id="radio-export",
                ),
                html.Button(
                    "Export",
                    id="export_button",
                    n_clicks=0,
                    style={"color": font_color},
                ),
                dcc.Download(id="download_repr"),
            ]
        )
    return export_block


def declare_layout(style_dict, blocks):
    font_color = style_dict["font_color"]
    algorithm = style_dict["algorithm"]
    export_block = blocks[0]
    frames_count = style_dict["frames_count"]
    background_color = style_dict["background_color"]
    m, n = style_dict["m"], style_dict["n"]

    layout = html.Div(
        children=[
            html.H1("Demo (version 0.4)", style={"color": font_color}),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Br(),
                            html.Label(
                                f"Algorithm: {algorithm}",
                                style={"padding": 10, "color": font_color},
                            ),
                            html.Br(),
                            export_block,
                        ],
                        style={"padding": 10, "flex": 1, "color": font_color},
                    ),
                    html.Div(
                        children=[
                            html.Label("Slider", style={"color": font_color}),
                            dcc.Slider(
                                id="slider",
                                min=1,
                                max=frames_count,
                                marks={i: str(i) for i in range(1, frames_count + 1)},
                                value=1,
                                step=1,
                            ),
                            html.Br(),
                            html.Button(
                                "Run",
                                id="run-button",
                                n_clicks=0,
                                style={"color": font_color},
                            ),
                        ],
                        style={"padding": 10, "flex": 1},
                    ),
                ],
                style={"display": "flex", "flex-direction": "row"},
            ),
            html.Div(
                children=[
                    # dcc.Store stores the intermediate value
                    dcc.Store(id="intermediate-value"),
                    dcc.Graph(
                        id="ex_graph",
                        style={"height": "700px", "width": f"{700*n/m}px"},
                    ),
                ],
                style={"display": "table", "margin": "0 auto"},
            ),  # (2)
        ],
        style={
            "display": "flex",
            "flex-direction": "column",
            "backgroundColor": background_color,
        },
    )
    return layout
