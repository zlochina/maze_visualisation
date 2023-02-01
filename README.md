# maze_visualisation

Project is built on Dash and solution of visualisation part of the project is based entirely on plotting.

## Initialisation

For running Maze visualisation project on your local machine create virtual enviorment for this project:

```
python3 -m venv env

```

Install all needed dependecies noted in **requirements.txt**:

```
python3 -m pip install -r requirements.txt

```

Then activate a virtual enviorment on UNIX or macOS by typing:

```
source env/bin/activate

```

Or for Windows users:

```
.\env\Scripts\activate

```

Change directory to the one with main.py file in it and start the program:

```
cd maze_visualisation
python3 main.py

```

And there you go, you can now freely open your browser and navigate to localhost:8050

## Configuration

Main script of the project depends on some constant values written down in file **config.py**.
It is important to change values there in order to visualise your data.
Most of the values are pathes to files used by **main.py**

## Modules

> modules/app.py

This module's functions initialise layout of the page in browser.

> modules/data.py

Just stores an array of strings of the algorithms' names.

> modules/deprecated_func.py

Module that is not used by main script, however, it contains some functions used by earlier versions of the project or some functions for creating some test data

> modules/Maze.py

One of the main modules of the project. Contains class Maze, which creates every single "figure" for plotting.

> modules/maze_gen.py

One of the main modules of the project. Contains functions used by class Maze and by **main.py** script for building boundaries, converting from input data to Maze class representaion and converting in the other way

> main.py

The main module of the project. Imports data from files configured in **config.py**, converts them to Maze class representation, initiates layout of the page, initiates object of Maze class, sets up callbacks of the layout's buttons.

> config.py

Contains constant values used by **main.py**.

> config.py

Contains constant values of pathes to data.

## Updates

No updates for the project are expected. However, there are ideas yet to be implemented, but weren't due to too less time generating test data for every algorithm.

#### Some proposals

- Implement more algorithm visualisation functions to class Maze
- Add dynamic approach to configuration pathes to files of data
- Exporting files is triggered by changing choice with radio buttons (Specific idea how to implement this is added as comment to corresponding function)
- Run button functionality. Couldn't come up with good idea how to with one click run through all of the frames. The only option appears to be in adding .js script with this functionality

## Contributions

If you would be so generous as to give contributions to this repository, I would try to assist you in every way I can, the contributions themself would be greatly appreciated.

## Credit

Credit goes to the owner of this repository Jugle14 or more commonly on internet as Zlochina.
Idea of the project was given by Ing. Petr Pošík, Ph.D. of the FEE faculty of CTU, Prague
