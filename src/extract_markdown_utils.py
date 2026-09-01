import re


def extract_markdown_images(text):
    img_tag_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return img_tag_matches


def extract_markdown_links(text):
    link_tag_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_tag_matches
