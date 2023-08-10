import matplotlib.pyplot as plt
import numpy as np
from config import LAT_BOUNDS, LON_BOUNDS, MAP_RESOLUTION


def bresenham_line(start, end):
    # Bresenham's line algorithm
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            yield x, y
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            yield x, y
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    yield x, y


plt.style.use('seaborn')
width = 345

tex_fonts = {
    # Use LaTeX to write all text
    "text.usetex": True,
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 10,
    "font.size": 10,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8
}

plt.rcParams.update(tex_fonts)


def set_size(width, fraction=1, subplots=(1, 1)):
    """Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float or string
            Document width in points, or string of predined document type
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy
    subplots: array-like, optional
            The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    if width == 'thesis':
        width_pt = 426.79135
    elif width == 'beamer':
        width_pt = 307.28987
    else:
        width_pt = width

    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5 ** .5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

    return (fig_width_in, fig_height_in)


def display_array_with_path(array, path_coords, cmap='inferno', filename=None):
    x_labels = LON_BOUNDS
    y_labels = LAT_BOUNDS
    y_tick_locs = [0, array.shape[1]-1]
    x_tick_locs = [0, array.shape[0]-1]

    fig, ax = plt.subplots(figsize=set_size(700))
    im = ax.imshow(array.T, cmap=cmap, origin='lower', interpolation='nearest')
    ax.tick_params(left=True, right=False,
                   bottom=True, top=False, labeltop=False,
                   labelleft=True, labelbottom=True)
    ax.set_xticks(x_tick_locs)
    ax.set_yticks(y_tick_locs)
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')

    # Convert path coordinates to separate x and y arrays for plotting
    x_coords, y_coords = zip(*path_coords)

    # Plotting the path coordinates
    ax.plot(y_coords, x_coords, color='green', alpha=0.5)

    cb = fig.colorbar(im)  # Display a colorbar (useful for visualizing numerical values in the array)
    cb.set_label('Fatality Risk [flt hr $^{-1}$]')  # Label the colorbar

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight', format='eps')
    fig.show()


def display_node_costs(nodes, grid, cmap='inferno'):
    # Display the costs of each node in a list as an array
    # This is useful for visualizing the cost of each node in the path
    cost_real = np.zeros(grid.shape)
    cost_img = np.zeros(grid.shape)
    for node in nodes:
        cost_real[node.y, node.x] = node.g[0]
        cost_img[node.y, node.x] = node.g[1]

    # Mask zeros as none so they don't show up on the plot
    cost_real = np.ma.masked_where(cost_real == 0, cost_real)
    cost_img = np.ma.masked_where(cost_img == 0, cost_img)

    plt.figure(figsize=set_size(700))
    plt.title("Real Costs")
    plt.imshow(cost_real.T, cmap=cmap, origin='lower', interpolation='nearest')
    plt.colorbar()
    plt.show()

    plt.figure(figsize=set_size(700))
    plt.title("Imaginary Costs")
    plt.imshow(cost_img.T, cmap=cmap, origin='lower', interpolation='nearest')
    plt.colorbar()
    plt.show()
