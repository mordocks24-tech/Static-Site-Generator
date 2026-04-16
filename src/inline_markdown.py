import re
from textnode import TextNode, TextType, LeafNode
from htmlnode import HTMLNode
from markdown_blocks import block_to_block_type, BlockType
from parentnode import ParentNode


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("not valid text type")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            node_list.append(node)
        else:
            if len(node.text.split(delimiter)) % 2 == 0:
                raise Exception("invalid markdown formatting")
            even = True
            for item in node.text.split(delimiter):
                if item != "":
                    if even:
                        node_list.append(TextNode(item, TextType.TEXT))
                    else:
                        node_list.append(TextNode(item, text_type))
                even = not even
    return node_list


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if len(extract_markdown_images(node.text)) == 0:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            remaining = node.text
            for image in images:
                alt_text = image[0]
                url = image[1]
                sections = remaining.split(f"![{alt_text}]({url})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                remaining = sections[1]
            if remaining:
                new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if len(extract_markdown_links(node.text)) == 0:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            remaining = node.text
            for link in links:
                alt_text = link[0]
                url = link[1]
                sections = remaining.split(f"[{alt_text}]({url})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                remaining = sections[1]
            if remaining:
                new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    first = [TextNode(text, TextType.TEXT)]
    result = split_nodes_delimiter(first, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_image(result)
    result = split_nodes_link(result)


    return result

def markdown_to_blocks(markdown):
    blocks = []
    unedited = markdown.split("\n\n")
    for block in unedited:
        if block.strip() == "":
            continue        
        stripped_block = block.strip()
        lines = stripped_block.splitlines()
        stripped = []
        for line in lines:
            stripped.append(line.strip())
        blocks.append("\n".join(stripped))
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            lines = block.splitlines()
            stripped = []
            for line in lines:
                stripped.append(line.strip())
            text = " ".join(stripped)
            nodes.append(ParentNode("p", text_to_children(text), None))

        if block_type == BlockType.HEADING:
            count = 0
            chopped = ""
            for char in block:
                if char == "#":
                    count += 1
                else:
                    chopped = block[count:].strip()
                    break
            nodes.append(ParentNode(f"h{count}", text_to_children(chopped), None))

        if block_type == BlockType.CODE:
            children = []
            sliced = block[4:][:-3]
            children.append(text_node_to_html_node(TextNode(sliced, TextType.CODE, None)))
            nodes.append(ParentNode("pre", children, None))

        if block_type == BlockType.QUOTE:
            lines = block.splitlines()
            stripped = []
            for line in lines:
                stripped.append(line[2:])
            result = " ".join(stripped)
            nodes.append(ParentNode("blockquote", text_to_children(result), None))

        if block_type == BlockType.UNORDERED_LIST:
            lines = block.splitlines()
            li_nodes = []
            for line in lines:
                li_nodes.append(ParentNode("li", text_to_children(line[2:])))    
            nodes.append(ParentNode("ul", li_nodes, None))

        if block_type == BlockType.ORDERED_LIST:
            lines = block.splitlines()
            li_nodes = []
            for line in lines:
                count = 0
                for char in line:
                    if char != ".":
                        count += 1
                    else:
                        count += 2
                        break
                li_nodes.append(ParentNode("li", text_to_children(line[count:])))    
            nodes.append(ParentNode("ol", li_nodes, None))
    
    
    return ParentNode("div", nodes, None)



def text_to_children(text):
    nodes = text_to_textnodes(text)
    htmlnodes = []
    for node in nodes:
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes
     
def extract_title(markdown):
    lines = markdown.splitlines()
    header_line = ""
    for line in lines:
        if line.startswith("# "):
            header_line = line
            break
    if header_line == "":
        raise Exception("No header line found!") 

    return header_line[1:].strip()
