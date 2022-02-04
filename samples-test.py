from samples import Samples
from midi import create_MIDI

sample = Samples.chord_progression_generator()
create_MIDI(sample, outfile="chord_progression_2", outdir="samples")
