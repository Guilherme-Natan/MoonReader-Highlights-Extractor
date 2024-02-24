import webcolors


class highlight_content:
    def __init__(
        self,
        preceding_characters,
        color,
        unix_time,
        note,
        highlighted_text,
        highlight_type,
    ):
        self.preceding_characters = preceding_characters
        self.color = color
        self.unix_time = unix_time
        self.note = note
        self.highlighted_text = highlighted_text
        self.highlight_type = highlight_type


def detect_highlights(file_content: str):
    file_iterator = iter(file_content.split("\n"))
    highlight_list = []
    while True:
        try:
            line = next(file_iterator)
        except StopIteration:
            break

        if line == "#":
            highlight, file_iterator = extract_highlights(file_iterator)
            highlight_list.append(highlight)

    return highlight_list


def extract_highlights(file_iterator: iter):
    next(file_iterator)
    next(file_iterator)
    next(file_iterator)
    next(file_iterator)
    next(file_iterator)
    next(file_iterator)
    preceding_characters = next(file_iterator)
    preceding_characters = int(preceding_characters)
    next(file_iterator)
    color = next(file_iterator)
    color = int(color)
    color = color_process(color)
    unix_time = next(file_iterator)
    next(file_iterator)
    note = next(file_iterator)
    highlighted_text = next(file_iterator)
    if next(file_iterator) == 1:
        highlight_type = "underline"
    elif next(file_iterator) == 1:
        highlight_type = "strikethrough"
    elif next(file_iterator) == 1:
        highlight_type = "squiggly"
    else:
        highlight_type = "highlight"
    highlight = highlight_content(
        preceding_characters, color, unix_time, note, highlighted_text, highlight_type
    )
    return highlight, file_iterator


def color_process(color: int):
    if color < 0:
        color = 4294967296 + color

    color = color % 16777216  # Removes the alpha component
    red, color = divmod(color, 65536)  # Gets the red component
    green, blue = divmod(color, 256)  # Gets both the green and blue component

    rgb_color = (red, green, blue)
    color = get_colour_name(rgb_color)
    return color


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    # Taken and slightly altered from
    # https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
    try:
        closest_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
    return closest_name
