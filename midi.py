from midiutil.MidiFile import MIDIFile
from music import Music, Track

'''Create MIDI file for the given Music object.
music(Music|List<Music>): The Music object(s)
outfile(string) = "output.mid": Name of the MIDI file to create.
outdir(string) = "midifiles": Folder to put the MIDI file in'''
def create_MIDI(music, outfile='output.mid', outdir='midifiles'):
    if type(music) == Music:
        music = [music]
    mf = MIDIFile(max([len(m.tracks) for m in music]) + 1)
    time = 0
    for m in music:
        drum_tracks = [t for t in m.tracks if t.drum_kit]
        combined_track = Track(drum_kit=True)
        for t in drum_tracks: combined_track.notes += t.notes
        trackn = 0
        for track in m.tracks + [combined_track]:
            if track in drum_tracks: continue
            channel = 9 if track.drum_kit else trackn
            mf.addProgramChange(trackn, channel, time, track.instrument)
            mf.addTempo(trackn, time, m.tempo)
            volume = track.volume
            for n in track.notes:
                mf.addNote(trackn, channel, n.pitch, n.time + time, n.duration, volume)
            trackn += 1
            if trackn == 9: trackn += 1
        time += max([t.section_length for t in m.tracks])
    with open(outdir+'/'+outfile, 'wb') as outf:
        mf.writeFile(outf)

