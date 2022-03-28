import random
import accomp
from midi import create_MIDI
import rhythmgen
import melodygen
from accomp import accomp_from_chords
from music import Music, Track
from rhythmgen import SIMPLE, COMPOUND, generate_random_rhythm_track
from samples import Samples
from templates import Template

class MusicGen():

    def generate_music(self):
        templatestr = random.choice(['ABACA', 'ABABCB'])
        self.tempo = random.randint(80, 160)
        self.key = random.randrange(12)
        self.meter = random.choice([SIMPLE, COMPOUND])
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
            for k in self.instruments:
                if random.randrange(3) == 0:
                    self.instruments[k] = random.randrange(115)
            section = self.generate_section()
            sections.append(section)
        template = Template(templateType=templatestr, sections=sections)
        song = template.getSections()
        return song

    def generate_section(self):
        testmusic = Music(tempo = self.tempo, key = self.key)
        chords = random.choice([
            Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=4), duration=4, repetitions=2),
            Samples().get_chords_from_prog(Samples().chord_prog_generator_borrowed(progKey=testmusic.key, numChords=4), duration=4, repetitions=2)
        ])
        volume_scale = 70

        chordtrack = Track(instrument = self.instruments["chords"], volume=volume_scale)
        chordtrack.notes = accomp_from_chords(chords, style=accomp.CHORDS)
        testmusic.tracks.append(chordtrack)

        rhythmbasstrack = Track(instrument = self.instruments["bass"], volume=100)
        rhythmbasstrack.notes = accomp_from_chords(chords, style=accomp.RHYTHMIC_BASS, meter=self.meter)
        testmusic.tracks.append(rhythmbasstrack)

        basstrack = Track(instrument = self.instruments["bass"], volume=100)
        basstrack.notes = accomp_from_chords(chords, style=accomp.BASS, meter=self.meter)
        testmusic.tracks.append(basstrack)

        strumtrack = Track(instrument = self.instruments["strum"], volume=volume_scale)
        strumtrack.notes = accomp_from_chords(chords, style=accomp.RHYTHMIC, meter=self.meter)
        testmusic.tracks.append(strumtrack)

        arpeggiotrack = Track(instrument = self.instruments["arpeggio"], volume=volume_scale)
        arpeggiotrack.notes = accomp_from_chords(chords, style=accomp.ARPEGGIO, meter=self.meter)
        testmusic.tracks.append(arpeggiotrack)

        melodytrack = Track(instrument = self.instruments["melody"], volume=100)
        melodytrack.notes = melodygen.melody_from_chords(testmusic, chords, meter=self.meter)
        testmusic.tracks.append(melodytrack)
        testmusic.melody = melodytrack

        #melodytrack2 = Track(instrument = self.instruments["melody2"])
        #melodytrack2.notes = melodygen.melody_from_chords(testmusic, chords, meter=self.meter)
        #testmusic.tracks.append(melodytrack2)

        rhythmtrack = generate_random_rhythm_track(4, self.meter)
        rhythmtrack = rhythmtrack.repeat(8, 4)
        rhythmtrack.volume = volume_scale+10
        testmusic.tracks.append(rhythmtrack)

        return testmusic

if __name__ == "__main__":

    song = MusicGen().generate_music()
    create_MIDI(song, "musicgen.mid")