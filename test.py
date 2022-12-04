from maze_gen import maze_genearator
import numpy as np

m = 2
n = 3
print(f"Printing {m}X{n} array of tiles or {m+1}X{n+1} array of points:")
print(np.array(maze_genearator(2, 3)))

# rest of the program TO DELETE
def figure_creator(color_d, df):
    fig = px.line(df, x="x", y="y")

    # Add text in the center of triangle
    fig.add_annotation(x=2.5, y=2.5, text="+10", showarrow=False)
    fig.add_annotation(x=2.75, y=3, text="-0.6", showarrow=False)
    fig.add_annotation(x=3.5, y=3, text="0.9", showarrow=False)

    # Initial range of axes of layout
    fig.update_layout(xaxis_range=[0,11], yaxis_range=[-1, 11])

    #fill color area
    fig.add_trace(go.Scatter(x=[2, 2.5, 3], y=[2, 3, 2],
                        fill='toself', fillcolor = '#A2D2FF',
                        hoveron = 'fills',
                        text="10",
                        hoverinfo = 'text',
                        line_color='#A2D2FF',
                        mode='none',
                        showlegend=False))

    fig.add_trace(go.Scatter(x=[3, 2.5, 3], y=[2, 3, 4],
                        fill='toself', fillcolor = '#CDB4DB',
                        hoveron = 'fills',
                        text="-0.6",
                        hoverinfo = 'text',
                        line_color='#CDB4DB',
                        mode='none',
                        showlegend=False))

    fig.add_trace(go.Scatter(x=[2, 2.5, 2], y=[4, 3, 2],
                        fill='toself', fillcolor = color_d,
                        hoveron = 'fills',
                        text="None",
                        hoverinfo = 'text',
                        line_color=color_d,
                        mode='none',
                        showlegend=False))
    return fig
