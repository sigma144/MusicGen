from copy import copy
from midi import create_MIDI
import music
from music import Music, Track, Note, OCTAVE
from numpy import random

def melody_from_chords(music, chords, **config):
    floor, ceiling = config['range'] if 'range' in config else [60, 72]
    chord_notes = [copy(n) for c in chords for n in c]
    chord_notes = put_in_range(chord_notes, floor, ceiling)
    prev_deg = random.choice([-3, 0, 2])
    notes = []
    time = 0
    for c in chords:
        beats = c[0].duration
        ptime = 0
        while ptime < beats:
            pitch = 1000000
            while pitch < floor or pitch > ceiling:
                scale_deg = round(random.normal(prev_deg, 2))
                pitch = music.get_scale_note(scale_deg)
                #input(pitch)
            duration = random.choice([0.5, min(1, beats-ptime)])
            notes.append(Note(pitch, ptime + time, duration))
            ptime += duration
            prev_deg = scale_deg
        time += beats
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