from midi import create_MIDI, create_MIDI_test
import music, rhythmgen, accomp
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import MAJOR, MINOR, SUSPENDED, DIMINISHED, AUGMENTED, DOMINANT
from music import Music, Track, Note
import random
from rhythmgen import RhythmGen, QUARTER_NOTE
from samples import Samples
import melodygen


class Templates():

    # A
    def template_A(section1):
        return section1

    # # A B
    # def template_AB(section1, section2):
    #     print(type(section1.tracks))
    #     print(section1.tracks)
    #     pass

    # A B
    def template_AB(section1tracks, section2tracks):
        
        testmusic = Music(tempo = 100, key = random.choice([A, As, B, C, Cs, D, Ds, E]))
        testmusic.sections.append(section1tracks)
        testmusic.sections.append(section2tracks)
        return testmusic


    # A B A
    def template_ABA(self):
        pass

    # A B A B
    def template_ABAB(self):
        pass

    # A B C
    def template_ABC(self):
        pass





if __name__ == "__main__":

    # random.seed(1)

    #All together with rhythmic chords & random key
    testmusic1 = Music(tempo = 100, key = random.choice([A, As, B, C, Cs, D, Ds, E]))
    chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic1.key, numChords=4), duration=2, repetitions=2)
    testtrack = Track(instrument = 49)
    testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
    testmusic1.tracks.append(testtrack)
    arptrack = Track(instrument = 46)
    arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
    testmusic1.tracks.append(arptrack)
    basstrack = Track(instrument = 42)
    basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
    testmusic1.tracks.append(basstrack)
    rhythmtrack = Track(instrument = 117, notes = rhythmgen.generate_random_rhythm(8))
    rhythmtrack = rhythmtrack.repeat(testtrack.length() // 8 + 1, 4)
    testmusic1.tracks.append(rhythmtrack)
    accomptrack = Track(instrument = 24)
    accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC)
    testmusic1.tracks.append(accomptrack)
    melodytrack = Track(instrument = 73)
    melodytrack.notes = melodygen.melody_from_chords(testmusic1, chords)
    testmusic1.tracks.append(melodytrack)

    # random.seed(2)

    #All together with rhythmic chords & random key
    testmusic2 = Music(tempo = 100, key = random.choice([A, As, B, C, Cs, D, Ds, E]))
    chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic2.key, numChords=4), duration=2, repetitions=2)
    testtrack = Track(instrument = 49)
    testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
    testmusic2.tracks.append(testtrack)
    arptrack = Track(instrument = 46)
    arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
    testmusic2.tracks.append(arptrack)
    basstrack = Track(instrument = 42)
    basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
    testmusic2.tracks.append(basstrack)
    rhythmtrack = Track(instrument = 117, notes = rhythmgen.generate_random_rhythm(8))
    rhythmtrack = rhythmtrack.repeat(testtrack.length() // 8 + 1, 4)
    testmusic2.tracks.append(rhythmtrack)
    accomptrack = Track(instrument = 24)
    accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC)
    testmusic2.tracks.append(accomptrack)
    melodytrack = Track(instrument = 73)
    melodytrack.notes = melodygen.melody_from_chords(testmusic2, chords)
    testmusic2.tracks.append(melodytrack)




    # song = Templates.template_A(testmusic1)
    # create_MIDI(song, "template_A")

    # song = Templates.template_A(testmusic2)
    # create_MIDI(song, "template_A2")


    # song = Templates.template_AB(testmusic1, testmusic2) 
    # create_MIDI(song, "template_AB")

    song = Templates.template_AB(testmusic1.tracks, testmusic2.tracks) 
    create_MIDI_test(song, "template_AB")

