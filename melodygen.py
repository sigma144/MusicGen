from copy import copy
from midi import create_MIDI
import music
from music import Music, Track, Note, OCTAVE
import random
import rhythmgen

def melody_from_chords(chords, **config):
    floor, ceiling = config['range'] if 'range' in config else [60, 72]
    notes = [copy(n) for c in chords for n in c]
    notes = put_in_range(notes, floor, ceiling)
    current_note = random.choice(notes)
    for c in chords:
        beats = c[0].duration
        for t in range(beats/2):
            pass
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