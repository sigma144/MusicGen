from midi import create_MIDI
import music, rhythmgen, accomp
from musicgen import MusicGen
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import MAJOR, MINOR, SUSPENDED, DIMINISHED, AUGMENTED, DOMINANT
from music import Music, Track, Note
import random
from rhythmgen import COMPOUND, RhythmGen, QUARTER_NOTE, generate_random_rhythm_track
from samples import Samples
import melodygen

#Multi-track
testmusic = Music()
testtrack = Track()
for i in range(100):
    testtrack.notes.append(Note(random.randrange(40, 80), i, 1))
testmusic.tracks.append(testtrack)
testtrack2 = Track(instrument = 19)
for i in range(100):
    testtrack2.notes.append(Note(random.randrange(40, 80), i, 1))
testmusic.tracks.append(testtrack2)
create_MIDI(testmusic, 'multi.mid')

#Chaos
testmusic = Music()
testtrack = Track()
for _ in range(2):
    for i in range(100):
        testtrack.notes.append(Note(random.randrange(40, 80), i/2, 1/2))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'chaos.mid')

#Scale
testmusic = Music()
testtrack = Track()
for _ in range(2):
    for i in range(100):
        testtrack.notes.append(Note(testmusic.get_scale_note(random.randrange(-10, 10)), i/2, 1/2))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'scale.mid')

#Chaos Chords
testmusic = Music()
testtrack = Track(instrument = 89)
for _ in range(3):
    for i in range(50):
        testtrack.notes.append(Note(random.randrange(40, 80), i*5, 5))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'chordc.mid')

#Scale Chords
testmusic = Music()
testtrack = Track(instrument = 89)
for _ in range(3):
    for i in range(50):
        testtrack.notes.append(Note(testmusic.get_scale_note(random.randrange(0, 20)), i*5, 5))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'chords.mid')

#Scale Triads
testmusic = Music()
testtrack = Track(instrument = 89)
for i in range(50):
    for n in testmusic.get_scale_chord(random.randrange(7) - 6, inversion=random.randrange(3)):
        testtrack.notes.append(Note(n, i*5, 5))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'triads.mid')

#Scale Triads+Sevenths
testmusic = Music()
testtrack = Track(instrument = 89)
for i in range(50):
    for n in testmusic.get_scale_chord(random.randrange(7) - 6, inversion=random.randrange(4),
        seventh=random.choice([music.DOMINANT, music.MAJOR, music.DIMINISHED])):
        testtrack.notes.append(Note(n, i*5, 5))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'sevenths.mid')

#Random Triads+Sevenths
testmusic = Music()
testtrack = Track(instrument = 89)
for i in range(50):
    for n in testmusic.get_chord(random.randrange(50, 70), quality=random.choice([MINOR, MAJOR, DIMINISHED, AUGMENTED, SUSPENDED]),
        inversion=random.randrange(4), seventh=random.choice([None, None, DOMINANT, MAJOR, DIMINISHED])):
        testtrack.notes.append(Note(n, i*5, 5))
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'triadr.mid')

#Messing with rhythms
testmusic = Music(key = E)
testtrack = Track()
time = 0
for i in range(100):
    duration = random.choice([1, 1/2])
    if random.randrange(3) > 0:
        testtrack.notes.append(Note(testmusic.get_scale_note(random.randrange(-10, 10)), time, duration))
    time += duration
testmusic.tracks.append(testtrack)
drumtrack = Track(instrument = 116, notes = rhythmgen.generate_random_rhythm(testtrack.length()))
testmusic.tracks.append(drumtrack)
create_MIDI(testmusic, 'rhythm.mid')

#Chords + Bass
testmusic = Music()
testtrack = Track(instrument = 49)
chords = []
for i in range(50):
    chord = [Note(n, i*5, 5) for n in testmusic.get_scale_chord(random.randrange(14) + 12, inversion=random.randrange(3))]
    chords.append(chord)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
create_MIDI(testmusic, 'bass.mid')

#Arpeggio + Bass
testmusic = Music(tempo = 85)
testtrack = Track(instrument = 49)
chords = []
for i in range(50):
    chord = [Note(n, i*4, 4) for n in testmusic.get_scale_chord(random.randrange(14) + 12, inversion=random.randrange(3))]
    chords.append(chord)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
arptrack = Track(instrument = 46)
arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
testmusic.tracks.append(arptrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
create_MIDI(testmusic, 'arpeggio.mid')

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

#New Rhythm Generator
testmusic = Music()
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
rhythmtrack = RhythmGen().generate_rhythm_track(basstrack.notes[-1].time + 4, 117)
testmusic.tracks.append(rhythmtrack)
create_MIDI(testmusic, 'drums.mid')

#New Chord Generator
testmusic = Music(tempo = 85)
testtrack = Track(instrument = 49)
chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=8), duration=4, repetitions=8)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
arptrack = Track(instrument = 46)
arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
testmusic.tracks.append(arptrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
create_MIDI(testmusic, 'chordgen.mid')

#Testing Melody Generator
testmusic = Music(tempo = 85)
testtrack = Track(instrument = 49)
chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=8), duration=4, repetitions=8)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
melodytrack = Track(instrument = 73)
melodytrack.notes = melodygen.melody_from_chords(testmusic, chords)
testmusic.tracks.append(melodytrack)
create_MIDI(testmusic, 'melody.mid')

#All together
testmusic = Music(tempo = 100, key = random.choice([A, As, B, C, Cs, D, Ds, E]))
chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=8), duration=4, repetitions=8)
testtrack = Track(instrument = 49)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
arptrack = Track(instrument = 46)
arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
testmusic.tracks.append(arptrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
rhythmtrack = generate_random_rhythm_track(4)
rhythmtrack = rhythmtrack.repeat(testtrack.length() // 4 + 1, 4)
testmusic.tracks.append(rhythmtrack)
accomptrack = Track(instrument = 24)
accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC)
testmusic.tracks.append(accomptrack)
melodytrack = Track(instrument = 73)
melodytrack.notes = melodygen.melody_from_chords(testmusic, chords)
testmusic.tracks.append(melodytrack)
create_MIDI(testmusic, 'alltogether.mid')

#All together with rhythmic chords & random key, & compound
testmusic = Music(tempo = 100, key = random.choice([A, As, B, C, Cs, D, Ds, E]))
chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=8), duration=4, repetitions=8)
testtrack = Track(instrument = 49)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
arptrack = Track(instrument = 46)
arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO, meter=COMPOUND)
testmusic.tracks.append(arptrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
rhythmtrack = generate_random_rhythm_track(4, meter=COMPOUND)
rhythmtrack = rhythmtrack.repeat(testtrack.length() // 4 + 1, 4)
testmusic.tracks.append(rhythmtrack)
accomptrack = Track(instrument = 24)
accomptrack.notes = accomp.accomp_from_chords(chords, accomp.RHYTHMIC, rhythmgen.COMPOUND)
testmusic.tracks.append(accomptrack)
melodytrack = Track(instrument = 73)
melodytrack.notes = melodygen.melody_from_chords(testmusic, chords, rhythmgen.COMPOUND)
testmusic.tracks.append(melodytrack)
create_MIDI(testmusic, 'alltogethercomp.mid')

#Random Instruments
testmusic = Music(tempo = 150)
testtrack = Track(instrument = random.randrange(115))
chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=8), duration=4, repetitions=8)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
basstrack = Track(instrument = random.randrange(115))
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC_BASS, meter=COMPOUND)
testmusic.tracks.append(basstrack)
rhythmtrack = Track(instrument = random.randrange(115, 119), notes = rhythmgen.generate_random_rhythm(8, meter=COMPOUND))
rhythmtrack = rhythmtrack.repeat(testtrack.length() // 8 + 1, 8)
testmusic.tracks.append(rhythmtrack)
rhythmtrack2 = Track(instrument = random.randrange(115, 119), notes = rhythmgen.generate_random_rhythm(8, meter=COMPOUND))
rhythmtrack2 = rhythmtrack2.repeat(testtrack.length() // 8 + 1, 8)
testmusic.tracks.append(rhythmtrack2)
accomptrack = Track(instrument = random.randrange(115))
accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC, meter=COMPOUND)
testmusic.tracks.append(accomptrack)
melodytrack = Track(instrument = random.randrange(115))
melodytrack.notes = melodygen.melody_from_chords(testmusic, chords, meter=COMPOUND)
testmusic.tracks.append(melodytrack)
create_MIDI(testmusic, 'instruments.mid')

#Trying out different chord duration
testmusic = Music(tempo = 100, key = random.choice([A, As, B, C, Cs, D, Ds, E]))
chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=5), duration=[4, 4, 4, 2, 2], repetitions=8)
testtrack = Track(instrument = 49)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(testtrack)
arptrack = Track(instrument = 46)
arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
testmusic.tracks.append(arptrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic.tracks.append(basstrack)
rhythmtrack = Track(instrument = 117, notes = rhythmgen.generate_random_rhythm(8))
rhythmtrack = rhythmtrack.repeat(testtrack.length() // 8 + 1, 8)
testmusic.tracks.append(rhythmtrack)
accomptrack = Track(instrument = 24)
accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC)
testmusic.tracks.append(accomptrack)
melodytrack = Track(instrument = 73)
melodytrack.notes = melodygen.melody_from_chords(testmusic, chords)
testmusic.tracks.append(melodytrack)
create_MIDI(testmusic, 'morechords.mid')

#Testing drum kits
testmusic = Music(tempo = 180)
testtrack = generate_random_rhythm_track(16)
testmusic.tracks.append(testtrack)
create_MIDI(testmusic, 'drumkit.mid')

#Concatenation
#Part 1
testmusic1 = Music(tempo = 100)
testtrack = Track(instrument = 49)
chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic1.key, numChords=4), duration=4, repetitions=2)
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic1.tracks.append(testtrack)
basstrack = Track(instrument = 42)
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
testmusic1.tracks.append(basstrack)
melodytrack = Track(instrument = 73)
melodytrack.notes = melodygen.melody_from_chords(testmusic1, chords)
testmusic1.tracks.append(melodytrack)
#Part 2
testmusic2 = Music(tempo = 150)
testtrack = Track(instrument = random.randrange(115))
testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
basstrack = Track(instrument = random.randrange(115))
basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC_BASS)
testmusic2.tracks.append(basstrack)
rhythmtrack = Track(instrument = random.randrange(115, 119), notes = rhythmgen.generate_random_rhythm(8, meter=COMPOUND))
rhythmtrack = rhythmtrack.repeat(testtrack.length() // 8, 8)
testmusic2.tracks.append(rhythmtrack)
rhythmtrack2 = Track(instrument = random.randrange(115, 119), notes = rhythmgen.generate_random_rhythm(8, meter=COMPOUND))
rhythmtrack2 = rhythmtrack2.repeat(testtrack.length() // 8, 8)
testmusic2.tracks.append(rhythmtrack2)
accomptrack = Track(instrument = random.randrange(115))
accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC, meter=COMPOUND)
testmusic2.tracks.append(accomptrack)
melodytrack = Track(instrument = random.randrange(115))
melodytrack.notes = melodygen.melody_from_chords(testmusic2, chords, meter=COMPOUND)
testmusic2.tracks.append(melodytrack)
#Part 3
testmusic3 = Music(tempo = 180)
testtrack = generate_random_rhythm_track(16)
testmusic3.tracks.append(testtrack)
create_MIDI([testmusic1, testmusic2, testmusic3, testmusic1], 'concat.mid')

#Split/join test
testmusic = Music(tempo = 100)
chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=8), duration=4, repetitions=1)
chordtrack = Track(instrument = 49)
chordtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
testmusic.tracks.append(chordtrack)
rhythmtrack = generate_random_rhythm_track(4)
rhythmtrack = rhythmtrack.repeat(8, 4)
testmusic.tracks.append(rhythmtrack)
melodytrack = Track(instrument = 73)
melodytrack.notes = melodygen.melody_from_chords(testmusic, chords)
testmusic.tracks.append(melodytrack)
create_MIDI(testmusic, "testsplit.mid")
measures = melodytrack.split()
newmusic = Music(tempo = 100)
newtrack = melodytrack.join(measures)
newmusic.tracks.append(newtrack)
newmusic.tracks.append(chordtrack)
newmusic.tracks.append(rhythmtrack)
create_MIDI(testmusic, "testjoin.mid")

#MusicGen test
song = MusicGen().generate_music()
create_MIDI(song, "musicgen.mid")