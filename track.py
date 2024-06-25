class Track:
    def __init__(self,times, volume, pitch):
        self.times = times
        self.volume = volume
        self.pitch = pitch

    def __str__(self):
        return f"Pitch: {self.pitch}, Times:{self.times}"