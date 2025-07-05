from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"


def markdown_to_blocks(markdown):
    blocks = []
    split_markdown = markdown.split("\n\n")

    for block in split_markdown:
        if len(block.lstrip().rstrip()):
            blocks.append(block.lstrip().rstrip())

    return blocks


def block_to_block_type(markdown):
    if markdown[:7] == "###### " or markdown[:6] == "##### " or markdown[:5] == "#### " or markdown[:4] == "### " or markdown[:3] == "## " or markdown[:2] == "# ":
        return BlockType.HEADING
    
    if markdown.startswith("```") and markdown.endswith( "```"):
        return BlockType.CODE
    
    quote_block = True
    for segment in markdown.split("\n"):
        if not segment.startswith(">"):
            quote_block = False
    
    if quote_block:
        return BlockType.QUOTE
    
    unordered_list = True
    for segment in markdown.split("\n"):
        if not segment.startswith("- "):
            unordered_list = False
    
    if unordered_list:
        return BlockType.UNORDERED_LIST
    
    ordered_list = True
    for i, segment in enumerate(markdown.split("\n")):
        if not segment.startswith(f"{i + 1}. "):
            ordered_list = False
    
    if ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_nodes(text):
    text_nodes = text_to_textnodes(text)
    nodes = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        nodes.append(html_node)

    return nodes


def heading_to_html_node(block):
    level = 0

    for char in block:
        if char == "#":
            level += 1
        else:
            break

    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    
    text = block[level + 1 :]
    nodes = text_to_nodes(text)

    return ParentNode(f"h{level}", nodes)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    node = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [node])

    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        
        new_lines.append(line.lstrip(">").strip())

    content = " ".join(new_lines)
    nodes = text_to_nodes(content)

    return ParentNode("blockquote", nodes)


def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []

    for item in items:
        text = item[2:]
        nodes = text_to_nodes(text)
        html_items.append(ParentNode("li", nodes))

    return ParentNode("ul", html_items)


def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []

    for item in items:
        text = item[3:]
        nodes = text_to_nodes(text)
        html_items.append(ParentNode("li", nodes))

    return ParentNode("ol", html_items)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    nodes = text_to_nodes(paragraph)

    return ParentNode("p", nodes)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case _:
            raise ValueError("invalid block type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        html_node = block_to_html_node(block)
        nodes.append(html_node)

    return ParentNode("div", nodes, None)
