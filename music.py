from fractions import Fraction

class Note:
    def __init__(self, start, duration):
        self.duration: Fraction = duration; self.start: Fraction = start

class Measure:
    def __init__(self):
        self.tracks: list[Note] = []

class Music:
    def __init__(self):
        self.tracks: list[Measure] = []
        self.tempo = 100
    
