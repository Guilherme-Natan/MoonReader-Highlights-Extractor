"""Parses the mrexpt file, extracting all relevant content into a highlight object
"""

from datetime import datetime


class highlight_content:
    """Class that represents a highlight, with all its relevant information.

    Attributes:
    chapter: The chapter's number. For sorting purposes.
    preceding_characters: The number of character that precedes the first
      letter from the highlighted text
    color: The highlight color's english name
    date: The date the highlight was made
    note: The note embedded into the highlight, if it was created
    highlighted_text: The actual highlighted text
    highlighted_type: The type of the highlight (highlight, underline, strikethrough and squiggly)
    """

    def __init__(
        self,
        chapter,
        preceding_characters,
        color,
        date,
        note,
        highlighted_text,
        highlight_type,
    ):
        self.chapter = chapter
        self.preceding_characters = preceding_characters
        self.color = color
        self.date = date
        self.note = note
        self.highlighted_text = highlighted_text
        self.highlight_type = highlight_type


def detect_highlights(file_content: str):
    """This function will detect every highlight (blocks of text that begin
    with a line consisting of the character "#").

    Args:
        file_content (str): The content from the mrexpt file

    Returns:
        A list, consisting of every highlight object
    """
    file_iterator = iter(file_content.split("\n"))
    highlight_list = []
    # Tries to find a line that consists of the character "#".
    # If it does, extracts the highlight below it
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
    """This function extracts every useful information from a highlight, and
    stores it into a highlight object

    Args:
        file_iterator (iter): An iterator, where every element as a line from
        the mrexpt file

    Returns:
        A tuple, consisting of the highlight object, and the iterator
    """
    # Ignores the first 4 lines
    next(file_iterator)
    next(file_iterator)
    next(file_iterator)
    next(file_iterator)

    # Gets the chapter number, and saves it as an int
    chapter = next(file_iterator)
    chapter = int(chapter)

    # Ignores the next line
    next(file_iterator)

    # Gets the preceding characters number, and saves it as an int
    preceding_characters = next(file_iterator)
    preceding_characters = int(preceding_characters)

    # Ignores the next line
    next(file_iterator)

    # Gets the color code, and tries to get the english name of that color
    color = next(file_iterator)
    color = int(color)
    color = color_process(color)

    # Gets the unix time, and converts it to a human readable form
    unix_time = next(file_iterator)
    unix_time = int(unix_time) / 1000
    date = datetime.fromtimestamp(unix_time).strftime("%d %B %Y, %H:%M:%S")

    # Ignores the next line
    next(file_iterator)

    # Gets the note, and the highlighted text
    note = next(file_iterator)
    highlighted_text = next(file_iterator)

    # Gets the highlight type
    if next(file_iterator) == "1":
        highlight_type = "underline"
    elif next(file_iterator) == "1":
        highlight_type = "strikethrough"
    elif next(file_iterator) == "1":
        highlight_type = "squiggly"
    else:
        highlight_type = "highlight"

    # Creates the highlight object, based on the information above
    highlight = highlight_content(
        chapter,
        preceding_characters,
        color,
        date,
        note,
        highlighted_text,
        highlight_type,
    )
    return highlight, file_iterator


def color_process(color: int):
    """This funciton gets the color code from the mrexpt file, and associates it with a color name

    Args:
        color (int): The color code

    Returns:
        The english color name
    """
    # It seems that moonreader stores the color code as a ARGB 32 bit signed int.
    # Because of that, numbers bigger than 2^31 ends up overflowing to a
    # negative number. The bellow equation fix that, by checking if the
    # color code is negative, and adding it with 2^32 if so
    if color < 0:
        color = 4294967296 + color

    # Transforms the color code from its decimal form to the RGB form
    color = color % 16777216  # Removes the alpha component
    red, color = divmod(color, 65536)  # Gets the red component
    green, blue = divmod(color, 256)  # Gets both the green and blue component

    rgb_color = (red, green, blue)
    color = get_color_name(rgb_color)
    return color


def get_color_name(rgb: tuple):
    """This function tries to get the english name from a color, based on its color code.

    Taken and slightly altered from JSch9619's answer at
    https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python

    Args:
        rgb (tuple): The red, blue and green components from the color

    Returns:
        The english name from the color
    """
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
