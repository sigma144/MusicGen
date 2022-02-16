# The important conecpt of rhythm is beat, tempo, meter
from unicodedata import name
from midiutil.MidiFile import MIDIFile
from music import Music, Track, Note
from midi import create_MIDI

import random
# Old function for demos
def generate_random_rhythm(beats):
    new_track = Track()
    for i in range(int(beats) * 2):
        if i == 0 or random.randrange(5) >= 2:
            new_track.notes.append(Note(60, i/2, 1))
    return new_track.notes

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

    def gen_composed_rhythm(self):
        # can also repeat by 1 or more measures
        tracks = []
        note_tracks = [WHOLE_NOTE, WHOLE_NOTE, WHOLE_NOTE, WHOLE_NOTE, HALF_NOTE, HALF_NOTE, HALF_NOTE, HALF_NOTE, 
                        QUARTER_NOTE, QUARTER_NOTE, EIGHTH_NOTE, SIXTEENTH_NOTE]
        # note_tracks = [WHOLE_NOTE, HALF_NOTE, QUARTER_NOTE, EIGHTH_NOTE, SIXTEENTH_NOTE]
        # randmaly pick from the note set to form different tracks
        # selected_tracks = [WHOLE_NOTE]
        track_nums = random.randint(2, 5)
        selected_tracks = random.sample(note_tracks, track_nums)
        # make a track for each selected ones
        for selected_track in selected_tracks:
            # suit_instrs = [9, 10, 11, 12, 46, 79, 52, 53, 54, 108, 109, 110, 108, 113, 114, 115, 116, 117, 118, 123, 126]
            suit_instrs = [114, 115, 116, 117, 118]
            # suit_instrs = range(0, 127)
            track = []
            instrument = random.choice(suit_instrs)
            beats = 16
            pitch = random.randint(60, 66)
            meter = random.randint(1, 10) # randoamly taken from 1, 2, 3, in crease the number to lower the chance of division
            
            # 4 beats and every beat is quater note, this is a very standard one, 4 beats with anything above would not
            # work, for instance, 4 beats with half note, will result in 8 in time length.
            if selected_track == WHOLE_NOTE:
                time_signature = (4, WHOLE_NOTE) 
                beats = int(beats / 4)
            if selected_track == HALF_NOTE:
                time_signature = (4, HALF_NOTE)
                beats = int(beats / 2)
            if selected_track == QUARTER_NOTE:
                time_signature = (4, QUARTER_NOTE)
            if selected_track == EIGHTH_NOTE:
                time_signature = (4, EIGHTH_NOTE)
                beats = int(beats * 2)
            if selected_track == SIXTEENTH_NOTE:
                time_signature = (4, SIXTEENTH_NOTE)
                beats = int(beats * 4)
            # randamly pick chord as well, basick define a measure of beats out
            print("track: ", instrument, meter, time_signature)
            track = self.generate_rhythm_track(beats, instrument, pitch, meter, time_signature)
            tracks.append(track)
        return tracks

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
            if meter == SIMPLE: # divide each beat by 2
                for _ in range(2):
                    measure.append([pitch, time, duration/2])
                    time += (duration/2)
            elif meter == COMPOUND: # divide each note by 3
                for _ in range(3):
                    measure.append([pitch, time, duration/3])
                    time += (duration/3)
            else:
                measure.append([pitch, time, duration])
                time += duration
                # print("here: ", measure)

            measures.append(measure)
            measure = []
        # print(measures)
        return measures
    
if __name__ == '__main__':

    for  i in range(20):
        rhythmtracks = RhythmGen().gen_composed_rhythm()
        testmusic = Music(tempo=60)
        for rhythmtrack in rhythmtracks:
            testmusic.tracks.append(rhythmtrack)
        create_MIDI(testmusic, 'rgythms' + str(i) + '.mid')