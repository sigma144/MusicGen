from music import A, MIDDLE_A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE, DOMINANT, DIMINISHED, AUGMENTED, SUSPENDED, MAJOR, MINOR, MAJOR_MODE, MINOR_MODE
from music import Music, Track, Note
import random
import time

class Samples():

    def sample1(self):
        sample = Music(key = E)
        testtrack = Track()
        time = 0
        for i in range(50):
            duration = random.choice([1, 1/2])
            if random.randrange(3) > 0:
                testtrack.notes.append(Note(sample.get_scale_note(random.randrange(-10, 10)), time, duration))
            time += duration
        sample.tracks.append(testtrack)
        # create_MIDI(testmusic, 'sample1.mid') ??
        return sample

    # C, Am, Dm, F chord progression
    def sample2(self):
        
        testmusic = Music(tempo=150)
        testtrack = Track(instrument = 0)

        chords = []
        chords.append(testmusic.get_chord(MIDDLE_A + C, quality=MAJOR))
        chords.append(testmusic.get_chord(MIDDLE_A + A, quality=MINOR))
        chords.append(testmusic.get_chord(MIDDLE_A + D, quality=MINOR))
        chords.append(testmusic.get_chord(MIDDLE_A + F, quality=MAJOR))
        
        for i, chord in enumerate(chords):
            for note in chord:
                testtrack.notes.append(Note(note, i*3, 3))
        testmusic.tracks.append(testtrack)

        return testmusic
    def chord_prog_generator_scale(self, progKey = C, numChords = 4):

        testmusic = Music(key=progKey)
        chord = []
        chords = []
        choices = []
        for _ in range(numChords):
            if random.randrange(4) == -1: #Disable for now
                testmusic.set_scale(MINOR_MODE)
                choices = [3, 6, 7]
            else:
                testmusic.set_scale(MAJOR_MODE)
                choices = [1, 2, 3, 4, 5, 6]
            chord = [0, 1, 2, 3] #Purposely out-of-scale chord to trigger the loop
            while not testmusic.is_in_scale(chord):
                chord = testmusic.get_scale_chord(random.choice(choices),
                inversion=random.choice([0, 0, 1, 2, 3]),
                seventh=None)#random.choice([None, None, DOMINANT, MAJOR, DIMINISHED]))
            chords.append(chord)
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
