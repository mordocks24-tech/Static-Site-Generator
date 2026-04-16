import unittest
from markdown_blocks import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_quote(self):
        block = ">This is a quote\n>So is this"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_not_quote(self):
        block = ">This is a quote\nBut this is not"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()