from abc import ABC

class Color(ABC):
    def __init__(self, name, rgb, id):
        self.name = name
        self.rgb = rgb
        self.id = id

class Hidden(Color):
    def __init__(self):
        super().__init__("Hidden", (40, 40, 40), -1)

class NC(Color):
    def __init__(self):
        super().__init__("NC", (255, 255, 255), 0)

class Red(Color):
    def __init__(self):
        super().__init__("Red", (255, 0, 0), 1)

class Orange(Color):
    def __init__(self):
        super().__init__("Orange", (255, 165, 0), 2)

class Yellow(Color):
    def __init__(self):
        super().__init__("Yellow", (255, 255, 0), 3)

class Green(Color):
    def __init__(self):
        super().__init__("Green", (0, 255, 0), 4)

class Blue(Color):
    def __init__(self):
        super().__init__("Blue", (0, 0, 255), 5)

class Pink(Color):
    def __init__(self):
        super().__init__("Pink", (255, 192, 203), 6)

class Violet(Color):
    def __init__(self):
        super().__init__("Violet", (138, 43, 226), 7)

class Cyan(Color):
    def __init__(self):
        super().__init__("Cyan", (0, 255, 255), 8)

class Coral(Color):
    def __init__(self):
        super().__init__("Coral", (255, 127, 80), 10)

class Teal(Color):
    def __init__(self):
        super().__init__("Teal", (0, 128, 128), 11)