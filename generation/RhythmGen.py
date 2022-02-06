# The important conecpt of rhythm is beat, tempo, meter
from midiutil.MidiFile import MIDIFile

class RhythmGen():
    # Tempo: slow, midium, fast are defined as 60 bpm, 120 bpm, and 240 bpm
    # time specify how 
    def __init__(self, tempo, track=0, channel=0, volume=100) -> None:
        self.tempo = tempo
        self.track = track
        self.channel = channel
        self.volume = volume

    # meter Simple Duple,  Simple Triple, Simple Quadruple define how many notes in a beat
    def generateRhythm(self, meter, top, bottom):
        # top number tells you how many beats there are in one measure.
        # bottom number means half, quater, eight. etc notes.
        time_signature  =  (top, bottom) 

        # different meters
        # define a measures, one measure contains {top} beats
        measures = []

        # the time at which the note sounds. The value can be either quarter notes [Float], or ticks [Integer].
        # the duration of the note. Like the time argument, the value can be either quarter notes [Float]
        time     = 0    # In beats, start at beat 0
        duration = 1    # In beats

        # meter tells how you are going to divide your beats
        degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # pitches

        MyMIDI = MIDIFile(1)  # One track, defaults to format 1
        MyMIDI.addTempo(self.track, time, self.tempo)

        # return out pitch time and duration, basicly the Note objects
        # play for one measure
        for i, pitch in enumerate(measures):
            MyMIDI.addNote(self.track, self.channel, pitch, time + i, duration, self.volume)

        with open("major-scale.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
        pass
    