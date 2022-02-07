from midi import create_MIDI
import music, rhythmgen, accomp
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import MAJOR, MINOR, SUSPENDED, DIMINISHED, AUGMENTED, DOMINANT
from music import Music, Track, Note
import random
from rhythmgen import RhythmGen, QUARTER_NOTE

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
drumtrack = Track(instrument=116)
time = 0
for i in range(100):
    duration = random.choice([1, 1/2])
    if random.randrange(3) > 0:
        testtrack.notes.append(Note(testmusic.get_scale_note(random.randrange(-10, 10)), time, duration))
    time += duration
testmusic.tracks.append(testtrack)
for i in range(int(time)*2):
    if random.randrange(2) == 0:
        drumtrack.notes.append(Note(music.MIDDLE_C, i/2, 1))
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

#Drums + Chords
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
create_MIDI(testmusic, 'simple_quad.mid')