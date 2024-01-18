from abc import ABC

class Global:
    def __init__(self, value=0):
        self.value = value

class Color(ABC):
    def __init__(self, rgb, encoding):
        self.rgb = rgb
        self.encoding = encoding

class Hidden(Color):
    def __init__(self):
        super().__init__((40, 40, 40), None)

class NC(Color):
    def __init__(self):
        super().__init__((255, 255, 255), None)

class Red(Color):
    def __init__(self):
        super().__init__((255, 0, 0), None)

class Orange(Color):
    def __init__(self):
        super().__init__((255, 165, 0), None)

class Yellow(Color):
    def __init__(self):
        super().__init__((255, 255, 0), None)

class Green(Color):
    def __init__(self):
        super().__init__((0, 255, 0), None)

class Blue(Color):
    def __init__(self):
        super().__init__((0, 0, 255), None)

class Pink(Color):
    def __init__(self):
        super().__init__((255, 192, 203), None)

class Violet(Color):
    def __init__(self):
        super().__init__((138, 43, 226), None)

class Cyan(Color):
    def __init__(self):
        super().__init__((0, 255, 255), None)

class Coral(Color):
    def __init__(self):
        super().__init__((255, 127, 80), None)

class Teal(Color):
    def __init__(self):
        super().__init__((0, 128, 128), None)