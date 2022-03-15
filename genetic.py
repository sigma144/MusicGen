from geneticUtil import geneticUtil as util

'''
For the genetc algorithm we will evaaluate the songs by eithe 4 measures or 8 measures
'''

NOTE_RANAGE = 49

class genetic:

    def __init__(self, smaple) -> None:
        self.population = []

    def mutation():
        pass

    def crossover():
        pass

    # TBD
    def getChords():
        pass

    # get 8 measures of rhythm
    def getRhythm():
        pass

    # measures are passed in as an 2d array
    # each subarray is a measure, a measure is an array of tuples(notes), each tuple has (pitch, time) information
    def rhythmEvaluation(measures):
        pass

    # get 8 meaasures of melody
    def getMelody():
        pass

    # extract features of a piece of melody
    def melodyFeatureExtraction():
        pass

    # measures how often repating measures occur in this piece
    # if the same measure occurs often in this piece means this piece is more self similar 
    def melodySelfSimilarity(measures):
        measureDict = {}
        totalNotes = 0
        for measure in measures:
            totalNotes += len(measure)
            measureEncode = util.getMeasureEncode(measure)
            if measureEncode in measureDict:
                measureDict[measureEncode] += 1
            else:
                measureDict[measureEncode] = 1

        mu = (1/len(measures) * sum(measureDict.values()))
        score = max(1, 2*mu / totalNotes)
        return score

    # there are 5 representations of melody shapes
    # Flat, Rising, Falling, TopArc, and BottomArc
    def melodyShape(measures):
        pass      

    def melodyLinearity(measures):
        pass

    def melodyKeyPrevalence(measures):
        pass

    def melodyRangeOfPitch(measures):
        pass

    def melodyIntervalClassPrevalence(measures):
        pass  

    def melodyEvaluation(measures):
        pass

    def run():
        pass

    # TBD
    def chordsEvaluation():
        pass
