"""Library of function that sort your highlights
"""


def hightlight_sort_by_order(highlight_list: list):
    """This funciton sorts the highlights by the order they appear on the text.

    Args:
        highlight_list (list): The list of highlits

    Returns:
        The sorted list of highlights
    """
    # Gets the sorted list of chapters
    chapter_list = [i.chapter for i in highlight_list]
    chapter_list = list(dict.fromkeys(chapter_list))  # Remove duplicates
    chapter_list.sort()

    sorted_highlight_list = []
    for chapter in chapter_list:
        highlight_list_chapter = [i for i in highlight_list if i.chapter == chapter]
        highlight_list_chapter.sort(key=lambda x: x.preceding_characters)

        sorted_highlight_list.extend(highlight_list_chapter)

    return sorted_highlight_list
