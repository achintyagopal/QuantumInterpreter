from node import Node

class StatementsNode(Node):

    def __init__(self, statements):
        self.statements = []
        for statement in statements:
            self.statements.append(statement[0])

    def get_statements(self):
        return self.statements