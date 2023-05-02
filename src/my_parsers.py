import ast

class GenericFinder(ast.NodeVisitor):
    def __init__(self, node_type):
        self.node_type = node_type
        self.found = []

    def generic_visit(self, node):
        if node.__class__.__name__ == self.node_type:
            self.found.append(node)
        super().generic_visit(node)

class RecursionDetector(ast.NodeVisitor):
    def __init__(self):
        self.function_name = None
        self.recursive = False

    def visit_FunctionDef(self, node):
        if self.function_name is None:
            self.function_name = node.name
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.function_name:
            self.recursive = True
        self.generic_visit(node)



def get_all_methods(locals_dict: dict):
    # From a given dictionnary, return the list of functions from a piece of code
    dunder = ["__builtins__"]  # Could be replaced by dictionnary if list grows
    functions = {}
    for k, v in locals_dict.items():
        if k not in dunder and isinstance(v, function):
            functions[k] = v
            

def submission_parser(code, elements):
    tree = ast.parse(code)
    
    for i, element in enumerate(elements):
        node_type = element["name"]
        visitor = GenericFinder(node_type)
        visitor.visit(tree)
        for node in visitor.found:
            elements[i]["occurences"].append(node.lineno)

