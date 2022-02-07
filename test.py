from midi import create_MIDI
import music
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import Music, Track, Note
import random
import accomp
import rhythmgen
from rhythmgen import RhythmGen
from samples import Samples
import melodygen

#New Chord Generator
testmusic = Music(tempo = 85, key=C)
testtrack = Track(instrument = 49)
chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(8), duration=4, repetitions=8)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
create_MIDI(testmusic, 'chordgen.mid')
