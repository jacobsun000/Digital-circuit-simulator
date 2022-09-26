from typing import *
from Pin import InputPin, OutputPin


class Part:
    def __init__(self, part_name: str, description=""):
        self.part_name = part_name
        self.description = description
        self.name = ""
        self.inputs: List[InputPin] = []
        self.outputs: List[OutputPin] = []
        self.parts: List[Part] = []
        self.n_transistor = -1

    def __repr__(self):
        return self.part_name

    def __eq__(self, o):
        return self.__hash__() == o.__hash__()

    def __hash__(self):
        return self.part_name.__hash__()

    def get_input_pin_names(self) -> List[str]:
        return [pin.name for pin in self.inputs]

    def get_output_pin_names(self) -> List[str]:
        return [pin.name for pin in self.outputs]

    def get_input_pin_values(self) -> List[bool]:
        return [pin.value for pin in self.inputs]

    def get_output_pin_values(self) -> List[bool]:
        return [pin.value for pin in self.outputs]

    def set_input_pin_values(self, values: List[bool]):
        if len(values) != len(self.inputs):
            return
        for i in range(len(values)):
            self.inputs[i].set_value(values[i])

    def get_num_transistors(self):
        if self.n_transistor != -1:
            return self.n_transistor
        result = 0
        for part in self.parts:
            result += part.get_num_transistors()
        return result


class Nand(Part):
    def __init__(self):
        Part.__init__(self, "NAND")
        self.description = "The NAND gate (short for Not-And) has two inputs \
            and one output. If both inputs are 1, the output is 0. Otherwise \
                the output is 1. \nThe NAND gate is the most basic element. It\
                     can be used to build _all_ other elements."
        self.inputs = [InputPin("in1"), InputPin("in2")]
        self.outputs = [OutputPin("out")]
        self.n_transistor = 1
