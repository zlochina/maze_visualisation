from dash import Dash, html, dcc, Input, Output, State

from json import load, dumps, loads

# importing from project modules
from modules.maze_gen import primitive_converter
from modules.Maze import Maze
from time import sleep

"""
Demo version 0.3
"""

""" INITIALISING """
# importing style specs for maze page
with open("data/layout.json", "r") as r:
    layout = load(r)

# setting layout specs
background_color = layout["background_color"]
font_color = layout["font_color"]

# importing style specs for maze objects
with open("algorithm_data/style.json", "r") as r:
    maze_style = load(r)

# importing processed data from json
with open("algorithm_data/astar-4iters-recording.json", 'r') as r:
    processed_data = load(r)

configuration = processed_data["config"]
frames_data = processed_data["frames"]

frames_count = len(frames_data)
walls_type = 1 if configuration["env_type"] == "walls_between_tiles" else 0
algorithm = configuration["alg"]



# app declaration
app = Dash(__name__, update_title="Loading...")

# size of maze declaration 

debugging = True
animation_on = False
maze_text = """   #   #   


#  ## ##  #
   #   #

   #   #
#  ## ##  #


   #   #   """

array_of_walls = primitive_converter(maze_text, walls_type)
m = len(array_of_walls)
n = len(array_of_walls[0])

# output to cmd
if debugging:
    print("\n~~Updated~~\n")

# maze declaration 
maze = Maze(m, n, processed_data = processed_data, algorithm = algorithm, maze_style = maze_style, layout_style = layout, walls = array_of_walls, type_of_walls = walls_type)

# frames declaration
slides = {}
for i in range(frames_count):
    slides[i] = maze.fill_maze(i)



# ! BE AWARE ! Some css style does not support old versions of browsers
# (2) does not support Internet Explorer 7 and earlier

# app layout
app.title = "Maze visualisation"
app.layout = html.Div(children=[
    html.H1("Demo (version 0.3)", style={"color": font_color}),
    html.Div(children=[
    
    html.Div(children=[
    html.Br(),
    html.Label("Choose algorithm", style={"padding": 10, "color": font_color}),

    html.Br(),
    dcc.RadioItems(["A*", "DFS", "BFS"], "A*")], style={"padding": 10, "flex": 1, "color": font_color}),
    html.Div(children=[
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
        html.Button("Run", id="run-button", n_clicks=0, style={"color": font_color})
    ], style={"padding": 10, "flex": 1}),
    ], style={"display": "flex", "flex-direction": "row"}),

    html.Div(children=[
    # dcc.Store stores the intermediate value
    dcc.Store(id='intermediate-value'),
    dcc.Graph(
        id='ex_graph',
        style={'height': '700px', 'width': f'{700*maze.n/maze.m}px'}
    )], style={"display": "table", "margin": "0 auto"}) # (2)
], style={"display": "flex", "flex-direction": "column", "backgroundColor": background_color}) 



# Callback of the slider
@app.callback(
    Output("ex_graph", "figure"),
    Input("slider", "value"))
def display_animated_graph(slider):
    global slides
    return slides[slider-1]

@app.callback(
    #Output("intermediate-value", "data"),
    Output("slider", "value"),
    Input("run-button", "n_clicks"),
    State("slider", "value")
)
def button_callback(n_clicks, value):
    print(f"n_clicks: {n_clicks}, 'value': {value}")
    global animation_on
    if not n_clicks or value == 4:
        return 1 #dumps({"frame_number": 1}), 1
    
    animation_on = True
    return value + 1#dumps({"frame_number": value + 1}), value + 1

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

    app.run_server(debug=debugging)
