from accomp import accomp_from_chords
from midi import create_MIDI
from music import A, MIDDLE_A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE, DOMINANT, DIMINISHED, AUGMENTED, SUSPENDED, MAJOR, MINOR, MAJOR_MODE, MINOR_MODE
from music import Music, Track, Note
import random
import time
import accomp
import melodygen

class Samples():

    def chord_prog_generator_scale(self, progKey = C, numChords = 4, match_prob = 0):
        testmusic = Music(key=progKey)
        testmusic.set_scale(MAJOR_MODE)
        chord = []
        chords = []
        choices = []
        suspended = 0
        last_chord = []
        for i in range(numChords):
            choices = random.choice([
                [1, 1, 1, 2, 3, 4, 4, 5, 5, 6, 6], #Major
                [1, 1, 2, 3, 4, 4, 5, 5, 6, 6, 6] #Minor
            ])
            scale_degree = random.choice(choices) 
            if suspended:
                chord = chord = testmusic.get_scale_chord(suspended,
                    inversion=random.choice([0, 0, 0, 1, 2, 3]), seventh=None)
                suspended = 0
            elif i % 2 == 1 and random.random() < match_prob:
                chord = last_chord[:]
            elif i+1 < numChords and random.randrange(3) == 0:
                chord = testmusic.get_chord(testmusic.get_scale_note(scale_degree), SUSPENDED,
                    inversion=random.choice([0, 0, 0, 1, 2, 3]), seventh=None)
                suspended = random.choice([scale_degree, scale_degree, (scale_degree + 2) % 7 + 1])
                if scale_degree == 4: suspended = scale_degree
            else:
                chord = testmusic.get_scale_chord(scale_degree,
                    inversion=random.choice([0, 0, 0, 1, 2, 3]),
                    seventh=None)#random.choice([None, None, DOMINANT, MAJOR, DIMINISHED]))
            chords.append(chord)
            last_chord = chord
        return chords

    def chord_prog_generator_borrowed(self, progKey = C, numChords = 4, match_prob = 0):
        testmusic = Music(key=progKey)
        testmusic.set_scale(MINOR_MODE)
        chord = []
        chords = []
        choices = []
        suspended = 0
        last_chord = []
        for i in range(numChords):
            choices = [1, 1, 3, 4, 6, 7]
            scale_degree = random.choice(choices)
            if suspended:
                chord = testmusic.get_chord(testmusic.get_scale_note(suspended), MAJOR,
                    inversion=random.choice([0, 0, 0, 1, 2, 3]), seventh=None)
                suspended = 0
            elif i % 2 == 1 and random.random() < match_prob:
                chord = last_chord[:]
            elif i+1 < numChords and scale_degree in [1, 4, 7] and random.randrange(3) == 0:
                chord = testmusic.get_chord(testmusic.get_scale_note(scale_degree), SUSPENDED,
                    inversion=random.choice([0, 0, 0, 1, 2, 3]), seventh=None)
                suspended = random.choice([scale_degree, scale_degree, (scale_degree + 2) % 7 + 1])
                if scale_degree == 4: suspended = scale_degree
            else:
                chord = testmusic.get_chord(testmusic.get_scale_note(scale_degree), MAJOR,
                inversion=random.choice([0, 0, 0, 1, 2, 3]), seventh=None)
            chords.append(chord)
            last_chord = chord
        return chords

    def get_chords_from_prog(self, chords, duration = 4, repetitions = 1):
        nchords = []
        time = 0
        if type(duration) == int:
            duration = [duration]
        for i, c in enumerate(chords * repetitions):
            chord = []
            for pitch in c:
                chord.append(Note(pitch, time, duration[i % len(duration)]))
            time += duration[i % len(duration)]
            nchords.append(chord)
        return nchords

    def merge_chords_from_progs(self, chord_prog_list, section_length):
        split_point = random.choice([0.25, 0.5, 0.75])
        prog1 = random.choice(chord_prog_list)
        prog2 = random.choice(chord_prog_list)
        newprog = []
        for c in prog1:
            if c[0].time + 0.00001 < split_point * section_length:
                newprog.append(c)
        for c in prog2:
            if c[0].time + 0.00001 >= split_point * section_length:
                newprog.append(c)
        return newprog

if __name__ == "__main__":
    #New Chord Generator
    testmusic = Music(tempo = 100)
    testtrack = Track(instrument = 49)
    #chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=32), duration=4, repetitions=1)
    chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_borrowed(progKey=testmusic.key, numChords=32), duration=4, repetitions=1)
    testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
    testmusic.tracks.append(testtrack)
    arptrack = Track(instrument = 46)
    arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
    testmusic.tracks.append(arptrack)
    basstrack = Track(instrument = 42)
    basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
    testmusic.tracks.append(basstrack)
    melodytrack = Track(instrument = 73)
    melodytrack.notes = melodygen.melody_from_chords(testmusic, chords)
    testmusic.tracks.append(melodytrack)
    create_MIDI(testmusic, 'chordgen.mid')