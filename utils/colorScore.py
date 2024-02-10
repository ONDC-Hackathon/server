import matplotlib.colors as mcolors
from sklearn.metrics import pairwise_distances_argmin_min

# Function to convert color name to RGB


def color_name_to_rgb(color_name):
    try:
        color = tuple(int(x * 255) for x in mcolors.to_rgb(color_name))
    except:
        color = (0, 0, 0)
    return color

# Function to find the closest color


def find_closest_color_score(color_name, dominant_colors):
    color_rgb_value = color_name_to_rgb(color_name)
    colors_rgb_list = [[color["red"], color["green"], color["blue"]]
                       for color in dominant_colors]

    closest_idx, _ = pairwise_distances_argmin_min(
        [color_rgb_value], colors_rgb_list)
    closest_color = dominant_colors[closest_idx[0]]
    return closest_color["score"]
