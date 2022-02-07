# The important conecpt of rhythm is beat, tempo, meter
from midiutil.MidiFile import MIDIFile
from music import Music, Track, Note
from midi import create_MIDI

WHOLE_NOTE = 4
HALF_NOTE = 2
QUATER_NOTE = 1
EIGHTH_NOTE = 0.5
SIXTEENTH_NOTE = 0.25

SIMPLE = 2
COMPOUND = 3

class RhythmGen():

    # meter Simple Duple, Simple Triple, Simple Quadruple define how many notes in a beat
    def generateRhythm(self, pitches, meter, time_signature, start_time):
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

        print(measures)
        return measures


if __name__ == '__main__':

    # there are 4 measures of pitches
    # pitches  = [60, 61, 60, 61, 60, 61, 60, 61]
    # pitches  = [60, 61, 62, 60, 61, 62, 60, 61, 62, 60, 61, 62]
    pitches  = [60, 61, 62, 61, 60, 61, 62, 61, 60, 61, 62, 61, 60, 61, 62, 61]
    # meter 2 is Simple, 3 is compound
    meter = 2
    # how many beats in a measure, and the note type
    time_signature = (4, QUATER_NOTE)
    start_time = 0
    
    rg = RhythmGen()
    results = rg.generateRhythm(pitches, meter, time_signature, start_time)

    testmusic = Music()
    testtrack = Track()
    # make just 1 track
    for measure in results:
        for vals in measure:
            # Note object takes pitch, time and duration
            testtrack.notes.append(Note(vals[0], vals[1], vals[2]))

    testmusic.tracks.append(testtrack)
    create_MIDI(testmusic, 'simple_quad.mid')
    