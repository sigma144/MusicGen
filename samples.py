from music import A, MIDDLE_A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE, DOMINANT, DIMINISHED, AUGMENTED, SUSPENDED, MAJOR, MINOR
from music import Music, Track, Note
import random

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

    # # generates random chord progressions
    # def chord_prog_generator_rand():

    #     testmusic = Music()
    #     testtrack = Track(instrument = 0)
    #     duration = 3
    #     numChords = 4
    #     chords = []

    #     for i in range(numChords):
    #         for n in testmusic.get_chord(random.randrange(50, 70), quality=random.choice([MINOR, MAJOR, DIMINISHED, AUGMENTED, SUSPENDED]),
    #             inversion=random.randrange(4), seventh=random.choice([None, None, DOMINANT, MAJOR, DIMINISHED])):
    #             testtrack.notes.append(Note(n, i*duration, duration))
    #             chords.append(n)
    #     testmusic.tracks.append(testtrack)

    #     return testmusic, chords

    # generates chord progressions in the same scale
    # Returns list[list[int]]
    def chord_prog_generator_scale(self, progKey = C, numChords = 4):

        testmusic = Music(key=progKey)
        chord = []
        chords = []

        for _ in range(numChords):
            for note in testmusic.get_scale_chord(random.randrange(7)-6,
                inversion=random.randrange(4)):
                #inversion=random.randrange(4), seventh=random.choice([None, None, DOMINANT, MAJOR, DIMINISHED])):
                chord.append(note)
            chords.append(chord)
            chord = []

        return chords

    def get_chords_from_prog(self, chords, duration = 4, repetitions = 1):
        nchords = []
        time = 0
        for c in chords * repetitions:
            chord = []
            for pitch in c:
                chord.append(Note(pitch, time, duration))
            time += duration
            nchords.append(chord)
        return nchords
