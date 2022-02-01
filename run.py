from midi import create_MIDI
import music
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import Music, Track, Note
import random

#Test
testmusic = Music(key = D)
testtrack = Track()
for i in range(8):
    testtrack.notes.append(Note(testmusic.get_scale_note(i), i, 1))
    #print(testmusic.get_scale_note(i))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'test.mid')

#Multi-track
testmusic = Music()
testtrack = Track()
for i in range(50):
    testtrack.notes.append(Note(random.randrange(40, 80), i, 1))
testmusic.tracks.append(testtrack)
testtrack2 = Track(instrument = 19)
for i in range(50):
    testtrack2.notes.append(Note(random.randrange(40, 80), i, 1))
testmusic.tracks.append(testtrack2)
create_MIDI(testmusic, 'multi.mid')

#Chaos
testmusic = Music()
testtrack = Track()
for _ in range(2):
    for i in range(50):
        testtrack.notes.append(Note(random.randrange(40, 80), i/2, 1/2))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'chaos.mid')

#Scale
testmusic = Music()
testtrack = Track()
for i in range(50):
    duration = random.randrange(4) + 1
    time = random.randrange(3) + 1
    testtrack.notes.append(Note(testmusic.get_scale_note(random.randrange(0, 20)), i*time, 2/duration))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'scale.mid')

#Chaos Chords
testmusic = Music()
testtrack = Track(instrument = 19)
for _ in range(3):
    for i in range(20):
        testtrack.notes.append(Note(random.randrange(40, 80), i*3, 3))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'chordc.mid')

#Scale Chords
testmusic = Music()
testtrack = Track(instrument = 19)
for _ in range(3):
    for i in range(20):
        testtrack.notes.append(Note(testmusic.get_scale_note(random.randrange(0, 20)), i*3, 3))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'chords.mid')

#Triads
testmusic = Music()
testtrack = Track(instrument = 0)
for i in range(20):
    for n in testmusic.get_scale_chord(random.randrange(7), inversion=random.randrange(3)):
        testtrack.notes.append(Note(n, i*3, 3))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'triads.mid')
