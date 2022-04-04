from socket import SO_LINGER
from geneticUtil import geneticUtil
from midi import create_MIDI
from music import Music, Track
from musicgen import MusicGen
import melodygen
import random
from rhythmgen import SIMPLE
import numpy as np
import accomp
from samples import Samples
import copy

'''
For the genetc algorithm we will evaluate the songs by 8 measures
'''

NOTE_RANAGE = 49
FOUR_OCTAVE_RANGE = [[36, 48], [48, 60], [60, 72], [72, 84]]

class Child:
    def __init__(self, id, song) -> None:
        self.song = song
        self.id = id

class Genetic:

    def __init__(self) -> None:
        self.population = []
        self.util = geneticUtil()
        self.flattened = []
        self.musicGen = MusicGen()
        self.testmusic = Music(tempo = 100)
        self.meter = SIMPLE
        self.chords = Samples().get_chords_from_prog(Samples().chord_prog_generator_scale(progKey=self.testmusic.key, numChords=8), duration=4, repetitions=1)
        self.childId = 0
        self.pSize = 10 # the population size 

    def initPopulation(self):
        # generate population
        for i in range(self.pSize):
            melodytrack = Track()
            melodytrack.notes = melodygen.melody_from_chords(self.testmusic, self.chords, meter=self.meter)
            # pase the music object
            section = melodytrack.split()
            child = Child(self.childId, [section]) # a chilld has mutiple sections
            # print("child dimension: ", i, self.util.dim(child))
            self.population.append(child)
            self.childId += 1

    def run(self, epoch=10):
        self.initPopulation()
        while epoch > 0:
            print("epoch: ", epoch)
            # mutate population, each parent in the population will produce 1 new child
            print("before: ", len(self.population))
            self.mutation()
            print("after: ", len(self.population))
            # calculate fitness of the muatted population
            scoreMap = self.melodyEvaluation()
            self.survival(scoreMap)
            epoch -= 1
        
        # decide the ones to survial
        best = self.population[-1].song[0]
        track = Track().join(best)
        return track

    # this function will kill half of the population that does not meet the requirement
    def survival(self, scoreMap):
        # print(scoreMap)
        # determine the goal maybe we shoudl weight the score, some scores are more important than other
        # remove the children
        pass

    # the mutation algorithm
    def mutation(self):
        for i in range(self.pSize):
            newChildSong = []
            p = self.population[i].song
            for j in range(len(p)):
                # cerate the new children
                newMeasures = copy.deepcopy(p[j])
                # randomly change a note in 8 measures?
                mIndex = random.randint(0, 7)
                measure = newMeasures[mIndex]
                noteIndex = random.randint(0, len(measure)-1)
                # mutate pitch and time
                pitchVariance = random.randint(-5, 5)
                # add a boundary check for pitch
                if newMeasures[mIndex][noteIndex].pitch + pitchVariance < 36:
                    newMeasures[mIndex][noteIndex].pitch = 36
                elif newMeasures[mIndex][noteIndex].pitch + pitchVariance > 84:
                    newMeasures[mIndex][noteIndex].pitch = 84
                else:
                    newMeasures[mIndex][noteIndex].pitch += pitchVariance

                # we do not want to modify the time of the first node or the last node
                # now the time change will only be in between the note before or after it
                if noteIndex != 0 and noteIndex != len(measure)-1:
                    interval = newMeasures[mIndex][noteIndex + 1].time - newMeasures[mIndex][noteIndex - 1].time
                    newTime = newMeasures[mIndex][noteIndex - 1].time + (random.randint(1, 9) / 10) * interval
                    newMeasures[mIndex][noteIndex].time = newTime
                newChildSong.append(newMeasures)
            # append the new child as new population
            self.population.append(Child(self.childId, newChildSong))
            self.childId += 1
            # exit()
                
    # TBD
    def crossover(self):
        pass

    # Get section of measures from song
    def getMelody(self, song):
        pass

    # decide life and death of the children
    def melodyEvaluation(self, prnt=False):
        scoreMap = {}
        for i, p in enumerate(self.population): # go through every children
            sections = p.song
            id = p.id
            for im, measures in enumerate(sections): # go through measures (sections) of a child
                self.setFlattend(measures)
                similarityScore = self.melodySelfSimilarity(measures)
                if prnt: print("similarityScore")
                if prnt: print(similarityScore)
                shapeScores = self.melodyShape(measures) # how to deal with shape scores
                if prnt: print("shapeScores")
                if prnt: print(shapeScores[0])
                if prnt: print(shapeScores[1])
                if prnt: print(shapeScores[2])
                if prnt: print(shapeScores[3])
                linearityScore = self.melodyLinearity()
                if prnt: print("linearityScore")
                if prnt: print(linearityScore)
                prevScore = self.melodyCMajorKeyPrevalence()
                if prnt: print("prevScore")
                if prnt: print(prevScore)
                melodyRangeScore = self.melodyRangeOfPitch()
                if prnt: print("melodyRangeScore")
                if prnt: print(melodyRangeScore)
                # encode and store the scores in a dictionary
                scoreMap[str(id) + "-" + str(im) + "-similarityScore"] = similarityScore
                scoreMap[str(id) + "-" + str(im) + "-shapeScores"] = shapeScores
                scoreMap[str(id) + "-" + str(im) + "-linearityScore"] = linearityScore
                scoreMap[str(id) + "-" + str(im) + "-prevScore"] = prevScore
                scoreMap[str(id) + "-" + str(im) + "-melodyRangeScore"] = melodyRangeScore
        return scoreMap

    def setFlattend(self, measures):
        self.flattened = self.util.flatten_measures(measures)
    # measures how often repating measures occur in this piece
    # if the same two notes patten occurs in this piece means this piece is more self similar 
    # return between 0 and 1, around 0.2 to 0.3, caan be as high as 0.4 to 0.5
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
            # print("two measure: ", flatSection)
            # sectionLength = len(flatSection)
            model = self.util.calcRegression(flatSection)
            # get mses of different type of shapes
            mses = self.util.getMSES(model)
            sectionResult = []
            for mse in mses:
                sectionResult.append(mse)
            result.append(sectionResult)
        return result

    # not sure how many lap response the sum up together, means not sure what n value is in the paper
    # return between 0 and 1, normally betweenn 0.3 to 0.4 can go betwwen 0.2 and 0.5
    def melodyLinearity(self, k=2, beta=1, alpha=0.00000001):
        # abondon the leftmost and right most note (this is kind of like the approach in image processing)
        acc_lap = 0
        for i in range(1, len(self.flattened) - 1):
            lap_response = self.flattened[i-1].pitch * beta + self.flattened[i].pitch * k + self.flattened[i+1].pitch * beta
            acc_lap += lap_response
        # print("acc_lap", acc_lap)
        linearity = (alpha * (acc_lap**2)) / (alpha * (acc_lap**2) + 1)
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

    # return a score between 0 and 1, typically around 0.3 to 0.45
    def melodyRangeOfPitch(self, r=2):
        inRange = 0
        for note in self.flattened:
            # Pass in pitch
            if FOUR_OCTAVE_RANGE[0][0] < note.pitch < FOUR_OCTAVE_RANGE[0][1]:
                inRange += r
            elif FOUR_OCTAVE_RANGE[1][0] < note.pitch < FOUR_OCTAVE_RANGE[1][1]:
                inRange += r
            elif FOUR_OCTAVE_RANGE[2][0] < note.pitch < FOUR_OCTAVE_RANGE[2][1]:
                inRange += 1
            elif FOUR_OCTAVE_RANGE[3][0] < note.pitch < FOUR_OCTAVE_RANGE[3][1]:
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
    genetic = Genetic()
    music_obj = []
    for i in range(1):
        testmusic = Music()
        chordtrack = Track(instrument = 49, volume=50)
        chordtrack.notes = accomp.accomp_from_chords(genetic.chords, style=accomp.CHORDS)
        testmusic.tracks.append(chordtrack)
        melody = genetic.run(epoch=1)
        testmusic.tracks.append(melody)
        music_obj.append(testmusic)
    create_MIDI(music_obj, "genetic.mid")

    # music_obj = []
    # for i in range(4):
    #     testmusic2 = Music()
    #     melodytrack = Track()
    #     melodytrack.notes = melodygen.melody_from_chords(testmusic2, genetic.chords, meter=genetic.meter)
    #     testmusic2.tracks.append(melodytrack)
    #     testmusic2.tracks.append(chordtrack)
    #     music_obj.append(testmusic2)
    # create_MIDI(music_obj, "geneticbaseline.mid")
