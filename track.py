class Track:
    def __init__(self,times, volume, panning, pitch):
        self.times = times
        self.volume = volume
        self.panning = panning
        self.pitch = pitch

    def __str__(self):
        return f"Pitch: {self.pitch}, Times:{self.times}, Volume: {self.volume}, Panning: {self.panning}"