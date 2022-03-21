import random
import accomp
from midi import create_MIDI
import rhythmgen
import melodygen
from accomp import accomp_from_chords
from music import Music, A, As, B, C, Cs, D, Ds, E, Track
from rhythmgen import SIMPLE, COMPOUND, generate_random_rhythm_track
from samples import Samples
from templates import Template

class MusicGen():

    def generate_music(self, filename):
        templatestr = random.choice(['ABACA', 'ABABA', 'ABCA'])
        self.tempo = random.randint(80, 160)
        self.key = random.choice([A, As, B, C, Cs, D, Ds, E])
        #self.meter = random.choice([SIMPLE, COMPOUND])
        self.meter = COMPOUND
        self.instruments = {'melody':random.randrange(115),
                       'melody2':random.randrange(115),
                       'chords':random.randrange(115),
                       'arpeggio':random.randrange(115),
                       'strum':random.randrange(115),
                       'bass':random.randrange(115),

                       'drumbass':random.randrange(115),
                       'drumsnare':random.randrange(115),
                       'drumbacking':random.randrange(115)}
        sections = []
        for s in set(templatestr):
            section = self.generate_section()
            sections.append(section)
        template = Template(templateType=templatestr, sections=sections)
        song = template.getSections()
        create_MIDI(song, filename)

    def generate_section(self):
        testmusic = Music(tempo = self.tempo, key = self.key)
        chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=4), duration=4, repetitions=1)

        chordtrack = Track(instrument = self.instruments["chords"])
        chordtrack.notes = accomp_from_chords(chords, style=accomp.CHORDS)
        testmusic.tracks.append(chordtrack)

        rhythmbasstrack = Track(instrument = self.instruments["bass"])
        rhythmbasstrack.notes = accomp_from_chords(chords, style=accomp.RHYTHMIC_BASS, meter=self.meter)
        testmusic.tracks.append(rhythmbasstrack)

        basstrack = Track(instrument = self.instruments["bass"])
        basstrack.notes = accomp_from_chords(chords, style=accomp.BASS, meter=self.meter)
        testmusic.tracks.append(basstrack)

        strumtrack = Track(instrument = self.instruments["strum"])
        strumtrack.notes = accomp_from_chords(chords, style=accomp.RHYTHMIC, meter=self.meter)
        testmusic.tracks.append(strumtrack)

        arpeggiotrack = Track(instrument = self.instruments["arpeggio"])
        arpeggiotrack.notes = accomp_from_chords(chords, style=accomp.ARPEGGIO, meter=self.meter)
        testmusic.tracks.append(arpeggiotrack)

        melodytrack = Track(instrument = self.instruments["melody"])
        melodytrack.notes = melodygen.melody_from_chords(testmusic, chords, meter=self.meter)
        testmusic.tracks.append(melodytrack)

        melodytrack2 = Track(instrument = self.instruments["melody2"])
        melodytrack2.notes = melodygen.melody_from_chords(testmusic, chords, meter=self.meter)
        testmusic.tracks.append(melodytrack2)

        #rhythmtrack = generate_random_rhythm_track(8, self.meter)
        #testmusic.tracks.append(rhythmtrack)

        return testmusic

if __name__ == "__main__":

    MusicGen().generate_music("musicgen.mid")