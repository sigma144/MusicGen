from midi import create_MIDI
import music
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import Music, Track, Note
import random
import accomp
import rhythmgen
from rhythmgen import RhythmGen
from samples import Samples

#Arpeggio + Bass
testmusic = Music(tempo = 85)
testtrack = Track(instrument = 49)
chords = Samples().chord_prog_generator_scale(8) * 4
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
arptrack = Track(instrument = 46)
arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
testmusic.tracks.append(arptrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
create_MIDI(testmusic, 'chordgen.mid')

