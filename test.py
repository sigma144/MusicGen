from midi import create_MIDI
import music
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import Music, Track, Note
import random
import accomp
import melodygen

#Chords + Bass
testmusic = Music(tempo = 90)
testtrack = Track(instrument = 49)
chords = []
for i in range(50):
    chord = [Note(n, i*4, 4) for n in testmusic.get_scale_chord(random.randrange(14) + 12, inversion=random.randrange(3))]
    chords.append(chord)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
melodytrack = Track(instrument = 73)
melodytrack.notes = melodygen.melody_from_chords(testmusic, chords)
testmusic.tracks.append(melodytrack)
create_MIDI(testmusic, 'melody.mid')


