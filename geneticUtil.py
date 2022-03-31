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
        self.flatRegression = self.calcRegression(FLAT_MELODY)
        self.riseRegression = self.calcRegression(RISING_MELODY)
        self.fallRegression = self.calcRegression(FALLING_MELODY)
        self.topArcRegression = self.calcRegression(TOP_ARC_MELODY)
        self.bottomArcRegression = self.calcRegression(BOTTOM_ARC_MELODY)

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
        notes = np.array(self.flatten_measures(measures))
        notes = notes.reshape((-1, 1))
        xVals = np.array([x for x in range(len(notes))]).reshape((-1, 1))
        model = LinearRegression()
        #print("measures\n",measures)
        #print("xVals\n",xVals)
        #print("Notes\n",notes)
        model.fit(xVals, notes)
        return model

    def getMSES(self, model, minVal, maxVal):
        # fit 10 notes to calculate mean square error
        #predXVals = np.array([x for x in range(10)]).reshape((-1, 1))
        #predctsOne = model.predict(predXVals)
        def getValsInRange(numVals, minVal, maxVal):
            return np.array([x for x in np.arange(minVal, maxVal+0.00001, (maxVal-minVal)/(numVals-1))]).reshape((-1, 1))
        predXVals = getValsInRange(10, minVal, maxVal)
        predctsOne = model.predict(predXVals)
        predXValsForFlat = getValsInRange(10, FLAT_RANGE[0], FLAT_RANGE[1])
        predXValsForRise = getValsInRange(10, RISING_RANGE[0], RISING_RANGE[1])
        predXValsForFall = getValsInRange(10, FALLING_RANGE[0], FALLING_RANGE[1])
        predXValsForTop = getValsInRange(10, TOP_ARC_RANGE[0], TOP_ARC_RANGE[1])
        predXValsForBottom = getValsInRange(10, BOTTOM_ARC_RANGE[0], BOTTOM_ARC_RANGE[1])
        flatResult = self.flatRegression.predict(predXValsForFlat)
        riseResult = self.riseRegression.predict(predXValsForRise)
        fallResult = self.fallRegression.predict(predXValsForFall)
        topResult = self.topArcRegression.predict(predXValsForTop)
        bottomResult = self.bottomArcRegression.predict(predXValsForBottom)

        mseFlat = np.mean((predctsOne - flatResult)**2)
        mseRise = np.mean((predctsOne - riseResult)**2)
        mseFall = np.mean((predctsOne - fallResult)**2)
        mseTop = np.mean((predctsOne - topResult)**2)
        mseBottom = np.mean((predctsOne - bottomResult)**2)
        mses = [mseFlat, mseRise, mseFall, mseTop, mseBottom]
        return mses
            


