# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

#Clase base para los nodos del árbol de comportamiento.
#Todos los tipos denodos heredan de esta clase.
class Node:
    def run(self):
        raise NotImplementedError


class Selector(Node):
    def __init__(self, children):
        self.children = children

    def run(self):
        for child in self.children:
            if child.run():
                return True
        return False


class Sequence(Node):
    def __init__(self, children):
        self.children = children

    def run(self):
        for child in self.children:
            if not child.run():
                return False
        return True


class Condition(Node):
    def __init__(self, func):
        self.func = func

    def run(self):
        return self.func()


class Action(Node):
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()
        return True