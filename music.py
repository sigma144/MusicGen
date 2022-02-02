from fractions import Fraction
A = 0; As = Bb = 1; B = Cb = 2; C = Bs = 3; Cs = Db = 4; D = 5; Ds = Eb = 6; E = Fb = 7; F = Es = 8; Fs = Gb = 9; G = 10; Gs = Ab = 11; OCTAVE = 12
MINOR_MODE = A; MAJOR_MODE = C
MAJOR = [0, 4, 7]; MINOR = [0, 3, 7]; DOMINANT = MINOR; DIMINISHED = [0, 3, 6]; SUSPENDED = [0, 5, 7]; AUGMENTED = [0, 4, 8]
FLAT = -1; NATURAL = 0; SHARP = 1
MIDDLE_A = 57; MIDDLE_C = 60

class Note:
    def __init__(self, pitch, time, duration):
        self.pitch = pitch
        self.time: Fraction = time
        self.duration: Fraction = duration

class Track:
    def __init__(self, instrument = 0, notes = None):
        if notes is None: notes = []
        self.instrument = instrument; self.notes = notes

class Music:
    def __init__(self, tempo = 100, key = C, mode = MAJOR_MODE, scale = None):
        self.tempo = tempo; self.key = key; self.tracks = []
        if scale is None:
            scale = [A, B, C, D, E, F, G]
            mode_index = scale.index(mode)
            scale = [n - mode for n in scale[mode_index:]] + [n - mode + OCTAVE for n in scale[:mode_index]]
            scale = [n + self.key + MIDDLE_A for n in scale]
        else:
            scale = [n - scale[0] + key + MIDDLE_A for n in scale]
            for i in range(1, len(scale)):
                if scale[i] < scale[i-1]:
                    scale[i] += OCTAVE
        self.scale = scale
    def get_scale_note(self, scale_degree):
        return self.scale[scale_degree % 7] + (scale_degree // 7) * OCTAVE
    def get_scale_chord(self, root_scale_degree, inversion = 0, seventh = None):
        chord = [self.get_scale_note(root_scale_degree), self.get_scale_note(root_scale_degree + 2), self.get_scale_note(root_scale_degree + 4)]
        if seventh == MAJOR: chord.append(chord[0] + 11)
        elif seventh == DOMINANT: chord.append(chord[0] + 10)
        elif seventh == DIMINISHED: chord.append(chord[0] + 9)
        for _ in range(inversion):
            chord.append(chord.pop(0) + OCTAVE)
        return chord
    def get_chord(self, root_note, quality = None, inversion = 0, seventh = None):
        if not isinstance(quality, list): raise Exception(f"Unknown chord quality {quality}")
        chord = [n + root_note for n in quality]
        if seventh == MAJOR: chord.append(root_note + 11)
        elif seventh == DOMINANT: chord.append(root_note + 10)
        elif seventh == DIMINISHED: chord.append(root_note + 9)
        elif not (seventh is None): raise Exception(f"Unknown seventh: {seventh}")
        for _ in range(inversion):
            chord.append(chord.pop(0) + OCTAVE)
        return chord



