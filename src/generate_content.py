import os
from pathlib import Path

from block_markdown import markdown_to_html_node


def extract_title(markdown):
    if not "# " in markdown:
        raise ValueError("No header found")
    else:
        split_markdown = markdown.split("\n")
        for section in split_markdown:
            if section.startswith("# "):
                return section.replace("# ", "").strip()


def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise ValueError(f"Invalid from_path: {from_path}")
    
    if not os.path.exists(template_path):
        raise ValueError(f"Invalid template_path: {template_path}")
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding="utf-8") as from_path_contents:
        page_contents = from_path_contents.read()
    
    with open(template_path, encoding="utf-8") as template_path_contents:
        template_file_contents = template_path_contents.read()
    
    page_contents_nodes = markdown_to_html_node(page_contents)
    page_title = extract_title(page_contents)
    template_file_contents = template_file_contents.replace("{{ Title }}", page_title)
    template_file_contents = template_file_contents.replace("{{ Content }}", page_contents_nodes.to_html())

    dest_path_folders = os.path.dirname(dest_path)
    if len(dest_path_folders):
        os.makedirs(dest_path_folders, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as dest_path_contents:
        dest_path_contents.write(template_file_contents)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, filename)
        # dest_path = os.path.join(dest_dir_path, filename.replace(".md", ".html"))
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(content_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(content_path, template_path, dest_path)
        else:
            generate_pages_recursive(content_path, template_path, dest_path)
