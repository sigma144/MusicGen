from midi import create_MIDI
import music
from music import Music, Track, Note
import random

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
testtrack = Track(instrument = 4)
for _ in range(2):
    for i in range(50):
        testtrack.notes.append(Note(testmusic.get_scale_note(random.randrange(0, 20)), i, 1))
    testmusic.tracks.append(testtrack)
    create_MIDI(testmusic, 'scale.mid')
