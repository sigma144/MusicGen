A = 0; As = Bb = 1; B = Cb = 2; C = Bs = 3; Cs = Db = 4; D = 5; Ds = Eb = 6; E = Fb = 7; F = Es = 8; Fs = Gb = 9; G = 10; Gs = Ab = 11; OCTAVE = 12
MINOR_MODE = A; MAJOR_MODE = C
MAJOR = [0, 4, 7]; MINOR = [0, 3, 7]; DOMINANT = MINOR; DIMINISHED = [0, 3, 6]; SUSPENDED = [0, 5, 7]; AUGMENTED = [0, 4, 8]
FLAT = -1; NATURAL = 0; SHARP = 1
MIDDLE_A = 57; MIDDLE_C = 60
from chorddist import CHORD_DIST_MAJOR, CHORD_DIST_MINOR
import random

class Note:
    '''Create a music note to add to a Track object.
    pitch(int): The MIDI pitch of the note (MIDDLE_C = 60 as shown above)
    time(float): The beat number on which the note occurs (fractions for offbeats)
    duration(float): How many beats the note lasts for'''
    def __init__(self, pitch, time, duration):
        self.pitch = pitch
        self.time: float = time
        self.duration: float = duration
    def __repr__(self):
        return f"{self.pitch} {self.time} {self.duration}"

class Track:
    '''Create a music track that has notes and an instrument type. It must be added to a Music object to be played.
    instrument(int): The instrument for this track (see instruments.txt for instrument numbers)
    notes(list[Note]): An optional list of Notes to initialize the track with'''
    def __init__(self, instrument = 0, notes = None, drum_kit = False):
        if notes is None: notes = []
        self.instrument = instrument; self.notes = notes; self.drum_kit = drum_kit
    '''Add a note to the track. Same function signature as the Note constructor.'''
    def add_note(self, pitch, time, duration):
        self.notes.append(Note(pitch, time, duration))

class Music:
    '''Create a new piece of music to be turned into MIDI.
    tempo(int) = 100: BPM of the song
    key(int) = C: Key of the song, used to generate scale. Pass in a note letter such as A or Bb
    mode_or_scale(int or list[int]) = MAJOR_MODE: Mode/scale of the song. Pass in a note letter for the mode or a list[int] scale.'''
    def __init__(self, tempo = 100, key = C, mode_or_scale = MAJOR_MODE):
        self.tempo = tempo; self.key = key; self.tracks = []
        self.set_scale(mode_or_scale)
    '''Sets the scale of the song while shifting it to match the current musical key.
    mode_or_scale(int or list[int]): New mode/scale of the song. Pass in a note letter for the mode or a list[int] scale.'''
    def set_scale(self, mode_or_scale):
        if isinstance(mode_or_scale, list):
            scale = mode_or_scale
            scale = [n - scale[0] + self.key + MIDDLE_A for n in scale]
            for i in range(1, len(scale)):
                if scale[i] < scale[i-1]:
                    scale[i] += OCTAVE
        else:
            mode = mode_or_scale
            scale = [A, B, C, D, E, F, G]
            if mode not in scale:
                raise Exception(f"Unknown mode: {mode}")
            mode_index = scale.index(mode)
            scale = [n - mode for n in scale[mode_index:]] + [n - mode + OCTAVE for n in scale[:mode_index]]
            scale = [n + self.key + MIDDLE_A for n in scale]
        self.scale = scale
    '''Get a note within the song's current scale/mode/key.
    scale_degree(int): Note scale degree (1 for key note)'''
    def get_scale_note(self, scale_degree):
        note = self.scale[(abs(scale_degree) - 1) % len(self.scale)] + ((abs(scale_degree) - 1) // len(self.scale)) * OCTAVE
        if scale_degree < 0: note -= 1
        return note
    '''Get a triad/seventh (list[int]) within the song's current scale/mode/key.
    root_scale_degree(int): Root note scale degree (1 for key note)
    inversion(int) = 0: Chord inversion
    seventh(None or DOMINANT or MAJOR or DIMINISHED) = None: Optional seventh to add to the chord'''
    def get_scale_chord(self, root_scale_degree, inversion = 0, seventh = None):
        prev_scale = self.scale
        if root_scale_degree < 0: self.set_scale(MINOR_MODE)
        chord = [self.get_scale_note(root_scale_degree), self.get_scale_note(root_scale_degree + 2), self.get_scale_note(root_scale_degree + 4)]
        if root_scale_degree < 0: self.scale = prev_scale
        if seventh == MAJOR: chord.append(chord[0] + 11)
        elif seventh == DOMINANT: chord.append(chord[0] + 10)
        elif seventh == DIMINISHED: chord.append(chord[0] + 9)
        for _ in range(inversion):
            chord.append(chord.pop(0) + OCTAVE)
        return chord
    def get_following_chord_type(self, prev_degree, prev_quality):
        if prev_quality == MAJOR and prev_degree in CHORD_DIST_MAJOR:
            dist = CHORD_DIST_MAJOR[prev_degree]
        elif prev_quality == MINOR and prev_degree in CHORD_DIST_MINOR:
            dist = CHORD_DIST_MINOR[prev_degree]
        else:
            dist = CHORD_DIST_MAJOR[5]
        deg, qual, _ = self.choose_from_dist(dist, p=[t[2] for t in dist])
        return deg, qual
    '''Get a chord (list[int]) with the given root note and chord quality
    root_note(int): Root note of the chord
    quality(list[int]): Chord quality, such as MAJOR, MINOR, or SUSPENDED
    inversion(int) = 0: Chord inversion
    seventh(None or DOMINANT or MAJOR or DIMINISHED) = None: Optional seventh to add to the chord'''
    def get_chord(self, root_note, quality, inversion = 0, seventh = None):
        if not isinstance(quality, list): raise Exception(f"Unknown chord quality {quality}")
        chord = [n + root_note for n in quality]
        if seventh == MAJOR: chord.append(root_note + 11)
        elif seventh == DOMINANT: chord.append(root_note + 10)
        elif seventh == DIMINISHED: chord.append(root_note + 9)
        elif not (seventh is None): raise Exception(f"Unknown seventh: {seventh}")
        for _ in range(inversion):
            chord.append(chord.pop(0) + OCTAVE)
        return chord


    def choose_from_dist(self, choices, p):
        p = [n / sum(p) for n in p]
        r = random.random()
        for i, n in enumerate(p):
            r -= n
            if r <= 0: return choices[i]


