import os
from json import load

from dash import Dash, Input, Output, State, dcc
from PIL import Image

import config
import constants
from modules.app import declare_export_block, declare_layout
from modules.Maze import Maze
from modules.maze_gen import (bitmap_converter, primitive_converter,
                              reverse_bitmap_converter,
                              reverse_complex_converter,
                              reverse_primitive_converter)

"""
Demo version 0.4
"""


def main():
    # Reading files
    style_dict = dict()
    style_dict["debug_mode"] = config.debugging

    # importing style specs for maze page
    with open(config.path_to_specs, "r") as r:
        layout = load(r)

        background_color = layout["background_color"]
        font_color = layout["font_color"]
        style_dict["maze_details"] = layout["maze_details"]
        style_dict["background_color"] = background_color

        del layout

    # importing style specs for maze objects
    with open(config.path_maze_specs, "r") as r:
        maze_style = load(r)
        style_dict["maze_style"] = maze_style
        del maze_style

    # importing processed data from json
    with open(config.path_to_processed_data, "r") as r:
        processed_data = load(r)

        configuration = processed_data["config"]
        frames_data = processed_data["iterations"]
        filename = configuration["file"]
        represantation_method = configuration["map"]

        del processed_data

        frames_count = len(frames_data)
        walls_type = 1 if configuration["env_type"] == "walls_between_tiles" else 0
        # walls_type = 1
        algorithm = "Astar"  # TODO change it
        style_dict["algorithm"] = algorithm
        style_dict["iterations"] = frames_data

    # importing maze map
    if filename not in os.listdir(config.path_to_maps_dir):
        print("ERROR: failed to navigate to map")
        os._exit(constants.error_enum["FAILED_PATH_TO_DATA"])

    if represantation_method == constants.mappings_tuple[2]:
        maze_text = Image.open(config.path_to_maps_dir + filename)
    else:
        with open(config.path_to_maps_dir + filename, "r") as r:
            maze_text = r.read()[:-1]

    if represantation_method == constants.mappings_tuple[2]:
        return_tuple = bitmap_converter(maze_text)
        array_of_walls = return_tuple[0]

        start_point = return_tuple[1][0]  # start point is returned,
        # but not used
        end_point = return_tuple[1][1]  # end point is returned, but not used
    else:
        array_of_walls = primitive_converter(maze_text, walls_type)
    m = len(array_of_walls)
    n = len(array_of_walls[0])

    if walls_type:
        n -= 1

    # output to cmd
    if config.debugging:
        print("\n~~Updated~~\n")

    # maze declaration
    maze = Maze(
        m,
        n,
        walls=array_of_walls,
        type_of_walls=walls_type,
        style=style_dict,
    )

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
    style_block = {
        "font_color": font_color,
        "algorithm": algorithm,
        "background_color": background_color,
        "frames_count": frames_count,
        "m": maze.m,
        "n": maze.n,
    }
    export_block = declare_export_block(walls_type, style_block)

    # main layout definition
    blocks = (export_block,)

    app.layout = declare_layout(style_block, blocks)

    # Callback of the slider
    @app.callback(Output("ex_graph", "figure"), Input("slider", "value"))
    def display_animated_graph(slider):
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
            return 1

        animation_on = True
        return value + 1

    # callback for export button
    # TODO remove input of radio buttons, in exchange add
    # datastore to some element, which will be storing data
    # of chosen export method and create a callback which
    # will react to radio button and change value in datastore
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
                prim_array = reverse_complex_converter(
                    maze.maze_array, m, n, walls_type
                )
                # reverse convert to txt
                txt_o = reverse_primitive_converter(prim_array, 1)
            else:
                txt_o = reverse_primitive_converter(maze.walls, 1)
            size_0, size_1 = maze.m, maze.n
            filename = f"maze_map_{walls_type}_{size_0}X{size_1}.txt"
            return dict(content=txt_o, filename=filename)

    return app


if __name__ == "__main__":
    app = main()
    app.run_server(debug=config.debugging)
