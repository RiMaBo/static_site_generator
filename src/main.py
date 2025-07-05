import os
import shutil
import sys

from copystatic import copy_site_contents
from generate_content import generate_pages_recursive


static = "static"
public = "docs"
content = "content"
template = "template.html"
default_basepath = "/"


def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(f"Deleting folder {public}...")
    if os.path.exists(public):
        shutil.rmtree(public)
    
    print(f"Copying files from {static} to {public}...")
    copy_site_contents(static, public)

    print("Generating content...")
    # generate_page(os.path.join(content, "index.md"), template, os.path.join(public, "index.html"))
    generate_pages_recursive(content, template, public, basepath)


main()
