class Source:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Source({self.name!r})'

class Constant:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Constant({self.value!r})'