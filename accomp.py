from copy import copy
from midi import create_MIDI
import music
from music import Music, Track, Note, OCTAVE
import random
import rhythmgen

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
        rhythm  = rhythmgen.generate_rhythm(beats = chords[0][0].duration * 2)
        notes = []
        for c in chords:
            for b in rhythm:
                for n in chord_notes:
                    notes.append(Note(n.pitch, b, 1/2))
                if b >= chord_notes[0].duration:
                    break
    elif style == ARPEGGIO:
        chord_notes = accomp_from_chords(instrument, chords, CHORDS)
        floor, ceiling = config['range'] if 'range' in config else [60, 80]
        notes = []
        time = 0
        for c in chords:
            chord_notes = [n.pitch % OCTAVE for n in c]
            in_range = [i for i in range(floor, ceiling+1) if i % 12 in chord_notes]
            pattern = []
            for i in range(c[0].duration * 2):
                pattern.append(random.choice([n for n in in_range if len(pattern) == 0 or n != pattern[i-1]]))
            notes += [Note(n, i/2 + time, 1) for i,n in enumerate(pattern)]
            time += c[0].duration
    elif style == RHYTHMIC_BASS:
        chord_notes = accomp_from_chords(instrument, chords, BASS)
        rhythm  = rhythmgen.generate_rhythm(beats = chords[0][0].duration * 2)
        notes = []
        for c in chords:
            for b in rhythm:
                notes.append(Note(c[0].pitch, b, 1/2))
                if b >= chord_notes[0].duration:
                    break
    else: raise Exception(f"Unknown style {style}")
    return notes

    



