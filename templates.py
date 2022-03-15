from mimetypes import init
from midi import create_MIDI
import music, rhythmgen, accomp
from music import A, As, Bb, B, C, Bs, Cs, Db, D, Ds, Eb, E, Fb, F, Es, Fs, Gb, G, Gs, Ab, OCTAVE
from music import MAJOR, MINOR, SUSPENDED, DIMINISHED, AUGMENTED, DOMINANT
from music import Music, Track, Note
import random
from rhythmgen import RhythmGen, QUARTER_NOTE
from samples import Samples
import melodygen
import time
from datetime import datetime




templateTypes = ["A", "AB", "ABA"]

class Section:

    '''
    A Section contains all the necessary elements to create a section of the song
    '''
    def __init__(self, tempo=100, key=C, chords_instrument=49, num_chords=4,
        chords_duration=2, chords_repetitions=2, arpeggio_instrument=46, bass_instrument=42,
        rhythm_instrument=117, accomp_instrument=24, melody_instrument=73):

        self.tempo = tempo
        self.key = key
        self.chords_instrument = chords_instrument
        self.num_chords = num_chords
        self.chords_duration = chords_duration
        self.chords_repetitions = chords_repetitions
        self.arpeggio_instrument = arpeggio_instrument
        self.bass_instrument = bass_instrument
        self.rhythm_instrument = rhythm_instrument
        self.accomp_instrument = accomp_instrument
        self.melody_instrument = melody_instrument
    
    def get_tempo(self):
        return self.tempo

    def get_key(self):
        return self.key

    def get_chords_instrument(self):
        return self.chords_instrument
    
    def get_num_chords(self):
        return self.num_chords
    
    def get_chords_duration(self):
        return self.chords_duration
    
    def get_chords_repetitions(self):
        return self.chords_repetitions
    
    def get_arpeggio_instrument(self):
        return self.arpeggio_instrument
    
    def get_bass_instrument(self):
        return self.bass_instrument
    
    def get_rhythm_instrument(self):
        return self.rhythm_instrument

    def get_accomp_instrument(self):
        return self.accomp_instrument

    def get_melody_instrument(self):
        return self.melody_instrument
    




class Template():

    ''' 
    templateType (str): The type of template to create (from templateTypes). e.g. "A", "AB", etc.
    sections (list[Section]): a list of Section objects
    '''
    def __init__(self, templateType, sections):
        if templateType not in templateType:
            print("Invalid template type used")
        self.templateType = templateType
        self.sections = sections



    # FIXME create Music objects from sections and return list of music objects
    def getSections(self):

        # Only accept valid combinations of sections and templateTypes
        unique_sections = list(set(self.templateType))
        if len(self.sections) != len(unique_sections):
           print("Invalid sections/templateType combination")
           return []

        # FIXME if a section is repeated, add it to list
        sections = self.sections
        randSeeds = []

        if self.templateType == "A":
            randSeeds.append(time.time())

        if self.templateType == "AB":
            randSeeds.append(time.time())
            randSeeds.append(time.time())

        if self.templateType == "ABA":
            sections.append(sections[0])
            randSeeds.append(time.time())
            randSeeds.append(time.time())
            randSeeds.append(randSeeds[0])

        all_sections = []
        for section, randSeed in zip(sections, randSeeds):

            testmusic = Music(tempo=section.get_tempo(), key=section.get_key())
            chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=section.get_num_chords(), randSeed=randSeed), duration=section.get_chords_duration(), repetitions=section.get_chords_repetitions())
            testtrack = Track(instrument=section.get_chords_instrument())
            testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
            testmusic.tracks.append(testtrack)
            arptrack = Track(instrument=section.get_arpeggio_instrument())
            arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
            testmusic.tracks.append(arptrack)
            basstrack = Track(instrument=section.get_bass_instrument())
            basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
            testmusic.tracks.append(basstrack)
            rhythmtrack = Track(instrument=section.get_rhythm_instrument(), notes = rhythmgen.generate_random_rhythm(8))
            rhythmtrack = rhythmtrack.repeat(testtrack.length() // 8 + 1, 4)
            testmusic.tracks.append(rhythmtrack)
            accomptrack = Track(instrument=section.get_accomp_instrument())
            accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC)
            testmusic.tracks.append(accomptrack)
            melodytrack = Track(instrument=section.get_melody_instrument())
            melodytrack.notes = melodygen.melody_from_chords(testmusic, chords)
            testmusic.tracks.append(melodytrack)

            all_sections.append(testmusic)

        return all_sections

    


    # # Choose template, key of song, tempo, 
    # def choose_template(template = templateTypes["AB"]):
    #     pass

    # # A
    # def template_A(section1):
    #     return section1

    # # # A B
    # # def template_AB(section1, section2):
    # #     print(type(section1.tracks))
    # #     print(section1.tracks)
    # #     pass

    # # A B
    # def template_AB(section1tracks, section2tracks):
        
    #     pass

    # # A B A
    # def template_ABA(self):
    #     pass

    # # A B A B
    # def template_ABAB(self):
    #     pass

    # # A B C
    # def template_ABC(self):
    #     pass





if __name__ == "__main__":

    random.seed(1)

    # #All together with rhythmic chords & random key
    # testmusic1 = Music(tempo = 100, key = random.choice([A, As, B, C, Cs, D, Ds, E]))
    # chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic1.key, numChords=4), duration=2, repetitions=2)
    # testtrack = Track(instrument = 49)
    # testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
    # testmusic1.tracks.append(testtrack)
    # arptrack = Track(instrument = 46)
    # arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
    # testmusic1.tracks.append(arptrack)
    # basstrack = Track(instrument = 42)
    # basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
    # testmusic1.tracks.append(basstrack)
    # rhythmtrack = Track(instrument = 117, notes = rhythmgen.generate_random_rhythm(8))
    # rhythmtrack = rhythmtrack.repeat(testtrack.length() // 8 + 1, 4)
    # testmusic1.tracks.append(rhythmtrack)
    # accomptrack = Track(instrument = 24)
    # accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC)
    # testmusic1.tracks.append(accomptrack)
    # melodytrack = Track(instrument = 73)
    # melodytrack.notes = melodygen.melody_from_chords(testmusic1, chords)
    # testmusic1.tracks.append(melodytrack)

    # # random.seed(2)

    # #All together with rhythmic chords & random key
    # testmusic2 = Music(tempo = 100, key = random.choice([A, As, B, C, Cs, D, Ds, E]))
    # chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic2.key, numChords=4), duration=2, repetitions=2)
    # testtrack = Track(instrument = 49)
    # testtrack.notes = accomp.accomp_from_chords(chords, style=accomp.CHORDS)
    # testmusic2.tracks.append(testtrack)
    # arptrack = Track(instrument = 46)
    # arptrack.notes = accomp.accomp_from_chords(chords, style=accomp.ARPEGGIO)
    # testmusic2.tracks.append(arptrack)
    # basstrack = Track(instrument = 42)
    # basstrack.notes = accomp.accomp_from_chords(chords, style=accomp.BASS)
    # testmusic2.tracks.append(basstrack)
    # rhythmtrack = Track(instrument = 117, notes = rhythmgen.generate_random_rhythm(8))
    # rhythmtrack = rhythmtrack.repeat(testtrack.length() // 8 + 1, 4)
    # testmusic2.tracks.append(rhythmtrack)
    # accomptrack = Track(instrument = 24)
    # accomptrack.notes = accomp.accomp_from_chords(chords, style=accomp.RHYTHMIC)
    # testmusic2.tracks.append(accomptrack)
    # melodytrack = Track(instrument = 73)
    # melodytrack.notes = melodygen.melody_from_chords(testmusic2, chords)
    # testmusic2.tracks.append(melodytrack)

    # Working
    # create_MIDI([testmusic1, testmusic2], "template_test.mid")





    # # Working
    # sectionA = Section(tempo=100, key=C, chords_instrument=49, num_chords=4,
    # chords_duration=2, chords_repetitions=2, arpeggio_instrument=46, bass_instrument=42,
    # rhythm_instrument=117, accomp_instrument=24, melody_instrument=73)
    
    # sectionB = Section(tempo=100, key=C, chords_instrument=49, num_chords=4,
    # chords_duration=2, chords_repetitions=2, arpeggio_instrument=46, bass_instrument=42,
    # rhythm_instrument=117, accomp_instrument=24, melody_instrument=73)
    
    # sections = [sectionA, sectionB]
    # template = Template(templateType="AB", sections=sections)
    # song = template.getSections()

    # create_MIDI(song, outfile='AB.mid')






    sectionA = Section(tempo=100, key=C, chords_instrument=49, num_chords=4,
    chords_duration=2, chords_repetitions=2, arpeggio_instrument=46, bass_instrument=42,
    rhythm_instrument=117, accomp_instrument=24, melody_instrument=73)
    
    sectionB = Section(tempo=100, key=C, chords_instrument=49, num_chords=4,
    chords_duration=2, chords_repetitions=2, arpeggio_instrument=46, bass_instrument=42,
    rhythm_instrument=117, accomp_instrument=24, melody_instrument=73)
    
    sections = [sectionA, sectionB]
    template = Template(templateType="ABA", sections=sections)
    song = template.getSections()

    create_MIDI(song, outfile='ABA.mid')
    



