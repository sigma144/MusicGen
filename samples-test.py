from samples import Samples
from midi import create_MIDI

# sample = Samples.sample2()
# create_MIDI(sample, outfile="sample2", outdir="samples")

# sample = Samples.chord_progression_generator()
# create_MIDI(sample, outfile="chord_progression_2", outdir="samples")

sample = Samples.chord_progression_generator_scale()
create_MIDI(sample, outfile="chord_progression_3", outdir="samples")
