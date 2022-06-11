import copy
import math
import sys
import matplotlib.pyplot as plt
import time

class KNN:

    def computeValueOfDist(self,distance, inpData, currDataPt, remainderFeatures, i, j):

        distance = distance + pow((inpData[i][remainderFeatures[j]] - inpData[currDataPt][remainderFeatures[j]]),
                                        2)
        distance = math.sqrt(distance)

        return distance

    def nearestNeigborClassifier(self,inputData, dataPoint, remainderFeatures, instanceCount):
        nearestNeighbor = 0
        smallestDistance = float(sys.maxsize)

        for i in range(instanceCount):
            if dataPoint == i:
                pass
            else:
                distance = 0
                for j in range(len(remainderFeatures)):
                    distance = self.computeValueOfDist(distance, inputData, dataPoint, remainderFeatures, i, j)

                if distance < smallestDistance:
                    nearestNeighbor = i
                    smallestDistance = distance

        return nearestNeighbor

    def accuracyCalculation(self,inputData, remainderFeatures, instanceCount):
        value = 0
        for i in range(instanceCount):
            currOO = i
            neighbor = self.nearestNeigborClassifier(inputData, currOO, remainderFeatures, instanceCount)

            if inputData[neighbor][0] == inputData[currOO][0]:
                value = value + 1

        accuracy = (value / instanceCount) * 100

        return accuracy


def forwardSelection(inputData, instanceCount, featureCount):
    startTime=time.time();
    featuresArray = []
    fnlFeatures = []
    maxAccuracy = 0
    results = {}
    for i in range(featureCount):
        appendValue = -1
        currentAdd = -1
        currentAccuracy = 0
        #newly added
        knn=KNN()
        for j in range(1, featureCount + 1):
            if j not in featuresArray:
                temp = copy.deepcopy(featuresArray) # to keep appending the features add them to a temp array first
                temp.append(j) # add the feature if not present in the temp.
                accuracy = knn.accuracyCalculation(inputData, temp, instanceCount) # calculate the accuracy now for the temp array
                print('\tFor the feature(s) ', temp, ' accuracy is ', accuracy, '%')
                if accuracy > maxAccuracy: # compare with the latest accuracy value
                    maxAccuracy = accuracy
                    appendValue = j
                if accuracy > currentAccuracy:
                    currentAccuracy = accuracy
                    currentAdd = j

        if appendValue >= 0:
            featuresArray.append(appendValue)
            fnlFeatures.append(appendValue)
            print('\n\nFeature set ', featuresArray, ' was best, accuracy is ', maxAccuracy, '%\n\n')
            results[str(featuresArray)] = maxAccuracy
        else:
            featuresArray.append(currentAdd)
            print('Feature set ', featuresArray, ' was best, accuracy is ', currentAccuracy, '%\n\n')
            results[str(featuresArray)] = maxAccuracy


    print('Search Completed!! The best feature subset is', fnlFeatures, ' with an accuracy of : ', maxAccuracy, '%')
    endTime = time.time()
    print('Time taken for execution', round(endTime-startTime,2))
    barGraph(results)

def backwardElimination(inputData, instanceCount, featureCount, predictedAccuracy):
    startTime=time.time();
    results={}
    featuresArray = [i + 1 for i in range(featureCount)] # consider all features in this array
    result = [i + 1 for i in range(featureCount)]# consider all features in this array
    maxAccuracy = predictedAccuracy # Accuracy with all features
    knn=KNN()
    for i in range(featureCount):
        valueToRemove = -1
        currentValueRemove = -1
        currentAccuracy = 0
        for j in range(1, featureCount + 1):

            if j in featuresArray:
                temp = copy.deepcopy(featuresArray) #Copy the array of all features initially
                temp.remove(j) # remove one feature
                accuracy = knn.accuracyCalculation(inputData, temp, instanceCount) # calculate accuracy
                print('\tUsing feature(s) ', temp, ' accuracy is ', accuracy, '%')
                if accuracy > maxAccuracy:
                    maxAccuracy = accuracy
                    valueToRemove = j
                if accuracy > currentAccuracy:
                    currentAccuracy = accuracy
                    currentValueRemove = j
        if valueToRemove >= 0:
            featuresArray.remove(valueToRemove) # remove value if the feature reduces the accuracy or has no impact
            result.remove(valueToRemove)
            results[str(featuresArray)] = maxAccuracy
            print('\n\nFeature set ', featuresArray, ' was best, accuracy is ', maxAccuracy, '%\n\n')
        else:
            featuresArray.remove(currentValueRemove)
            results[str(featuresArray)] = maxAccuracy
            print('Feature set ', featuresArray, ' was best, accuracy is ', currentAccuracy, '%\n\n')
    endTime = time.time()

    print('Time taken for execution', round(endTime - startTime, 2))
    print('The best Feature Subset is ', result, ' with an accuracy of', maxAccuracy, '%')
    barGraph(results)


def barGraph(finalResults):
    # creating the dataset

        features = list(finalResults.keys())
        accuracy = list(finalResults.values())

        fig = plt.figure(figsize = (10, 5))
     # creating the bar plot
        plt.bar(features, accuracy, color ='grey',width=0.3)
        plt.xlabel("Features ")
        plt.ylabel("Accuracy")
        plt.title("feature sets vs accuracy")
        plt.xticks(rotation=15)
        plt.show()


def main():
    #file = input('Name of File to Test ? ')

    try:
        inputData = open("CS205_SP_2022_Largetestdata__38.txt", 'r')
    except:
        raise IOError('' + "file" + ' Was not found. Ending Program')

    inputLnOne = inputData.readline()

    featureCount = len(inputLnOne.split()) - 1

    inputData.seek(0)
    instanceCount = sum(1 for line in inputData)

    inputData.seek(0)

    dataInst = [[] for i in range(instanceCount)]
    for i in range(instanceCount):
        dataInst[i] = [float(j) for j in inputData.readline().split()]

    print
    'Select The Algorithm from the option below:'
    print('1. Forward Selection')
    print('2. Backward Elimination')
    
    userAlgoSelected = int(input())
    
    while userAlgoSelected < 1 or userAlgoSelected > 2:
        print('Only Valid Inputs are 1 and 2. Try Entering the number again.')
        userAlgoSelected = int(input())

    print('Number of given features are ' + str(featureCount) + ' and the number of instances are ' + str(
        instanceCount))


    ftrList = []
    for i in range(1, featureCount + 1):
        ftrList.append(i)
    knn = KNN()
    accuracy = knn.accuracyCalculation(dataInst, ftrList, instanceCount)
    if userAlgoSelected == 1:
        forwardSelection(dataInst, instanceCount, featureCount)
    elif userAlgoSelected == 2:
        backwardElimination(dataInst, instanceCount, featureCount, accuracy)
    

if __name__ == '__main__':
    main()