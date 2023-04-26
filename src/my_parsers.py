import ast

class GenericFinder(ast.NodeVisitor):
    def __init__(self, node_type):
        self.node_type = node_type
        self.found = []

    def generic_visit(self, node):
        if node.__class__.__name__ == self.node_type:
            self.found.append(node)
        super().generic_visit(node)


def get_all_methods(locals_dict: dict):
    # From a given dictionnary, return the list of functions from a piece of code
    dunder = ["__builtins__"]  # Could be replaced by dictionnary if list grows
    functions = {}
    for k, v in locals_dict.items():
        if k not in dunder and isinstance(v, function):
            functions[k] = v
            

def submission_parser(code, elements):
    tree = ast.parse(code)
    
    for element in elements:
        visitor = GenericFinder(element)
        visitor.visit(tree)
        for node in visitor.found:
            elements[element].append(node.lineno)

