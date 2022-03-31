from geneticUtil import geneticUtil
from music import Music, Track
from musicgen import MusicGen
import melodygen
import random
from rhythmgen import SIMPLE

from samples import Samples

'''
For the genetc algorithm we will evaaluate the songs by eithe 4 measures or 8 measures
'''

NOTE_RANAGE = 49
FOUR_OCTAVE_RANGE = [[12, 24], [24, 36], [36, 48], [48, 60]]

class Genetic:

    def __init__(self) -> None:
        self.population = []
        self.util = geneticUtil()
        self.flattened = []
        self.musicGen = MusicGen()
        self.testmusic = Music(tempo = 100)
        self.meter = SIMPLE
        self.chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=self.testmusic.key, numChords=8), duration=4, repetitions=1)

    def initPopulation(self):
        # generate 50 population
        for _ in range(50):
            melodytrack = Track()
            melodytrack.notes = melodygen.melody_from_chords(self.testmusic, self.chords, meter=self.meter)
            # pase the music object
            section = melodytrack.split()
            child = [section] # a chilld has mutiple sections
            self.population.append(child)

    def run(self, epoch=10):
        self.initPopulation()
        while epoch >= 0:
            # mutate population
            self.mutation()
            # calculate fitness of the muatted population
            self.melodyEvaluation()
            epoch -= 1
        
        # decide the ones to survial

    # the mutation algorithm
    def mutation(self):
        for i, p in enumerate(self.population):
            for j, measures in enumerate(p):
                # randomly change a note in 8 measures?
                mIndex = random.randint(0, 7)
                measure = measures[mIndex]
                noteIndex = random.randint(0, len(measure)-1)
                # mutate pitch and time
                pitchVariance = random.randint(-10, 10)
                timeVariance = float(random.randint(-10, 10) / 10)
                self.population[i][j][mIndex][noteIndex].pitch += pitchVariance
                self.population[i][j][mIndex][noteIndex].time += timeVariance
                
    # TBD
    def crossover(self):
        pass

    # Get section of measures from song
    def getMelody(self, song):
        pass

    # decide life and death of the children
    def melodyEvaluation(self):
        for p in self.population: # go through every children
            for measures in p: # go through measures (sections) of a child
                self.setFlattend(measures)
                simillarityScore = self.melodySelfSimilarity(measures)
                print("simillarityScore")
                print(simillarityScore)
                shapeScores = self.melodyShape(measures) # how to deal with shape scores
                print("shapeScores")
                print(shapeScores)
                linearityScore = self.melodyLinearity()
                print("linearityScore")
                print(linearityScore)
                prevScore = self.melodyCMajorKeyPrevalence()
                print("prevScore")
                print(prevScore)
                melodyRangeScore = self.melodyRangeOfPitch()
                print("melodyRangeScore")
                print(melodyRangeScore)
            break

    def setFlattend(self, measures):
        self.flattened = self.util.flatten_measures(measures)
    # measures how often repating measures occur in this piece
    # if the same two notes patten occurs in this piece means this piece is more self similar 
    # return between 0 and 1
    def melodySelfSimilarity(self, measures):
        measureDict = {}
        gaps = 0
        flatted = self.util.flatten_measures(measures)
        for i in range(len(flatted)-1): # go through two notes a time
            twoNotes = [flatted[i], flatted[i+1]]
            gaps += 1
            twoNotesEncode = self.util.getMeasureEncode(twoNotes)
            if twoNotesEncode in measureDict:
                measureDict[twoNotesEncode] += 1
            else:
                measureDict[twoNotesEncode] = 1
        
        repetition = 0
        for i, value in measureDict.items():
            if value > 1:
                repetition += value

        score = repetition / gaps
        return score

    # there are 5 representations of melody shapes
    # Flat, Rising, Falling, TopArc, and BottomArc
    # return 4 subsection's scores for each type
    def melodyShape(self, measures):
        measures = [[n.pitch for n in m] for m in measures]
        # Divide the 8 measure into 4 sub measures
        twomeasures = [measures[:2], measures[2:4], measures[4:6], measures[6:]]
        #print(twomeasures)
        result = []
        for twomeasure in twomeasures:
            flatSection = self.util.flatten_measures(twomeasure)
            sectionLength = len(flatSection)
            model = self.util.calcRegression(twomeasure)
            minval = min(twomeasure[0] + twomeasure[1]) 
            maxval = max(twomeasure[0] + twomeasure[1])
            # get mses of different type of shapes
            mses = self.util.getMSES(model, minval, maxval)
            sectionResult = []
            for mse in mses:
                mMax = NOTE_RANAGE / sectionLength
                m = flatSection[-1] - flatSection[0] # m could be negative
                factorOne = 1 - (mMax - m) / 2 * mMax
                factorTwo = 1 - mse**2 / (mse**2 + 10000)
                score = factorOne * factorTwo # not making too much of sense
                sectionResult.append(score)
            result.append(sectionResult)
        return result

    # not sure how many lap response the sum up together, means not sure what n value is in the paper
    # return between 0 and 1
    def melodyLinearity(self, k=2, beta=1, alpha=1):
        # abondon the leftmost and right most note (this is kind of like the approach in image processing)
        acc_lap = 0
        for i in range(1, len(self.flattened) - 1):
            lap_response = self.flattened[i-1].pitch * beta + self.flattened[i].pitch * k + self.flattened[i+1].pitch * beta
            acc_lap += lap_response
        linearity = (alpha * (acc_lap ** 2)) / (alpha * (acc_lap**2) + 1)
        return linearity

    # Since we only have C major, thus, this function will only measure the propotion
    # of the key that stay in C major rather than descrip propotion of different key
    # return a score between 0 and 1
    def melodyCMajorKeyPrevalence(self):
        checkerMusic = Music()
        inMajor = 0
        for note in self.flattened:
            # Pass in pitch
            if checkerMusic.is_in_scale(note.pitch):
                inMajor += 1
        return inMajor/len(self.flattened)

    # return a score between 0 and 1
    def melodyRangeOfPitch(self, r=2):
        inRange = 0
        for note in self.flattened:
            # Pass in pitch
            if FOUR_OCTAVE_RANGE[0][1] < note.pitch < FOUR_OCTAVE_RANGE[0][1]:
                inRange += r
            elif FOUR_OCTAVE_RANGE[1][1] < note.pitch < FOUR_OCTAVE_RANGE[1][1]:
                inRange += r
            elif FOUR_OCTAVE_RANGE[2][1] < note.pitch < FOUR_OCTAVE_RANGE[2][1]:
                inRange += 1
            elif FOUR_OCTAVE_RANGE[3][1] < note.pitch < FOUR_OCTAVE_RANGE[3][1]:
                inRange += 1
            else:
                continue
        return inRange/(len(self.flattened) * r)

    # TBD
    def getChords(self):
        pass

    # get 8 measures of rhythm
    def getRhythm(self):
        pass

    # measures are passed in as an 2d array
    # each subarray is a measure, a measure is an array of tuples(notes), each tuple has (pitch, time) information
    def rhythmEvaluation(self, measures):
        pass

    # TBD
    def chordsEvaluation(self):
        pass

if __name__ == "__main__":
    Genetic().run(1)
