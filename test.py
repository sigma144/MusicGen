from midi import create_MIDI
import music
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import Music, Track, Note
import random
import accomp

#Rhythmic Chords + Bass
testmusic = Music()
testtrack = Track(instrument = 30)
chords = []
for i in range(50):
    chord = [Note(n, i*4, 4) for n in testmusic.get_scale_chord(random.randrange(14) + 12, inversion=random.randrange(3))]
    chords.append(chord)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC)
testmusic.tracks.append(testtrack)
basstrack = Track(instrument = 39)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC_BASS)
testmusic.tracks.append(basstrack)
create_MIDI(testmusic, 'rhythmic.mid')


