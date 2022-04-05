import numpy as np
import math
from sklearn.linear_model import LinearRegression

FLAT_MELODY = [[24, 26, 24, 24, 24, 23, 21, 19], [21, 19, 18, 19, 20, 23, 24, 23], [24]]; FLAT_RANGE = [18, 26]
RISING_MELODY = [[-6, -5, -3, -1, 0, 4, 7, 9], [12, 11, 12, 16, 19, 18, 19, 23], [24]]; RISING_RANGE = [-6, 23]
FALLING_MELODY = [[33, 28, 26, 24, 21, 19, 16, 18], [16, 14, 11, 9, 7, 4, 6, 2], [-1]]; FALLING_RANGE = [2, 33]
TOP_ARC_MELODY = [[7, 9, 9, 12, 14, 16, 19, 21], [19, 18, 19, 12, 11, 9, 6, 4], [2]]; TOP_ARC_RANGE = [2, 21]
BOTTOM_ARC_MELODY = [[23, 18, 11, 4, 2, -1, 0, 2], [4, 7, 6, 4, 7, 12, 14, 16], [18]]; BOTTOM_ARC_RANGE = [-1, 23]

class geneticUtil:

    def __init__(self) -> None:
        self.flatRegression = self.calcRegression(self.flatten_measures(FLAT_MELODY))
        self.riseRegression = self.calcRegression(self.flatten_measures(RISING_MELODY))
        self.fallRegression = self.calcRegression(self.flatten_measures(FALLING_MELODY))
        self.topArcRegression = self.calcRegression(self.flatten_measures(TOP_ARC_MELODY))
        self.bottomArcRegression = self.calcRegression(self.flatten_measures(BOTTOM_ARC_MELODY))

    def getMeasureEncode(self, measure):
        times = [note.time for note in measure]
        pitches = [note.pitch for note in measure]
        timeDiffs = [""] + [abs(math.floor(times[n]-times[n-1])) for n in range(1,len(times))]
        result = []
        for timeDiff, pitch in zip(timeDiffs, pitches):
            if timeDiff  != "":
                result.append('-' + str(timeDiff) + '-')
            result.append(str(pitch))
        code = "".join(result)
        return code

    def getNotesLength(self, measures):
        length = 0
        for measure in measures:
            length += len(measure)
        return length

    def flatten_measures(self, measures):
        flatted = []
        for measure in measures:
            flatted = flatted + measure
        return flatted

    def calcRegression(self, measures):
        notes = np.array(measures)
        xVals = self.getValsInRange(len(notes), 0, 16)
        model = np.polyfit(xVals, notes, 3)
        p = np.poly1d(model)
        # print("xVals\n",xVals)
        # print("Notes\n",notes)
        # result = p(xVals)
        # print(result)
        return p

    def getValsInRange(self, numVals, minVal, maxVal):
        return np.array([x for x in np.arange(minVal, maxVal+0.00001, (maxVal-minVal)/(numVals-1))])
                
    def getMSES(self, model):
        # fit 10 notes to calculate mean square error
        predXValsForFlat = self.getValsInRange(17, 0, 16)
        predXValsForRise = self.getValsInRange(17, 0, 16)
        predXValsForFall = self.getValsInRange(17, 0, 16)
        predXValsForTop = self.getValsInRange(17, 0, 16)
        predXValsForBottom = self.getValsInRange(17, 0, 16)
        flatResult = self.flatRegression(predXValsForFlat)
        riseResult = self.riseRegression(predXValsForRise)
        fallResult = self.fallRegression(predXValsForFall)
        topResult = self.topArcRegression(predXValsForTop)
        bottomResult = self.bottomArcRegression(predXValsForBottom)
        predXVals = self.getValsInRange(17, 0, 16)
        predicts = model(predXVals)
        # print(predicts)
        # print(flatResult)
        # print(riseResult)
        # print(fallResult)
        # print(topResult)
        # print(bottomResult)
        # we need to do a shifting on y direction to fit the shape
        mseFlat = np.mean(((predicts - abs(flatResult[0] - predicts[0])) - flatResult)**2)
        mseRise = np.mean(((predicts - abs(riseResult[0] - predicts[0])) - riseResult)**2)
        mseFall = np.mean(((predicts - abs(fallResult[0] - predicts[0])) - fallResult)**2)
        mseTop = np.mean(((predicts - abs(topResult[0] - predicts[0])) - topResult)**2)
        mseBottom = np.mean(((predicts - abs(bottomResult[0] - predicts[0])) - bottomResult)**2)
        mses = [mseFlat, mseRise, mseFall, mseTop, mseBottom]
        # nomalize mse value
        maxVal = max(mses)
        mses = [x/maxVal for x in mses]
        return mses

    # check dimension of a python list
    def dim(self, a):
        if not type(a) == list:
            return []
        return [len(a)] + self.dim(a[0])

    def printPopulation(self, population):
        for p in population:
            print("id: ", p.id)
            print("score: ", p.score)

    def printBest(self, population):
        p = population[0]
        print("best child with id {} score {}".format(p.id, p.score))