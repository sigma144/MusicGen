from samples import Samples
from midi import create_MIDI
import os

SAMPLE_DIR = "samples"
SAMPLE_FILENAME = "sample1"

if not os.path.exists(SAMPLE_DIR):
    os.mkdir(SAMPLE_DIR)

# sample = Samples.sample1()
# filepath = os.path.join(SAMPLE_DIR, SAMPLE_FILENAME)
# create_MIDI(sample, filepath)

sample = Samples.sample2()
filepath = os.path.join(SAMPLE_DIR, "sample3")
create_MIDI(sample, filepath)
