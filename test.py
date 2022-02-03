from midi import create_MIDI
import music
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import Music, Track, Note
import random
import accomp

#Chords + Bass
testmusic = Music()
testtrack = Track(instrument = 89)
chords = []
for i in range(50):
    chord = [Note(n, i*5, 5) for n in testmusic.get_scale_chord(random.randrange(7) - 6, inversion=random.randrange(3))]
    chords.append(chord)
    testtrack.notes += chord
testmusic.tracks.append(testtrack)
backingtrack = Track(instrument = 42)
backingtrack.notes = accomp.accomp_from_chords(42, chords, style=accomp.BASS)
testmusic.tracks.append(backingtrack)

create_MIDI(testmusic, 'bass.mid')

