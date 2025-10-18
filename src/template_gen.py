from blocks import markdown_to_html_node
import os
import shutil


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if "# " in line:
            no_hash = markdown.replace("#", "")
            no_hash = no_hash.strip()
            return no_hash


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        from_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()
    markdown = markdown_to_html_node(from_content)
    markdown = markdown.to_html()
    title = extract_title(from_content)
    new_template = template_content.replace("{{ Title }}", str(title))
    new_template = new_template.replace("{{ Content }}", str(markdown))
    with open(dest_path, "w") as file:
        file.write(new_template)


def generate_pages_recursive(from_path, template_path, dest_path):
    if os.path.isfile(from_path):
        from_file = open(from_path, "r")
        markdown_content = from_file.read()
        from_file.close()

        template_file = open(template_path, "r")
        template = template_file.read()
        template_file.close()

        node = markdown_to_html_node(markdown_content)
        html = node.to_html()

        title = extract_title(markdown_content)
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html)

        dest_dir_path = os.path.dirname(dest_path)
        if dest_dir_path != "":
            os.makedirs(dest_dir_path, exist_ok=True)
        to_file = open(dest_path, "w")
        to_file.write(template)
    else:
        # Store the original paths for correct base path generation
        original_from_path = from_path
        original_dest_path = dest_path

        for filename in os.listdir(original_from_path):
            # Calculate the full path for the current item
            from_path_new = os.path.join(original_from_path, filename)

            # For the destination path, if it's a file, change the extension to .html
            # (or handle it based on your desired logic. For now, assuming direct name copy)
            dest_path_new = os.path.join(original_dest_path, filename)

            # If the item is a markdown file, change the extension for the destination
            # This is a common requirement but not strictly part of the fix to your immediate error.
            if os.path.isfile(from_path_new) and from_path_new.endswith(".md"):
                dest_path_new = dest_path_new[:-3] + ".html"  # Replace .md with .html

            print(f" * {from_path_new} {template_path} -> {dest_path_new}")
            generate_pages_recursive(from_path_new, template_path, dest_path_new)
