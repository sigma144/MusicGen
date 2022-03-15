class geneticUtil:

    def getMeasureEncode(measure):
        times = [note[1] for note in measure]
        pitches = [note[0] for note in measure]
        timeDiffs = [None] + [times[n]-times[n-1] for n in range(1,len(times))]
        result = []
        for timeDiff, pitch in zip(timeDiffs, pitches):
            if timeDiff: 
                result.append(str(timeDiff))
            result.append(str(pitch))
        code = "".join(result)
        return code