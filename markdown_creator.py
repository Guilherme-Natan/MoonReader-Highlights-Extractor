def markdown_creator(highlight_list: list):
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
