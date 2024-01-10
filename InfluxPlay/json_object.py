class Message:
    def __init__(self, id, target_id, object_type, coordinates, sim_time, scenario=None):
        self.SourceId = id
        self.TargetId = target_id
        self.ObjectType = object_type
        self.Coordinates = coordinates
        self.Scenario = scenario
        self.SimTime = sim_time


class Coordinates:
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z
