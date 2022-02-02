from midi import create_MIDI
import music
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import Music, Track, Note
import random

#Chaos Chords
testmusic = Music()
testtrack = Track(instrument = 89)
for _ in range(3):
    for i in range(30):
        testtrack.notes.append(Note(random.randrange(60 - music.OCTAVE, 60), i*10, 10))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'test.mid')
