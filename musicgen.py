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
        templatestr = random.choice(['ABACA', 'ABACBA', 'ABABCB', 'ABCBA', 'ABCABA'])
        self.tempo = random.randint(80, 160)
        self.key = random.randrange(12)
        self.meter = random.choice([SIMPLE, COMPOUND])
        def lr(first, last): return list(range(first, last+1))
        melodic_instruments = lr(0,8)+lr(17,31)+lr(41,44)+lr(55,88)+lr(105,111)+[115]
        perc_instruments = lr(0,16)+lr(25,29)+lr(46,47)+lr(105,115)
        sustain_instruments = lr(17,24)+[30,31]+lr(41,45)+lr(49,55)+lr(57,96)
        bass_instruments = lr(33,40)+[48]
        instrument_sets = {'melody':melodic_instruments,
                       'melody2':melodic_instruments,
                       'chords':sustain_instruments,
                       'arpeggio':perc_instruments,
                       'strum':perc_instruments,
                       'bass':sustain_instruments,
                       'rbass':bass_instruments}
        self.instruments = {k:random.choice(v) for k,v in instrument_sets.items()}
        sections = []
        for s in set(templatestr):
            for k in self.instruments:
                if random.randrange(3) == 0:
                    self.instruments[k] = random.choice(instrument_sets[k])
            types = ["chords", "rchords", "bass", "rbass", "arpeg", "drums"]
            selected = [random.choice(types) for _ in range(10)] + ["melody"]
            section = self.generate_section(selected)
            sections.append(section)
        template = Template(templateType=templatestr, sections=sections)
        song = template.getSections()
        return song

    def generate_section(self, types=["chords", "rchords", "bass", "rbass", "arpeg", "melody", "drums"]):
        testmusic = Music(tempo = self.tempo, key = self.key)
        chords = random.choice([
            Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=4), duration=4, repetitions=2),
            Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=testmusic.key, numChords=4), duration=4, repetitions=2),
            Samples().get_chords_from_prog(Samples().chord_prog_generator_borrowed(progKey=testmusic.key, numChords=4), duration=4, repetitions=2)
        ])
        volume_scale = 80
        if "chords" in types:
            chordtrack = Track(instrument = self.instruments["chords"], volume=volume_scale)
            chordtrack.notes = accomp_from_chords(chords, style=accomp.CHORDS)
            testmusic.tracks.append(chordtrack)
        if "rbass" in types:
            rhythmbasstrack = Track(instrument = self.instruments["rbass"], volume=100)
            rhythmbasstrack.notes = accomp_from_chords(chords, style=accomp.RHYTHMIC_BASS, meter=self.meter)
            testmusic.tracks.append(rhythmbasstrack)
        if "bass" in types:
            basstrack = Track(instrument = self.instruments["bass"], volume=100)
            basstrack.notes = accomp_from_chords(chords, style=accomp.BASS, meter=self.meter)
            testmusic.tracks.append(basstrack)
        if "rchords" in types:
            strumtrack = Track(instrument = self.instruments["strum"], volume=volume_scale)
            strumtrack.notes = accomp_from_chords(chords, style=accomp.RHYTHMIC, meter=self.meter)
            testmusic.tracks.append(strumtrack)
        if "arpeg" in types:
            arpeggiotrack = Track(instrument = self.instruments["arpeggio"], volume=volume_scale)
            arpeggiotrack.notes = accomp_from_chords(chords, style=accomp.ARPEGGIO, meter=self.meter)
            testmusic.tracks.append(arpeggiotrack)
        if "melody" in types:
            melodytrack = Track(instrument = self.instruments["melody"], volume=100)
            melodytrack.notes = melodygen.melody_from_chords(testmusic, chords, meter=self.meter)
            testmusic.tracks.append(melodytrack)
            testmusic.melody = melodytrack
        if "melody2" in types:
            melodytrack2 = Track(instrument = self.instruments["melody2"])
            melodytrack2.notes = melodygen.melody_from_chords(testmusic, chords, meter=self.meter)
            testmusic.tracks.append(melodytrack2)
        if "drums" in types:
            rhythmtrack = generate_random_rhythm_track(4, self.meter)
            rhythmtrack = rhythmtrack.repeat(8, 4)
            rhythmtrack.volume = volume_scale
            testmusic.tracks.append(rhythmtrack)
        return testmusic

if __name__ == "__main__":

    song = MusicGen().generate_music()
    create_MIDI(song, "musicgen.mid")