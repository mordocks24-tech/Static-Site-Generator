from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
        lines = block.splitlines()

        count = 0
        for char in block:
            if char == "#":
                count += 1 
            else:
                if count > 0 and count < 7:
                    if char == " ":
                        return BlockType.HEADING


        if block[:4] == "```\n" and block[-3:] == "```":
            return BlockType.CODE


        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST

        if all(line.startswith(f"{num}. ") for num, line in enumerate(lines, start=1)):
            return BlockType.ORDERED_LIST

        return BlockType.PARAGRAPH
