from fractions import Fraction

A = 0; As = Bb = 1; B = Cb = 2; C = Bs = 3; Cs = Db = 4; D = 5; Ds = Eb = 6; E = Fb = 7; F = Es = 8; Fs = Gb = 9; G = 10; Gs = Ab = 11; OCTAVE = 12
MINOR_MODE = A; MAJOR_MODE = C
MAJOR = [0, 4, 7]; MINOR = [0, 3, 7]; DOMINANT = MINOR; DIMINISHED = [0, 3, 6]; SUSPENDED = [0, 5, 7]; AUGMENTED = [0, 4, 8]
FLAT = -1; NATURAL = 0; SHARP = 1;

class Note:
    def __init__(self, pitch, time, duration) -> None:
        self.pitch: int = pitch
        self.time: Fraction = time
        self.duration: Fraction = duration

class Track:
    def __init__(self) -> None:
        self.instrument: int = None
        self.notes: list[Note] = []

class Music:
    def __init__(self) -> None:
        self.tracks: list[Track] = []
        self.tempo = 100
        self.key: int = C
        self.mode: int = MAJOR_MODE
    def get_scale(self, key: int = None, mode: int = None, scale: int = None) -> int:
        if key is None: key = self.key
        if mode is None: mode = self.mode
        if scale is None: scale = [A, B, C, D, E, F, G]
        #Establish mode
        mode_index = scale.index(mode)
        scale = [n - mode for n in scale[mode_index:]] + [n - mode + OCTAVE for n in scale[:mode_index]]
        #Shift by key
        scale = [n + key for n in scale]
        return scale
    def get_scale_note(self, scale_degree: int, key: int = None, mode: int = None, scale: int = None) -> int:
        scale = self.get_scale(key, mode, scale)
        return scale[scale_degree % 8] + (scale_degree // 8) * 8
    def get_scale_chord(self, root_scale_degree: int, key: int = None, mode: int = None, scale: int = None, inversion: int = 0, seventh: list[int] = None) -> int:
        scale = self.get_scale(key, mode, scale)
        #Finish
    def get_chord(self, root_note: int, quality: list[int] = None, inversion: int = 0, seventh: list[int] = None):
        if not (quality is list): raise Exception(f"Unknown chord quality {quality}")
        chord = [n + root_note for n in quality]
        if seventh == MAJOR: chord.append(root_note + 11)
        elif seventh == DOMINANT: chord.append(root_note + 10)
        elif seventh == DIMINISHED: chord.append(root_note + 9)
        else: raise Exception(f"Unknown seventh: {seventh}")
        for _ in range(inversion):
            chord.append(chord.pop(0) - OCTAVE)
        return chord
    def get_default_chord_quality(self, scale_degree: int, mode: int = None, scale: int = None) -> list[int]:
        chord =  [self.get_scale_note(scale_degree, 0, mode, scale),
            self.get_scale_note(scale_degree + 2, 0, mode, scale),
            self.get_scale_note(scale_degree + 4, 0, mode, scale)]
        return chord



