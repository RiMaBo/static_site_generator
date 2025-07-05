import os
import shutil

from copystatic import copy_site_contents
from generate_content import generate_pages_recursive


static = "static"
public = "public"
content = "content"
template = "template.html"


def main():
    print(f"Deleting folder {public}...")
    if os.path.exists(public):
        shutil.rmtree(public)
    
    print(f"Copying files from {static} to {public}...")
    copy_site_contents(static, public)

    print("Generating content...")
    # generate_page(os.path.join(content, "index.md"), template, os.path.join(public, "index.html"))
    generate_pages_recursive(content, template, public)


main()
