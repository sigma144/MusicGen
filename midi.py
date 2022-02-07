from midiutil.MidiFile import MIDIFile
from music import Music, Track

'''Create MIDI file for the given Music object.
music(Music): The Music object
outfile(string) = "output.mid": Name of the MIDI file to create.
outdir(string) = "midifiles": Folder to put the MIDI file in'''
def create_MIDI(music, outfile='output.mid', outdir='midifiles'):
    mf = MIDIFile(len(music.tracks))
    drum_tracks = [t for t in music.tracks if t.drum_kit]
    combined_track = Track(drum_kit=True) #TODO: Need to fix
    for t in drum_tracks: combined_track.notes += t.notes
    for trackn, track in enumerate(music.tracks):
        if track in drum_tracks: continue
        mf.addProgramChange(0, trackn, 0, track.instrument)
        time = 0
        mf.addTrackName(trackn, time, "Track" + str(trackn))
        mf.addTempo(trackn, time, music.tempo)
        volume = 100
        channel = 10 if track.drum_kit else trackn
        for n in track.notes:
            mf.addNote(trackn, channel, n.pitch, n.time, n.duration, volume)
    with open(outdir+'/'+outfile, 'wb') as outf:
        mf.writeFile(outf)