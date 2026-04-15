from htmlnode import HTMLNode
import unittest

class Test_htmlnode(unittest.TestCase):
    def test_none_tag(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertIsNone(node.tag, node2.tag)

    


if __name__ == "__main__":
    unittest.main()