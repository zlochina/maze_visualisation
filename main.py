import os
from json import load

from dash import Dash, Input, Output, State, dcc, html
from PIL import Image

import config
import constants
from modules.Maze import Maze
# importing from project modules
from modules.maze_gen import (bitmap_converter, primitive_converter,
                              reverse_bitmap_converter,
                              reverse_complex_converter,
                              reverse_primitive_converter)

# from time import sleep
"""
Demo version 0.4
"""

""" INITIALISING """

# Reading files

# importing style specs for maze page
with open(config.path_to_specs, "r") as r:
    layout = load(r)

# setting layout specs
background_color = layout["background_color"]
font_color = layout["font_color"]

# importing style specs for maze objects
with open(config.path_maze_specs, "r") as r:
    maze_style = load(r)

# importing processed data from json
with open(config.path_to_processed_data, "r") as r:
    processed_data = load(r)

configuration = processed_data["config"]
frames_data = processed_data["iterations"]
filename = configuration["file"]
represantation_method = configuration["map"]

frames_count = len(frames_data)
walls_type = 1 if configuration["env_type"] == "walls_between_tiles" else 0
# walls_type = 1
algorithm = "Astar"  # TODO change it

# importing maze map
if filename not in os.listdir(config.path_to_maps_dir):
    print("ERROR: failed to navigate to map")
    os._exit(constants.error_enum["FAILED_PATH_TO_DATA"])

if represantation_method == constants.mappings_tuple[2]:
    maze_text = Image.open(config.path_to_maps_dir + filename)
else:
    with open(config.path_to_maps_dir + filename, "r") as r:
        maze_text = r.read()[:-1]

# size of maze declaration

animation_on = False

if represantation_method == constants.mappings_tuple[2]:
    return_tuple = bitmap_converter(maze_text)
    array_of_walls = return_tuple[0]
    start_point = return_tuple[1][0]
    end_point = return_tuple[1][1]
else:
    array_of_walls = primitive_converter(maze_text, walls_type)
m = len(array_of_walls)
n = len(array_of_walls[0])

if walls_type:
    m -= 1
    n -= 1

# output to cmd
if config.debugging:
    print("\n~~Updated~~\n")

# maze declaration
maze = Maze(
    m,
    n,
    processed_data=processed_data,
    algorithm=algorithm,
    maze_style=maze_style,
    layout_style=layout,
    walls=array_of_walls,
    type_of_walls=walls_type,
)


if config.debugging:
    print(maze.maze_array[-1])
# frames declaration
slides = {}
for i in range(frames_count):
    slides[i] = maze.fill_maze(i)

# ! BE AWARE ! Some css style does not support old versions of browsers
# (2) does not support Internet Explorer 7 and earlier

# app declaration
app = Dash(__name__, update_title="Loading...")

# app layout
app.title = "Maze visualisation"

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

# main layout definition
app.layout = html.Div(
    children=[
        html.H1("Demo (version 0.3)", style={"color": font_color}),
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
                    style={"height": "700px", "width": f"{700*maze.n/maze.m}px"},
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


# Callback of the slider
@app.callback(Output("ex_graph", "figure"), Input("slider", "value"))
def display_animated_graph(slider):
    global slides
    return slides[slider - 1]


# Callback for the run button
@app.callback(
    # Output("intermediate-value", "data"),
    Output("slider", "value"),
    Input("run-button", "n_clicks"),
    State("slider", "value"),
)
def button_callback(n_clicks, value):
    print(f"n_clicks: {n_clicks}, 'value': {value}")
    global animation_on
    if not n_clicks or value == frames_count:
        return 1  # dumps({"frame_number": 1}), 1

    animation_on = True
    return value + 1  # dumps({"frame_number": value + 1}), value + 1


@app.callback(
    Output("download_repr", "data"),
    Input("export_button", "n_clicks"),
    Input("radio-export", "value"),
    prevent_initial_call=True,
)
def export_file(n_clicks, chosen_export_method):
    if chosen_export_method == "bitmap representation":
        # zero stage: reverse converting
        new_pixels = reverse_bitmap_converter(maze.walls)

        size_0, size_1 = m, n

        # first stage: creating image and saving file
        img = Image.fromarray(new_pixels)

        path = config.path_to_export_data
        path_end = f"maze_map_{walls_type}_{size_0}X{size_1}.bmp"
        img.save(path + path_end)

        # second stage: outputting image
        return dcc.send_file(path + path_end)

    elif chosen_export_method == "hashtag representation":
        # reverse convert to txt
        txt_o = reverse_primitive_converter(maze.walls, 0)
        size_0, size_1 = maze.m, maze.n
        filename = f"maze_map_{walls_type}_{size_0}X{size_1}.txt"
        return dict(content=txt_o, filename=filename)
    else:
        if not walls_type:
            # reverse convert to primitive array
            prim_array = reverse_complex_converter(maze.maze_array, m, n, walls_type)
            print(prim_array)
            # reverse convert to txt
            txt_o = reverse_primitive_converter(prim_array, 1)
        else:
            txt_o = reverse_primitive_converter(maze.walls, 1)
        size_0, size_1 = maze.m, maze.n
        filename = f"maze_map_{walls_type}_{size_0}X{size_1}.txt"
        return dict(content=txt_o, filename=filename)


"""@app.callback(
        Output("intermediate-value", "data"),
        Input("intermediate-value", "data")
        )
def store_callback(value):
    global animation_on
    if value == 4:
        animation_on = False
        return dumps({"frame_number": 1})
    if animation_on:
        a = loads(value)["frame_number"] + 1
    return dumps({"frame_number": a})"""
"""# Callback of the button
@app.callback(
        Output("slider", "value"),
        Input("ex_graph", "figure"))
def run_slider_workflow(ex_graph):
    global slides
    global animation_on
    if animation_on:
        id_of_slide = id(ex_graph)
        for i in len(slides):
            slide = slides[i]
            if id(slide) == id_of_slide and i != (len(slides) + 1):
                return i + 1"""

if __name__ == "__main__":
    app.run_server(debug=config.debugging)
    print(maze.maze_array)
