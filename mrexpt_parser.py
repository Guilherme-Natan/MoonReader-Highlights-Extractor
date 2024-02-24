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


def get_colour_name(rgb):
    # Taken and slightly altered from JSch9619 answer at
    # https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
    colors = {
        "Red": (255, 0, 0),
        "Lime": (0, 255, 0),
        "Blue": (0, 0, 255),
        "Yellow": (255, 255, 0),
        "Magenta": (255, 0, 255),
        "Cyan": (0, 255, 255),
        "Black": (0, 0, 0),
        "White": (255, 255, 255),
        # "Grey": (128, 128, 128),
        "Green": (0, 128, 0),
        "Maroon": (128, 0, 0),
        "Navy": (0, 0, 128),
        "Olive": (128, 128, 0),
        "Purple": (128, 0, 128),
        # "Silver": (192, 192, 192),
        "Teal": (0, 128, 128),
        "Orange": (255, 165, 0),
        "Lavander": (230, 230, 250),
    }
    min_distance = float("inf")
    closest_color = None
    for color, value in colors.items():
        distance = sum([(i - j) ** 2 for i, j in zip(rgb, value)])
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color
