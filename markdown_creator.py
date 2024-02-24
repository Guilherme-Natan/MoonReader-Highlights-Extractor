"""Library of functions related to the creation of the markdown file
"""


def markdown_creator_by_order(highlight_list: list):
    """Creates the markdown file, based upon a list of highlights, sorted by
    the order at which they apper at the book

    Args:
        highlight_list (list): The list of highlights

    Returns:
        A string, with the contents of the markdown file
    """
    markdown_text = []
    for i in highlight_list:
        markdown_text.append(f"> {i.highlighted_text}")
        markdown_text.append(">")
        markdown_text.append(f"> — {i.color} {i.highlight_type}, {i.date}")
        markdown_text.append("")
        if i.note:
            markdown_text.append(i.note)
            markdown_text.append("")

    markdown_text = "\n".join(markdown_text)
    return markdown_text
