from midi import create_MIDI
import music
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import Music, Track, Note
import random
import accomp

#Arpeggio + Bass
testmusic = Music(tempo = 85)
testtrack = Track(instrument = 49)
chords = []
for i in range(50):
    chord = [Note(n, i*4, 4) for n in testmusic.get_scale_chord(random.randrange(14) + 12, inversion=random.randrange(3))]
    chords.append(chord)
testtrack.notes = accomp.accomp_from_chords(49, chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
arptrack = Track(instrument = 46)
arptrack.notes = accomp.accomp_from_chords(46, chords, style=accomp.ARPEGGIO)
testmusic.tracks.append(arptrack)
backingtrack = Track(instrument = 42)
backingtrack.notes = accomp.accomp_from_chords(42, chords, style=accomp.BASS)
testmusic.tracks.append(backingtrack)
create_MIDI(testmusic, 'arpeggio.mid')

