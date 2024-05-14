"""
Script for generating scaffolded Python class files along with optional wiki documentation.

This script allows users to create Python class files with optional features such as inheritance,
attribute definition, package structure, and generation of wiki documentation.

Usage:
    python script.py MyClass ParentClass --package --attributes attr1 attr2 --wiki

Arguments:
    MyClass: The name of the class to create, possibly with a nested package path.
    ParentClass (optional): The parent class to inherit from.
    --package: Flag to create a package instead of a single module.
    --attributes attr1 attr2: List of attributes for the class (optional).
    --wiki: Flag to generate a wiki for the created class.

Examples:
    python script.py MyClass ParentClass --package --attributes attr1 attr2 --wiki

This script utilizes helper functions from external modules 'helpers' and 'template_hydrator' to format class names,
generate class content, and create nested directories.

"""

import os
import argparse
from helpers import (camel_case, snake_case, format_class_name,
                      format_parent_class)
from template_hydrator import generate_content, WIKI_TEMPLATE

def create_nested_directories(class_name, package):
    """
    Create nested directories if needed and return the file name.

    Args:
        class_name (str): The name of the class.
        package (bool): Indicates whether to create a package or not.

    Returns:
        tuple: A tuple containing the file name, __init__ file name, and package name.
    """
    if '.' in class_name:
        nested_path = os.path.join(*class_name.split('.')[:-1])
        package_name = snake_case(class_name.split('.')[-1])
        os.makedirs(nested_path, exist_ok=True)
        if package:
            file_name = os.path.join(nested_path, package_name, f"{package_name}.py")
            os.makedirs(os.path.join(nested_path, package_name), exist_ok=True)
            return file_name, os.path.join(nested_path, package_name,'__init__.py'), package_name
        else:
            return os.path.join(nested_path, f"{package_name}.py"), None, None
    else:
        if package:
            package_name = snake_case(class_name)
            os.makedirs(package_name, exist_ok=True)
            return os.path.join(package_name, f"{package_name}.py"), os.path.join(package_name, '__init__.py'), package_name
        else:
            return f"{snake_case(class_name)}.py", None, None

def write_to_file(file_name, content):
    """
    Write the content to the class file.

    Args:
        file_name (str): The name of the file to write to.
        content (str): The content to write to the file.
    """
    with open(file_name, 'w') as file:
        file.write(content)

def create_init_file(init_file_name, class_name, package_name):
    """
    Create __init__.py with import statement.

    Args:
        init_file_name (str): The name of the __init__.py file.
        class_name (str): The name of the class.
        package_name (str): The name of the package.
    """
    init_file_content = f"from .{package_name} import {class_name}\n"
    with open(init_file_name, 'w') as init_file:
        init_file.write(init_file_content)

def generate_wiki(class_name):
    """
    Generate wiki content based on stub.

    Args:
        class_name (str): The name of the class.

    Returns:
        str: The generated wiki content.
    """
    wiki_content = WIKI_TEMPLATE.replace('{{Title}}', class_name)
    return wiki_content

def create_class_file(class_name, parent_class=None, package=False, attributes=None, wiki=False):
    """
    Create a Python class file along with an optional wiki file.

    Args:
        class_name (str): The name of the class to create.
        parent_class (str, optional): The parent class to inherit from.
        package (bool, optional): Indicates whether to create a package or not.
        attributes (list, optional): List of attributes for the class.
        wiki (bool, optional): Indicates whether to generate a wiki file or not.
    """

    class_name = format_class_name(class_name)

    parent_class = format_parent_class(parent_class)
    content = generate_content(class_name, parent_class, attributes or [])
    file_name, init_file_name, package_name = create_nested_directories(class_name, package)

    write_to_file(file_name, content)
    if init_file_name and package_name:
        create_init_file(init_file_name, class_name, package_name)

    print(f"Class file '{file_name}' has been created successfully.")

    if wiki:
        wiki_content = generate_wiki(class_name)
        wiki_file_name = f"docs/{class_name}_wiki.md"
        write_to_file(wiki_file_name, wiki_content)
        print(f"Wiki file '{wiki_file_name}' has been created successfully.")

def main():
    """
    Main function to parse command-line arguments and create class files.
    """
    parser = argparse.ArgumentParser(description="Generate a scaffolded Python class file.")
    parser.add_argument("class_name", help="The name of the class to create, possibly with nested package path.")
    parser.add_argument("parent_class", nargs="?", help="The parent class to inherit from (optional).")
    parser.add_argument("--package", action="store_true", help="Create a package instead of a single module.")
    parser.add_argument("--attributes", nargs="*", help="List of attributes for the class (optional).")
    parser.add_argument("--wiki", action="store_true", help="Generate a wiki for the created class.")
    args = parser.parse_args()

    create_class_file(args.class_name, args.parent_class, args.package, args.attributes, args.wiki)

if __name__ == "__main__":
    main()
