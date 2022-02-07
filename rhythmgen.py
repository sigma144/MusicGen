# The important conecpt of rhythm is beat, tempo, meter
from midiutil.MidiFile import MIDIFile
from music import Music, Track, Note
from midi import create_MIDI

import random
# Old function for demos
def generate_rhythm(beats):
    rhythm = []
    for i in range(beats * 2):
        if random.randrange(5) >= 2:
            rhythm.append(i/2)
    return rhythm

WHOLE_NOTE = 4
HALF_NOTE = 2
QUARTER_NOTE = 1
EIGHTH_NOTE = 0.5
SIXTEENTH_NOTE = 0.25

SIMPLE = 2
COMPOUND = 3

class RhythmGen():

    def generate_rhythm_track(self, beats, instrument, pitch=60, meter=2, time_signature=(4, QUARTER_NOTE)):
        results = self.generate_rhythm_measures([pitch]*beats, meter, time_signature, start_time=0)
        track = Track(instrument=instrument)
        for measure in results:
            for vals in measure:
                track.notes.append(Note(vals[0], vals[1], vals[2]))
        return track
    # meter Simple Duple, Simple Triple, Simple Quadruple define how many notes in a beat
    def generate_rhythm_measures(self, pitches, meter, time_signature, start_time):
        # top number tells you how many beats there are in one measure.
        # bottom number means half, quater, eight. etc notes.
        t, b = time_signature
        measures = []
        measure = []
        time = start_time
        for pitch in pitches:
            duration = b
            if meter == SIMPLE: # divide each note by 2
                for _ in range(2):
                    measure.append([pitch, time, duration/2])
                    time += (1/2)
            elif meter == COMPOUND: # divide each note by 3
                for _ in range(3):
                    measure.append([pitch, time, duration/3])
                    time += (1/3)
            else:
                measure.append([pitch, time, duration])
                time += 1
                
            if len(measure) == t * meter:
                measures.append(measure)
                measure = []

        return measures
    