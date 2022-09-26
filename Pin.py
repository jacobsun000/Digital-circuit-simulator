from typing import *


class Pin:
    def __init__(self, name: str):
        self.name = name
        self.connected_pins: List[Pin] = []
        self.value = False

    def __repr__(self):
        return self.name

    def connect(self, pin):
        self.connected_pins.append(pin)

    def set_value(self, value: bool, is_source: bool = True):
        if self.value == value:
            return

        self.value = value

        for pin in self.connected_pins:
            pin.set_value(value, False)


class InputPin(Pin):
    def __init__(self, name: str):
        Pin.__init__(self, name)


class OutputPin(Pin):
    def __init__(self, name: str):
        Pin.__init__(self, name)


class ConstantPin(Pin):
    def __init__(self):
        Pin.__init__(self, "const")

    def set_value(self, value):
        return
