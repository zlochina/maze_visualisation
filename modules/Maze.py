from copy import copy

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data import algorithm_list
from modules.maze_gen import build_walls_array, complex_converter

# potentially useful requirements
"""
import sys
import time

from dateutil import parser
"""

# maze class declaration
# type of walls:
#    0: thick walls
#    1: thin walls


class Maze:
    """A class for generating mazes.

    Class Maze is a class for generating mazes and visualizing them with Plotly Express.
    It is initialized with a number of rows and columns, an algorithm, a processed data dict,
    type of walls, a maze style dict, a layout style dict, and an array of walls.
    It has methods for adding a trace and an annotation, creating a tile, filling abysses within walls,
    adding images, converting a decimal array to a hex string, and filling the maze.
    """

    def __init__(
        self,
        m,
        n,
        type_of_walls,
        walls,
        style,
    ):
        # setting style specs for maze
        maze_style_details = style["maze_details"]

        grid_color = maze_style_details["grid_color"]
        boundary_color = maze_style_details["boundary_color"]
        background_color = style["background_color"]
        algorithm = style["algorithm"]

        """
        # start_point_color = maze_style_details["start_point_color"]
        # end_point_color = maze_style_details["end_point_color"]
        """

        # setting configuration and frames data variables
        """configuration = processed_data["config"]"""
        frames_data = style["iterations"]

        """
        start_point = configuration["start"]
        end_points = configuration["goal"]
        """

        # declaring sizes of maze
        self.m = m
        self.n = n

        # converting walls:
        maze_array = complex_converter(walls, m, n, type_of_walls)
        # generating dictionary of the boundaries of the maze
        x_boundary, y_boundary = build_walls_array(m, n, maze_array)

        boundaries_dict = dict(x=x_boundary, y=y_boundary)

        df = pd.DataFrame(boundaries_dict)

        # ! Setting layout of the maze !
        fig_template = px.line(df, x="x", y="y")

        # skip hoverinfo
        fig_template.update_traces(mode="lines", hoverinfo="skip", hovertemplate=None)
        # Initial range of axes of layout
        fig_template.update_layout(xaxis_range=[0, n], yaxis_range=[0, m])
        # Change style of layout
        fig_template.update_layout(paper_bgcolor=background_color)
        # change period of axes to 1 and hide titles
        fig_template.update_xaxes(
            dtick=1, title_text="", gridcolor=grid_color, visible=style["debug_mode"]
        )
        fig_template.update_yaxes(
            dtick=1, title_text="", gridcolor=grid_color, visible=style["debug_mode"]
        )

        # Change line color to black #000000
        fig_template["data"][0]["line"]["color"] = boundary_color

        """# Add start and end points
        self.create_tile(fig_template, start_point[0], start_point[1], start_point_color)

        for end_point in end_points:
            self.create_tile(fig_template, end_point[0], end_point[1], end_point_color)"""

        # add icon to end point DEBUG
        self.add_image(fig_template, 10, 1, r"")

        # Declaring template layout of the maze
        self.fig_template = fig_template

        if not type_of_walls:
            self.fill_abyss_within_walls(walls)

        # Declaring processed data
        self.frames_data = frames_data

        # Declaring objects style
        self.maze_style = style["maze_style"]

        # Declaring walls of array
        self.walls = walls

        # 2nd declaration of walls of array (for exporting needs)
        self.maze_array = maze_array

        # Declaring used algorithm
        self.algorithm = algorithm

        # Delay array (for run button)
        self.delay_array = []

    def fill_abyss_within_walls(self, array_of_walls):
        for y_i in range(self.m):
            for x_i in range(self.n):
                if array_of_walls[y_i][x_i]:
                    self.create_tile(
                        self.fig_template, x_i, self.m - y_i - 1, color="#000000"
                    )
        return 1

    # Algorithms processing
    # TODO
    # If you want to process more unique algorithms,
    # please write your methods here or create subclass for
    # these methods and export your methods
    def astar_alg_fill(self, fig, states):
        for state in states:
            # defininig some values for tile
            x_i, y_i = state["state"][0], state["state"][1]

            if "value" in state.keys():
                value = state["value"]
            else:
                value = ""
            text = self.maze_style["tile-text"].replace("$Value", str(value))

            if len(state["tags"]):
                tag = state["tags"][0]
            else:
                tag = "no-tag"

            tile_color = self.maze_style["tile-color"]["tag"][tag]

            self.create_tile(
                fig,
                x_i,
                y_i,
                tile_color,
                triangled=False,
                value=str(value),
                text=text,
            )

    # TODO
    # Behaivour of this function was not debugged,
    # so in order for it to order as expected please debug it
    # and change it for it to correspond expected format
    # of processed data
    def reinforcement_alg_fill(self, fig, states):
        # Defining q-value colors range
        q_value_color_range = self.maze_style["triangle-color"]["q-value"]
        mid_color_exists = True if q_value_color_range.has_key("mid-color") else False

        min_value = q_value_color_range["min-value"]
        min_color = q_value_color_range["min-color"]
        max_value = q_value_color_range["max-value"]
        max_color = q_value_color_range["max-color"]
        if mid_color_exists:
            mid_value = q_value_color_range["mid-value"]
            mid_color = q_value_color_range["mid-color"]

        for state in states:
            x_i, y_i = state["state"][0], state["state"][1]
            q_values = state["q-values"]
            list_of_text = [
                self.maze_style["triangle-text"].replace("$Value", i) for i in q_values
            ]
            triangles_colors = []

            # populate triangles_colors array
            for q_value in q_values:
                # convert rgb int array to hex string
                if q_value <= min_value:
                    triangle_color = self.decimal_arr_to_hex_str(min_color)

                elif q_value >= max_value:
                    triangle_color = self.decimal_arr_to_hex_str(max_color)

                elif mid_color_exists and q_value < mid_value:
                    rgb_array = [
                        int((mid_color[iter] - min_color[iter]) % 256)
                        * (q_value / mid_color)
                        for iter in range(3)
                    ]
                    triangle_color = self.decimal_arr_to_hex_str(rgb_array)

                elif mid_color_exists:
                    rgb_array = [
                        int(
                            ((mid_color[iter] - max_color[iter]) % 256)
                            * ((q_value - mid_value) / mid_color)
                        )
                        for iter in range(3)
                    ]
                    triangle_color = self.decimal_arr_to_hex_str(rgb_array)

                else:
                    rgb_array = [
                        int((max_color[iter] - min_color[iter]) % 256)
                        * (q_value / max_value)
                        for iter in range(3)
                    ]
                    triangle_color = self.decimal_arr_to_hex_str(rgb_array)

                # add resulting color hex string to the array
                triangles_colors.append(triangle_color)

            # create tile
            self.create_tile(
                fig,
                x_i,
                y_i,
                color=triangles_colors,
                triangled=True,
                text=list_of_text,
            )

    @staticmethod
    def add_trace(fig, x, y, color, text, hoverinfo="text", opacity=1):
        """Add trace to a figure.

        Args:
            fig (Plotly.figure): Figure to add a trace to.
            x (list): x-axis values of the trace.
            y (list): y-axis values of the trace.
            color (str): Color of the trace.
            text (list): Text to display when hovered over.
            hoverinfo (str, optional): Defaults to 'text'. Specifies which type of hover info to display.
        Returns:
            bool: True if successful.
        """

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                fill="toself",
                fillcolor=color,
                opacity=opacity,
                hoveron="fills",
                text=text,
                hoverinfo=hoverinfo,
                line_color=color,
                mode="none",
                showlegend=False,
            )
        )

        return True

    @staticmethod
    def add_annotation(fig, x, y, text):
        fig.add_annotation(x=x, y=y, showarrow=False, text=text[:4])

        return True

    @staticmethod
    def create_tile(
        fig, x_tmp, y_tmp, color="#FFFFFF", triangled=False, value=None, text=None
    ):
        x = [x_tmp + 1, x_tmp, x_tmp, x_tmp + 1, x_tmp + 1]
        y = [y_tmp + 1, y_tmp + 1, y_tmp, y_tmp, y_tmp + 1]

        # add diagonals to tile if triangled
        # TODO
        # triangled tiles weren't fully added to processing,
        # be sure to add it
        if triangled:
            # upper triangle
            x = [x_tmp + 1, x_tmp, x_tmp + 0.5, x_tmp + 1]
            y = [y_tmp + 1, y_tmp + 1, y_tmp + 0.5, y_tmp + 1]

            # right triangle
            x = [x_tmp + 1, x_tmp + 1, x_tmp + 0.5, x_tmp + 1]
            y = [y_tmp, y_tmp + 1, y_tmp + 0.5, y_tmp]

            # bottom triangle
            x = [x_tmp, x_tmp + 1, x_tmp + 0.5, x_tmp]
            y = [y_tmp, y_tmp, y_tmp + 0.5, y_tmp]

            # left triangle
            x = [x_tmp, x_tmp, x_tmp + 0.5, x_tmp]
            y = [y_tmp + 1, y_tmp, y_tmp + 0.5, y_tmp + 1]

        if text:
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    fill="toself",
                    fillcolor=color,
                    opacity=1,
                    hoveron="fills",
                    text=text,
                    hoverinfo="text",
                    line_color=color,
                    mode="none",
                    showlegend=False,
                )
            )

            fig.add_annotation(
                x=x_tmp + 0.5, y=y_tmp + 0.5, showarrow=False, text=value[:4]
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    fill="toself",
                    fillcolor=color,
                    hoveron="fills",
                    text=text,
                    hoverinfo="skip",
                    hovertemplate=text,
                    line_color=color,
                    mode="none",
                    showlegend=False,
                )
            )

    # static methods declaration
    @staticmethod
    def add_image(fig, x, y, source):
        dict_image_settings = dict(
            source=source,
            x=x,
            y=y,
            xref="x",
            yref="y",
            sizex=1,
            sizey=1,
            layer="above",
            opacity=1.0,
        )

        fig.add_layout_image(dict_image_settings)

        """fig.update_layout_images(dict(
                xref="paper",
                yref="paper",
                sizex=1,
                sizey=1,
                xanchor="right",
                yanchor="bottom"
        ))"""
        return None

    @staticmethod
    def decimal_arr_to_hex_str(int_array):
        string = "#"

        for value in int_array:
            string += hex(value)[2:]

        return string

    def fill_maze(self, frame_num):
        fig = copy(self.fig_template)
        # declaring frame data with states responsible for each tile info
        frame_data = self.frames_data[frame_num]
        states = frame_data["states"]

        if self.algorithm == algorithm_list[0]:
            # Processing Astar algorithm
            self.astar_alg_fill(fig, states)

        elif self.algorithm == "Reinforcement algorithm":
            # Processing reinforcment algorithm
            # WARNING
            # This function is expected to encounter some issues
            self.reinforcement_alg_fill(fig, states)

        else:
            raise BaseException(
                f"UndefinedAlgorithmError: processing algorithm {self.algorithm} data wasn't added"
            )

        # updating delay array
        timestamp_iso = frame_data["timestamp"]
        timestamp_sec = int(timestamp_iso[17:19] + timestamp_iso[20:])

        if frame_num:
            self.delay_array[frame_num - 1] = (
                timestamp_sec - self.delay_array[frame_num - 1]
            )

        self.delay_array.append(timestamp_sec)

        # Debugging
        return fig
