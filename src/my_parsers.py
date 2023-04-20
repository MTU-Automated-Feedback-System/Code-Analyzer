import ast

class StatementFinder(ast.NodeVisitor):
    def __init__(self, stmt_type):
        self.stmt_type = stmt_type
        self.found = []

    def generic_visit(self, node):
        if node.__class__.__name__ == self.stmt_type:
            self.found.append(node)
        super().generic_visit(node)


class ExpressionFinder(ast.NodeVisitor):
    def __init__(self, expr_type):
        self.expr_type = expr_type
        self.found = []

    def generic_visit(self, node):
        if node.__class__.__name__ == self.expr_type:
            self.found.append(node)
        super().generic_visit(node)

