class Message:
    def __init__(self, id,targetId, objectType, coordinates, timestamp, scenario= None):
        self.SourceId = id
        self.TargetId = targetId
        self.ObjectType = objectType
        self.Coordinates = coordinates
        self.Scenario = scenario
        self.Timestamp = timestamp

class Coordinates:
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z