from inline_markdown import markdown_to_html_node, extract_title
import os
import pathlib

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    
    with open(from_path) as f:
        fpath_contents = f.read()
    with open(template_path) as f:
        tpath_contents = f.read()
    
    html_string = markdown_to_html_node(fpath_contents).to_html()
    title = extract_title(fpath_contents)

    placeholder = tpath_contents.replace("{{ Title }}", title)
    almost = placeholder.replace("{{ Content }}", html_string)
    nearly = almost.replace('href="/', 'href="' + basepath)
    final_page = nearly.replace('src="/', 'src="' + basepath)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_page)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        if entry.endswith(".md"):
            generate_page(basepath, os.path.join(dir_path_content, entry), template_path, os.path.join(dest_dir_path, pathlib.Path(entry).with_suffix(".html")))
        else:
            generate_pages_recursive(basepath, os.path.join(dir_path_content, entry), template_path, os.path.join(dest_dir_path, entry))