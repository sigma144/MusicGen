from copy import copy
from midi import create_MIDI
import music
from music import Music, Track, Note, OCTAVE
import random
import rhythm

BASS = 0; CHORDS = 1; ARPEGGIO = 2; RHYTHMIC = 3; RHYTHMIC_BASS = 4
def accomp_from_chords(instrument, chords, style=CHORDS, **config):
    add_octave = -OCTAVE if instrument in [32,33,34,35,36,37,38,39,43,58,70] else 0
    if style == BASS:
        floor = config['floor'] if 'floor' in config else 40
        notes = [Note(c[0].pitch % OCTAVE + floor - floor % OCTAVE, c[0].time, c[0].duration) for c in chords]
    elif style == CHORDS:
        floor, ceiling = config['range'] if 'range' in config else [60, 72]
        notes = [copy(n) for c in chords for n in c]
        for i,n in enumerate(notes):
            if n.pitch < floor:
                n.pitch += OCTAVE * ((floor - n.pitch) // OCTAVE + 1)
            if n.pitch > ceiling:
                n.pitch -= OCTAVE * ((n.pitch - ceiling) // OCTAVE + 1)
    elif style == RHYTHMIC:
        chord_notes = accomp_from_chords(instrument, chords, CHORDS)
        rhythms = rhythm.generate_rhythm(beats = 4)
        notes = []
        for nb in rhythms:
            for n in chord_notes:
                notes.append(Note(n.pitch, nb.time, nb.duration))
    else: raise Exception(f"Unknown style {style}")
    return notes

    



