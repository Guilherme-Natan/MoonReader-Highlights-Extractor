"""Extracts the content from a mrexpt file (generated from moonreader), 
and places its contents into a markdown file

Usage: python3 moonreader.py <mrexpt_file_path>
"""

#!/usr/bin/env python3

import sys

import highlight_sorter
import markdown_creator
import mrexpt_parser


def main():
    # Extracts the mrexpt file content
    with open(sys.argv[1], "r", encoding="utf-8") as file:
        file_content = file.read()

    highlight_list = mrexpt_parser.detect_highlights(file_content)
    highlight_list_sorted = highlight_sorter.hightlight_sort_by_order(highlight_list)
    markdown_content = markdown_creator.markdown_creator_by_order(highlight_list_sorted)

    filename_markdown_extension = f'{sys.argv[1].split(".")[0]}.md'

    # Saves the markdown file
    with open(filename_markdown_extension, "w", encoding="utf-8") as file:
        # Read the entire file content into a variable
        file.write(markdown_content)


if __name__ == "__main__":
    main()
