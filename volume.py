import math

class Volume:
    def __init__(self,volume, panning):
        self.volume = volume
        self.panning = panning
        self.left = math.floor((-0.5*panning + 0.5) * volume)
        self.right = math.floor((0.5*panning + 0.5) * volume)

    def __str__(self):
        return f"Volume: {self.left}, {self.right}"