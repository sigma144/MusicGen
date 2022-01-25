from midiutil.MidiFile import MIDIFile
from music import Music

def create_MIDI(music: Music):
    # create your MIDI object
    mf = MIDIFile(music.tracks)

    for trackn, notes in enumerate(music.tracks):   

        time = 0    # start at the beginning
        mf.addTrackName(trackn, time, "Track" + str(trackn))
        mf.addTempo(trackn, time, music.tempo)

        # add some notes
        channel = 0
        volume = 100


        pitch = 60           # C4 (middle C)
        time = 0             # start on beat 0
        duration = 1         # 1 beat long
        mf.addNote(track, channel, pitch, time, duration, volume)

        pitch = 64           # E4
        time = 2             # start on beat 2
        duration = 1         # 1 beat long
        mf.addNote(track, channel, pitch, time, duration, volume)

        pitch = 67           # G4
        time = 4             # start on beat 4
        duration = 1         # 1 beat long
        mf.addNote(track, channel, pitch, time, duration, volume)

        # write it to disk
        with open("output.mid", 'wb') as outf:
            mf.writeFile(outf)