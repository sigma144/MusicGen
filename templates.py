from mimetypes import init
from midi import create_MIDI
import music, rhythmgen, accomp
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import MAJOR, MINOR, SUSPENDED, DIMINISHED, AUGMENTED, DOMINANT
from music import Music, Track, Note
import random
from rhythmgen import COMPOUND, RhythmGen, QUARTER_NOTE
from samples import Samples
import melodygen
import time
from datetime import datetime




templateTypes = ["A", "AB", "ABA", "ABC", "ABCD"]

class Template():

    ''' 
    templateType (str): The type of template to create (from templateTypes). e.g. "A", "AB", etc.
    sections (list[Music]): a list of Music objects
    '''
    def __init__(self, templateType, sections):
        if templateType not in templateType:
            print("Invalid template type used")
        self.templateType = templateType
        self.sections = sections


    # FIXME create Music objects from sections and return list of music objects
    '''
    Returns a list of Music objects following the template.
    '''
    def getSections(self):

        # Only accept valid combinations of sections and templateTypes
        unique_sections = list(set(self.templateType))
        if len(self.sections) != len(unique_sections):
           print("Invalid sections/templateType combination")
           return []

        sections = []

        for c in self.templateType:
            index = ord(c) - ord('A')
            sections.append(self.sections[index])

        return sections

def make_test_section():
    #Random Instruments
    testmusic = Music(tempo = 150)
    testtrack = Track(instrument = random.randrange(115))
    chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=4), duration=4, repetitions=1)
    testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
    basstrack = Track(instrument = random.randrange(115))
    basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC_BASS, meter=COMPOUND)
    testmusic.tracks.append(basstrack)
    rhythmtrack = Track(instrument = random.randrange(115, 119), notes = rhythmgen.generate_random_rhythm(8, meter=COMPOUND))
    rhythmtrack = rhythmtrack.repeat(testtrack.length() // 8, 8)
    testmusic.tracks.append(rhythmtrack)
    rhythmtrack2 = Track(instrument = random.randrange(115, 119), notes = rhythmgen.generate_random_rhythm(8, meter=COMPOUND))
    rhythmtrack2 = rhythmtrack2.repeat(testtrack.length() // 8, 8)
    testmusic.tracks.append(rhythmtrack2)
    accomptrack = Track(instrument = random.randrange(115))
    accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC, meter=COMPOUND)
    testmusic.tracks.append(accomptrack)
    melodytrack = Track(instrument = random.randrange(115))
    melodytrack.notes = melodygen.melody_from_chords(testmusic, chords, meter=COMPOUND)
    testmusic.tracks.append(melodytrack)
    return testmusic

if __name__ == "__main__":

    sectionA = make_test_section()
    
    sectionB = make_test_section()

    sectionC = make_test_section()

    sectionD = make_test_section()
    
    sections = [sectionA]
    template = Template(templateType="A", sections=sections)
    song = template.getSections()
    create_MIDI(song, outfile='A.mid')

    sections = [sectionA, sectionB]
    template = Template(templateType="AB", sections=sections)
    song = template.getSections()
    create_MIDI(song, outfile='AB.mid')

    sections = [sectionA, sectionB]
    template = Template(templateType="ABA", sections=sections)
    song = template.getSections()
    create_MIDI(song, outfile='ABA.mid')

    sections = [sectionA, sectionB, sectionC]
    template = Template(templateType="ABC", sections=sections)
    song = template.getSections()
    create_MIDI(song, outfile='ABC.mid')

    sections = [sectionA, sectionB, sectionC, sectionD]
    template = Template(templateType="ABCD", sections=sections)
    song = template.getSections()
    create_MIDI(song, outfile='ABCD.mid')
    



