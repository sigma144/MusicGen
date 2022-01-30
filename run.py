from midi import create_MIDI
import music
from music import Music, Track, Note
import random

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
        testtrack.notes.append(Note(random.randrange(40, 80), i, 1))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'chaos.mid')

#Scale
testmusic = Music()
testtrack = Track()
for _ in range(2):
    for i in range(50):
        testtrack.notes.append(Note(testmusic.get_scale_note(random.randrange(0, 20)), i, 1))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'scale.mid')

#Chaos Chords
testmusic = Music()
testtrack = Track(instrument = 19)
for _ in range(3):
    for i in range(50):
        testtrack.notes.append(Note(random.randrange(40, 80), i*3, 3))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'chordc.mid')

#Scale Chords
testmusic = Music()
testtrack = Track(instrument = 19)
for _ in range(3):
    for i in range(50):
        testtrack.notes.append(Note(testmusic.get_scale_note(random.randrange(0, 20)), i*3, 3))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'chords.mid')