from textnode import TextNode, TextType
from copystatic import copy_to
import shutil, os
from generate_page import generate_pages_recursive

def main():
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    copy_to("static/",  "public/")

    generate_pages_recursive("content", "template.html", "public")






main()