from geneticUtil import geneticUtil


'''
For the genetc algorithm we will evaaluate the songs by eithe 4 measures or 8 measures
'''

NOTE_RANAGE = 49

class Genetic:

    def __init__(self, smaple) -> None:
        self.population = []
        self.util = geneticUtil()

    def mutation(self):
        pass

    def crossover(self):
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

    # get 8 meaasures of melody
    def getMelody(self):
        pass

    # extract features of a piece of melody
    def melodyFeatureExtraction(self):
        pass

    # measures how often repating measures occur in this piece
    # if the same measure occurs often in this piece means this piece is more self similar 
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

        mu = (1/len(measures) * sum(measureDict.values()))
        score = max(1, 2*mu / totalNotes)
        return score

    # there are 5 representations of melody shapes
    # Flat, Rising, Falling, TopArc, and BottomArc
    def melodyShape(self, measures):
        length = self.util.getNotesLength(measures)
        for measure in measures:
            length += len(measure)
        m_max = NOTE_RANAGE / length

        # Divide the 8 measure into 4 sub measures
        sectionOne = measures[:2]
        sectionTwo = measures[2:4]
        sectionThree = measures[4:6]
        sectionFour = measures[6:]
        modelOne = self.util.calcRegression(sectionOne)
        modelTwo = self.util.calcRegression(sectionTwo)
        modelThree = self.util.calcRegression(sectionThree)
        modelFour = self.util.calcRegression(sectionFour)
        typeOne = self.util.getTypeViaMSE(modelOne)
        typeTwo = self.util.getTypeViaMSE(modelTwo)
        typeThree = self.util.getTypeViaMSE(modelThree)
        typeFour = self.util.getTypeViaMSE(modelFour)
        return [typeOne, typeTwo, typeThree, typeFour]

    def melodyLinearity(self, measures):
        pass

    def melodyKeyPrevalence(self, measures):
        pass

    def melodyRangeOfPitch(self, measures):
        pass

    def melodyIntervalClassPrevalence(self, measures):
        pass  

    def melodyEvaluation(self, measures):
        pass

    def run(self):
        pass

    # TBD
    def chordsEvaluation(self):
        pass
