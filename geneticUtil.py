import numpy as np
from sklearn.linear_model import LinearRegression

FLAT_MELODY = [[24, 26, 24, 24, 24, 23, 21, 19], [21, 19, 18, 19, 20, 23, 24, 23], [24]]
RISING_MELODY = [[-6, -5, -3, -1, 0, 4, 7, 9], [12, 11, 12, 16, 19, 18, 19, 23], [24]]
FALLING_MELODY = [[33, 28, 26, 24, 21, 19, 16, 18], [16, 14, 11, 9, 7, 4, 6, 2], [-1]]
TOP_ARC_MELODY = [[7, 9, 9, 12, 14, 16, 19, 21], [19, 18, 19, 12, 11, 9, 6, 4], [2]]
BOTTOM_ARC_MELODY = [[23, 18, 11, 4, 2, -1, 0, 2], [4, 7, 6, 4, 7, 12, 14, 16], [18]]

class geneticUtil:

    def __init__(self) -> None:
        self.flatRegression = self.calcRegression(FLAT_MELODY)
        self.riseRegression = self.calcRegression(RISING_MELODY)
        self.fallRegression = self.calcRegression(FALLING_MELODY)
        self.topArcRegression = self.calcRegression(TOP_ARC_MELODY)
        self.bottomArcRegression = self.calcRegression(BOTTOM_ARC_MELODY)

    def getMeasureEncode(self, measure):
        times = [note[1] for note in measure]
        pitches = [note[0] for note in measure]
        timeDiffs = [""] + [times[n]-times[n-1] for n in range(1,len(times))]
        result = []
        for timeDiff, pitch in zip(timeDiffs, pitches):
            result.append(str(timeDiff))
            result.append(str(pitch))
        code = "".join(result)
        return code

    def getNotesLength(self, measures):
        length = 0
        for measure in measures:
            length += len(measure)
        return length

    def flatten_measures(self, measures):
        measures = np.array(measures)
        flatted = measures.flatten()
        return flatted

    def calcRegression(self, measures):
        notes = self.flatten_measures(measures)
        xVals = np.array([x for x in range(len(notes))]).reshape((-1, 1))
        model = LinearRegression()
        model.fit(xVals, notes)
        return model

    def getMSES(self, model):
        # fit 10 notes to calculate mean square error
        predXVals = np.array([x for x in range(10)]).reshape((-1, 1))
        predctsOne = model.predict(predXVals)
        flatResult = self.flatRegression.predict(predXVals)
        riseResult = self.riseRegression.predict(predXVals)
        fallResult = self.fallRegression.predict(predXVals)
        topResult = self.topArcRegression.predict(predXVals)
        bottomResult = self.bottomArcRegression.predict(predXVals)

        mseFlat = np.mean((predctsOne - flatResult)**2)
        mseRise = np.mean((predctsOne - riseResult)**2)
        mseFall = np.mean((predctsOne - fallResult)**2)
        mseTop = np.mean((predctsOne - topResult)**2)
        mseBottom = np.mean((predctsOne - bottomResult)**2)
        mses = [mseFlat, mseRise, mseFall, mseTop, mseBottom]
        return mses
            


