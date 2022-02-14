from copy import copy
from midi import create_MIDI
import music
from music import Music, Track, Note, OCTAVE
import random
import rhythmgen

BASS = 0; CHORDS = 1; ARPEGGIO = 2; RHYTHMIC = 3; RHYTHMIC_BASS = 4
def accomp_from_chords(chords, style=CHORDS, meter=rhythmgen.SIMPLE, **config):
    if style == BASS:
        floor = config['floor'] if 'floor' in config else 40
        notes = [put_in_range(Note(c[0].pitch, c[0].time, c[0].duration), floor, floor+12) for c in chords]
    elif style == CHORDS:
        floor, ceiling = config['range'] if 'range' in config else [60, 72]
        notes = [copy(n) for c in chords for n in c]
        notes = put_in_range(notes, floor, ceiling)
    elif style == RHYTHMIC:
        floor, ceiling = config['range'] if 'range' in config else [60, 72]
        rhythm  = [n.time for n in rhythmgen.generate_random_rhythm(beats = chords[0][0].duration * 2)]
        notes = []
        time = 0
        for c in chords:
            c = put_in_range(c, floor, ceiling)
            for b in rhythm:
                if b >= c[0].duration:
                    break
                for n in c:
                    notes.append(Note(n.pitch, b + time, 1/2))
            time += c[0].duration
    elif style == ARPEGGIO:
        floor, ceiling = config['range'] if 'range' in config else [60, 80]
        notes = []
        time = 0
        for c in chords:
            chord_notes = [n.pitch % OCTAVE for n in c]
            in_range = [i for i in range(floor, ceiling+1) if i % 12 in chord_notes]
            pattern = []
            for i in range(c[0].duration * (3 if meter == rhythmgen.COMPOUND else 2)):
                pattern.append(random.choice([n for n in in_range if len(pattern) == 0 or n != pattern[i-1]]))
            if meter == rhythmgen.COMPOUND:
                notes += [Note(n, i/3 + time, 1) for i,n in enumerate(pattern)]
            else:
                notes += [Note(n, i/2 + time, 1) for i,n in enumerate(pattern)]
            time += c[0].duration
    elif style == RHYTHMIC_BASS:
        floor, ceiling = config['range'] if 'range' in config else [40, 52]
        rhythm  = [n.time for n in rhythmgen.generate_random_rhythm(beats = chords[0][0].duration * 2, meter=meter)]
        notes = []
        time = 0
        for c in chords:
            for b in rhythm:
                if b >= c[0].duration:
                    break
                notes.append(put_in_range(Note(c[0].pitch, b + time, 1/2), floor, ceiling))
            time += c[0].duration
    else: raise Exception(f"Unknown style {style}")
    return notes

def put_in_range(notes, floor, ceiling):
    if isinstance(notes, Note):
        return put_in_range([notes], floor, ceiling)[0]
    notes = [copy(n) for n in notes]
    for n in notes:
        if n.pitch < floor:
            n.pitch += OCTAVE * ((floor - n.pitch) // OCTAVE + 1)
        if n.pitch > ceiling:
            n.pitch -= OCTAVE * ((n.pitch - ceiling) // OCTAVE + 1)
    return notes