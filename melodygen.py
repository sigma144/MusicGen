from copy import copy
from midi import create_MIDI
import music
from music import Music, Track, Note, OCTAVE
from numpy import random as nrandom
import random
from rhythmgen import SIMPLE, COMPOUND

def check_clash(chord, pitch):
    if any([(n.pitch - pitch) % 12 == 0 for n in chord]):
        return 0
    if any([abs(n.pitch - pitch) % 12 == 1 for n in chord]):
        return 1
    if any([abs(n.pitch - pitch) % 12 == 2 for n in chord]):
        return 2
    return 0

def melody_from_chords(music, chords, meter=SIMPLE, **config):
    floor, ceiling = config['range'] if 'range' in config else [60, 72]
    chord_notes = [copy(n) for c in chords for n in c]
    chord_notes = put_in_range(chord_notes, floor, ceiling)
    prev_deg = random.choice([-3, 0, 2])
    notes = []
    time = 0
    phrasetime = 0
    duration = 0
    for chord in chords:
        beats = chord[0].duration
        ptime = 0
        PHRASE_LEN = 7
        while ptime < beats:
            if duration > 0.5 and phrasetime > nrandom.normal(PHRASE_LEN, 1):
                duration = random.choice([0.5, min(1, beats-ptime), min(1.5, beats-ptime)])
                ptime += duration
                phrasetime -= PHRASE_LEN
                continue
            pitch = 1000000 # To trigger while loop
            while pitch < floor or pitch > ceiling or \
            check_clash(chord, pitch) == 1 and random.randrange(4) <= 3 or \
            check_clash(chord, pitch) == 2 and random.randrange(2) == 0 or \
            prev_deg == scale_deg and random.randrange(3) <= 1:  #Reduce repetition
                scale_deg = round(nrandom.normal(prev_deg, 2))
                pitch = music.get_scale_note(scale_deg)
                for n in chord:
                    if not music.is_in_scale(n.pitch) and abs(n.pitch - pitch) % 12 in [1, 11]:
                        pitch = n.pitch
                        break
            duration = random.choice([0.5, min(1, beats-ptime), min(1.5, beats-ptime)])
            if meter == COMPOUND and int(ptime) != ptime and ptime+time > 1/2:
                notes.append(Note(pitch, ptime + time - 1/2 + 2/3, duration))
            else:
                notes.append(Note(pitch, ptime + time, duration))
            ptime += duration
            phrasetime += duration
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