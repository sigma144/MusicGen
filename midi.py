from midiutil.MidiFile import MIDIFile
from music import Music

def create_MIDI(music, outfile='output.mid'):
    mf = MIDIFile(len(music.tracks))
    for trackn, track in enumerate(music.tracks):
        mf.addProgramChange(0, trackn, 0, track.instrument)
        time = 0
        mf.addTrackName(trackn, time, "Track" + str(trackn))
        mf.addTempo(trackn, time, music.tempo)
        volume = 100
        channel = trackn
        for n in track.notes:
            mf.addNote(trackn, channel, n.pitch, n.time, n.duration, volume)
    with open(outfile, 'wb') as outf:
        mf.writeFile(outf)