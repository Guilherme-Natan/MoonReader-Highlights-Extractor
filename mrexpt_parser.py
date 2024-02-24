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
    color = color_adjust(color)
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


def color_adjust(color: int):
    if color < 0:
        color = 4294967296 + color
    return color
