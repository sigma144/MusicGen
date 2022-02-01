from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE, DOMINANT
from music import Music, Track, Note
import random

class Samples():

    def sample1():
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
    def sample2():
        sample = Music(key = C, tempo = 150)
        testtrack = Track(instrument = 0)
        duration = 4

        chords = []
        chords.append(sample.get_scale_chord(A))
        chords.append(sample.get_scale_chord(A, seventh=DOMINANT))
        for i, chord in enumerate(chords):
            for j in range(len(chords)):
                testtrack.notes.append(Note(chord[j], i, duration))
        
        sample.tracks.append(testtrack)
        return sample


    # C chord split
    def sample3():
        sample = Music(key = C, tempo = 150)
        testtrack = Track(instrument = 0)
        duration = 4

        chord = sample.get_scale_chord(C)
        for _ in range(3):
            for i, note in enumerate(chord):
                testtrack.notes.append(Note(note, i*duration, duration))
        
        sample.tracks.append(testtrack)
        return sample

