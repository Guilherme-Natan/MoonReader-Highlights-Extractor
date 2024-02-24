def hightlight_sorter(highlight_list: list):
    chapter_list = [i.chapter for i in highlight_list]
    chapter_list = list(dict.fromkeys(chapter_list))  # Remove duplicates
    chapter_list.sort()

    sorted_highlight_list = []
    for chapter in chapter_list:
        highlight_list_chapter = [i for i in highlight_list if i.chapter == chapter]
        highlight_list_chapter.sort(key=lambda x: x.preceding_characters)

        sorted_highlight_list.extend(highlight_list_chapter)

    return sorted_highlight_list
