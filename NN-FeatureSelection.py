import math
import copy


def NNClassifier(inpData, currDataPt, remainderFeatures, instanceCount):
    nNeigh = 0
    distSmallest = float('inf')

    for i in range(instanceCount):
        if currDataPt == i:
            pass
        else:
            ValueOfDist = 0
            for j in range(len(remainderFeatures)):
                ValueOfDist = ValueOfDist + pow((inpData[i][remainderFeatures[j]] - inpData[currDataPt][remainderFeatures[j]]), 2)

            ValueOfDist = math.sqrt(ValueOfDist)

            if ValueOfDist < distSmallest:
                nNeigh = i
                distSmallest = ValueOfDist

    return nNeigh


def accuracyOneOut(inpData, remainderFeatures, instanceCount):
    correct = 0.0

    for i in range(instanceCount):
        currOO = i
        neighbor = NNClassifier(inpData, currOO, remainderFeatures, instanceCount)

        if inpData[neighbor][0] == inpData[currOO][0]:
            correct = correct + 1

    accuracy = (correct / instanceCount) * 100

    return accuracy


def forwardSelection(inpData, instanceCount, featureCount):
    remainderFeatures = []
    fnlFeatures = []
    topAccuracy = 0.0

    for i in range(featureCount):
        add_this = -1
        local_add = -1
        localAccuracy = 0.0
        for j in range(1, featureCount + 1):
            if j not in remainderFeatures:
                temp_subset = copy.deepcopy(remainderFeatures)
                temp_subset.append(j)

                accuracy = accuracyOneOut(inpData, temp_subset, instanceCount)
                print('\tFor the feature(s) ', temp_subset, ' accuracy is ', accuracy, '%')
                if accuracy > topAccuracy:
                    topAccuracy = accuracy
                    add_this = j
                if accuracy > localAccuracy:
                    localAccuracy = accuracy
                    local_add = j
        if add_this >= 0:
            remainderFeatures.append(add_this)
            fnlFeatures.append(add_this)
            print('\n\nFeature set ', remainderFeatures, ' was best, accuracy is ', topAccuracy, '%\n\n')
        else:
            remainderFeatures.append(local_add)
            print('Feature set ', remainderFeatures, ' was best, accuracy is ', localAccuracy, '%\n\n')

    print('Search Completed!! The best feature subset is', fnlFeatures, ' with an accuracy of : ', topAccuracy, '%')


def backwardElimination(inpData, instanceCount, featureCount, topAcc):
    remainderFeatures = [i + 1 for i in range(featureCount)]
    fnlFeatures = [i + 1 for i in range(featureCount)]
    topAccuracy = topAcc
    for i in range(featureCount):
        remove_this = -1
        local_remove = -1
        localAccuracy = 0.0
        for j in range(1, featureCount + 1):

            if j in remainderFeatures:
                temp_subset = copy.deepcopy(remainderFeatures)

                temp_subset.remove(j)

                accuracy = accuracyOneOut(inpData, temp_subset, instanceCount)
                print('\tUsing feature(s) ', temp_subset, ' accuracy is ', accuracy, '%')
                if accuracy > topAccuracy:
                    topAccuracy = accuracy
                    remove_this = j
                if accuracy > localAccuracy:
                    localAccuracy = accuracy
                    local_remove = j
        if remove_this >= 0:
            remainderFeatures.remove(remove_this)
            fnlFeatures.remove(remove_this)
            print('\n\nFeature set ', remainderFeatures, ' was best, accuracy is ', topAccuracy, '%\n\n')
        else:
            print('\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)')
            remainderFeatures.remove(local_remove)
            print('Feature set ', remainderFeatures, ' was best, accuracy is ', localAccuracy, '%\n\n')

    print('The best Feature Subset is ', fnlFeatures, ' with an accuracy of', topAccuracy, '%')



def main():
    #file = input('Name of File to Test ? ')

    try:
        inpData = open("CS205_SP_2022_SMALLtestdata__48.txt", 'r')
    except:
        raise IOError('' + "file" + ' Was not found. Ending Program')

    inputLnOne = inpData.readline()

    featureCount = len(inputLnOne.split()) - 1

    inpData.seek(0)
    instanceCount = sum(1 for line in inpData)

    inpData.seek(0)

    dataInst = [[] for i in range(instanceCount)]
    for i in range(instanceCount):
        dataInst[i] = [float(j) for j in inpData.readline().split()]

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

    accuracy = accuracyOneOut(dataInst, ftrList, instanceCount)
    if userAlgoSelected == 1:
        forwardSelection(dataInst, instanceCount, featureCount)
    elif userAlgoSelected == 2:
        backwardElimination(dataInst, instanceCount, featureCount, accuracy)
    

if __name__ == '__main__':
    main()