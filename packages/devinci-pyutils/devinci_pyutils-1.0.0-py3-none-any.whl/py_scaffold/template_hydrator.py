import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

with open(f'{SCRIPT_DIR}/stubs/_class.stub.py','r') as stub:
    CLASS_TEMPLATE = stub.read().rstrip("\'\'\'").lstrip("\'\'\'")

with open(f'{SCRIPT_DIR}/stubs/_wiki.stub.py','r') as stub:
    WIKI_TEMPLATE = stub.read().rstrip("\"\"\"").lstrip("\"\"\"")


def generate_attributes_docstring(attributes):
    """Generate the attributes section of the docstring."""
    return '\n'.join(
        [f'    {attr} (int): Description of {attr}.' for attr in attributes])


def generate_attributes_methods_docstring(attributes):
    """Generate the attributes methods section of the docstring."""
    return '\n'.join(
        [f'    {attr} (property): Getter and setter method for {attr}.' for attr
         in attributes])


def generate_init_args(attributes):
    """Generate the __init__ arguments."""
    return ''.join([f', {attr}: int = 0' for attr in attributes])


def generate_init_body(attributes):
    """Generate the __init__ body."""
    return '\n'.join([f'        self._{attr} = {attr}' for attr in attributes])


def generate_attributes_properties(attributes):
    """Generate the property methods for attributes."""
    properties = []
    for attr in attributes:
        properties.append(f'''    @property
    def {attr}(self) -> int:
        """
        Gets the value of {attr}.

        Returns:
            int: The value of {attr}.
        """
        return self._{attr}

    @{attr}.setter
    def {attr}(self, value: int) -> None:
        """
        Sets the value of {attr}.

        Args:
            value (int): The value to set.
        """
        self._{attr} = value
''')
    return '\n'.join(properties)


def generate_content(class_name, parent_class, attributes):
    """Generate the content of the class file."""
    attributes_docstring = generate_attributes_docstring(attributes)
    attributes_methods_docstring = generate_attributes_methods_docstring(
        attributes)
    init_args = generate_init_args(attributes)
    init_body = generate_init_body(attributes)
    attributes_properties = generate_attributes_properties(attributes)

    return CLASS_TEMPLATE.format(
        class_name=class_name,
        parent_class=parent_class,
        attributes_docstring=attributes_docstring,
        attributes_methods_docstring=attributes_methods_docstring,
        init_args=init_args,
        init_body=init_body,
        attributes_properties=attributes_properties
    )
