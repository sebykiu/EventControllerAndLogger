class Message:
    def __init__(self, id, instruction, coordinates, timestamp, scenario= None):
        self.Id = id
        self.Instruction = instruction
        self.Coordinates = coordinates
        self.Scenario = scenario
        self.Timestamp = timestamp

class Coordinates:
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z