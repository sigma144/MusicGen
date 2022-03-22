from geneticUtil import geneticUtil
from music import Music


'''
For the genetc algorithm we will evaaluate the songs by eithe 4 measures or 8 measures
'''

NOTE_RANAGE = 49
FOUR_OCTAVE_RANGE = [[12, 24], [24, 36], [36, 48], [48, 60]]

class Genetic:

    def __init__(self) -> None:
        self.population = []
        self.util = geneticUtil()
        self.flattend = []

    def initPopulation(self):

        self.population = []

    def run(self):
        pass

    def mutation(self):
        pass

    # TBD
    def crossover(self):
        pass

    # Get 8 meaasures of melody from music object
    def getMelody(self):
        pass

    def setFlattend(self, measures):
        self.flattend = self.until.flatten_measures(measures)
    # measures how often repating measures occur in this piece
    # if the same measure occurs often in this piece means this piece is more self similar 
    # return between 0 and 1
    def melodySelfSimilarity(self, measures):
        measureDict = {}
        totalNotes = 0
        for measure in measures:
            totalNotes += len(measure)
            measureEncode = self.util.getMeasureEncode(measure)
            if measureEncode in measureDict:
                measureDict[measureEncode] += 1
            else:
                measureDict[measureEncode] = 1

        score = max(measureDict.values()) / len(measures) 
        return score

    # there are 5 representations of melody shapes
    # Flat, Rising, Falling, TopArc, and BottomArc
    def melodyShape(self, measures):
        # Divide the 8 measure into 4 sub measures
        sections = [measures[:2], measures[2:4], measures[4:6], measures[6:]]
        result = []
        for section in sections:
            flatSection = self.util.flatten_measures(section)
            sectionLength = len(flatSection)
            model = self.util.calcRegression(section)
            # get mses of different type of shapes
            mses = self.util.getMSES(model)
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
            lap_response = self.flattened[i-1] * beta + self.flattened[i] * k + self.flattened[i+1] * beta
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
            if checkerMusic.is_in_scale(note[0]):
                inMajor += 1
        return inMajor/len(self.flattened)

    # return a score between 0 and 1
    def melodyRangeOfPitch(self, r=2):
        inRange = 0
        for note in self.flattened:
            # Pass in pitch
            if FOUR_OCTAVE_RANGE[0][1] < note[0] < FOUR_OCTAVE_RANGE[0][1]:
                inRange += r
            elif FOUR_OCTAVE_RANGE[1][1] < note[0] < FOUR_OCTAVE_RANGE[1][1]:
                inRange += r
            elif FOUR_OCTAVE_RANGE[2][1] < note[0] < FOUR_OCTAVE_RANGE[2][1]:
                inRange += 1
            elif FOUR_OCTAVE_RANGE[3][1] < note[0] < FOUR_OCTAVE_RANGE[3][1]:
                inRange += 1
            else:
                continue
        return inRange/(len(self.flattened) * r)

    # decide life and death of the children
    def melodyEvaluation(self, measures):
        pass

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
