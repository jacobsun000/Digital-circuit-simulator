from typing import *
from Pin import InputPin, OutputPin, ConstantPin
from Part import Part, Nand
from copy import deepcopy
from re import sub


def read_from_file(filename, part_dict: Dict[str, Part]):
    # Initialize variables
    result = Part(filename.split('.')[0])
    result_dict = {}

    # Read lines from file
    with open(filename) as f:
        lines = f.read()
        lines = lines.replace('\n', ' ')
        lines = sub(' +', ' ', lines).split(';')

    # Convert lines into a dict
    for line in lines:
        if line == '':
            continue
        structure, content = line.split(':')
        result_dict[structure.strip()] = content.strip().split(',')

    # Handling Input pins
    inputs = []
    for pin in result_dict['Inputs']:
        inputs.append(InputPin(pin))

    # Handling Output pins
    outputs = []
    for pin in result_dict['Outputs']:
        outputs.append(OutputPin(pin))

    # Handling Parts
    parts = []
    for part_declearation in result_dict['Parts']:
        name, part_name = part_declearation.split(' ')
        part = deepcopy(part_dict[part_name])
        part.name = name
        parts.append(part)

    # Handling Wires
    for wire in result_dict['Wires']:
        wire = wire.split('->')
        wire = [i.strip() for i in wire]

        # Get pin object of wire[0] to wire[1]
        for i in range(len(wire)):
            pin = wire[i]
            if pin.isdigit():  # Is a constant pin
                cur_pin = ConstantPin()
                cur_pin.set_value(pin != '0')
                wire[i] = cur_pin
            elif '.' in pin:  # Is a pin from another part
                part, pin = pin.split('.')
                for cur_part in parts:
                    if cur_part.name == part:
                        part = cur_part
                        break
                for cur_pin in part.inputs + part.outputs:
                    if cur_pin.name == pin:
                        wire[i] = cur_pin
                        break
            else:  # Is a pin of direct input
                for cur_pin in inputs + outputs:
                    if cur_pin.name == pin:
                        wire[i] = cur_pin
        wire[0].connect(wire[1])

    # Finally, initialize this part
    result.inputs = inputs
    result.outputs = outputs
    result.parts = parts
    part_dict[result.part_name] = result


def main():
    part_dict: Dict[str, Part] = {}
    part_dict["NAND"] = Nand()
    read_from_file("NOT.dc", part_dict)
    print(part_dict)
    print(part_dict['NOT'].get_num_transistors())


main()
