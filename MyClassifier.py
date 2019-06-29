# Import python libraries
import sys
import os
import numpy as np

def sortFirst(val):
    return val[0]

def FindDistance(test, point):
    distance = 0
    for i in range(len(test)):
        if type(test[i]) is not str:
            distance += (test[i]-point[i])*(test[i]-point[i])
    return distance

# Tests the test data against 'data' using the testType selected.
# NB for Naive Briers, and Nx for x nearest neighbours.
def Clasifier(test, data, testType):
    if testType == "NB":
        # Naive Briers

        # Find probability of each class by itself
        # Need to find mean and standard deviation of each atribute
        yestotal = 0
        nototal = 0
        for i in range(len(data)):
            if data[i][-1] == "yes":
                yestotal += 1
            else:
                nototal += 1
        probs = []
        for i in range(len(data[0])-1):
            sumy = 0
            sumn = 0
            #print("mean")
            for j in range(len(data)):
                if data[j][-1] == "yes":
                    sumy += data[j][i]
                    #print(data[j][i])
                else:
                    sumn += data[j][i]
            meany = sumy/yestotal
            meann = sumn/nototal
            #print(meany)
            stdsumy = 0
            stdsumn = 0
            #print("std")
            for j in range(len(data)):
                if data[j][-1] == "yes":
                    stdsumy += (meany - data[j][i])*(meany - data[j][i])
                    #print((meany - data[j][i])*(meany - data[j][i]))
                else:
                    stdsumn += (meann - data[j][i])*(meann - data[j][i])

            stdy = np.sqrt(stdsumy/(yestotal-1))
            stdn = np.sqrt(stdsumn/(nototal-1))
            #print(stdy)

            probs.append([meany, stdy, meann, stdn])

        probs.append([yestotal/len(data),nototal/len(data)])

        # Go through tests and compare yes/no probabilities
        for t in test:
            ysum = 1
            nsum = 1
            for i in range(len(t)):
                if type(t[i]) is not str:
                    ysum = ysum*((1/np.sqrt(2*np.pi)/probs[i][1])*np.power(np.e,-((t[i]-probs[i][0])*(t[i]-probs[i][0])/(2*probs[i][1]*probs[i][1]))))
                    nsum = nsum*((1/np.sqrt(2*np.pi)/probs[i][3])*np.power(np.e,-((t[i]-probs[i][2])*(t[i]-probs[i][2])/(2*probs[i][3]*probs[i][3]))))
            yprob = ysum*probs[-1][0]
            nprob = nsum*probs[-1][1]

            if yprob > nprob:
                if len(t) == len(data[0]):
                    t[-1] = "yes"
                else:
                    t.append("yes")
            else:
                #print("no", end = '')
                if len(t) == len(data[0]):
                    t[-1] = "no"
                else:
                    t.append("no")
        return test

    else:

        ## K nearest neighbours ##
        # Get how many neighbours,
        k = float(testType[:-2])


        for value in test:

            neighbours = []

            # Get the neighbours
            for point in data:
                distance = FindDistance(value, point)
                if len(neighbours) < k:
                    neighbours.append([distance, point[-1]])
                    neighbours.sort(key = sortFirst)
                else:
                    if neighbours[-1][0] > distance:
                        neighbours[-1] = [distance, point[-1]]
                        neighbours.sort(key = sortFirst)
            # Find predicted class
            yes = 0
            no = 0
            for n in neighbours:
                if n[1] == "yes":
                    yes += 1
                else:
                    no += 1
            if yes > no:
                #print("yes", end = '')
                if len(value) == len(data[0]):
                    value[-1] = "yes"
                else:
                    value.append("yes")
            else:
                #print("no", end = '')
                if len(value) == len(data[0]):
                    value[-1] = "no"
                else:
                    value.append("no")
        return test

def Printing(result):
    for value in result:
        print(value[-1])


def main():
    # Inport system arguments
    input = sys.argv

    # Initiate variables
    data = []
    # It will look like:
    #[[0.2,0.1,0.9,yes],
    #[0.5,0.6,0.7,no]]

    # Access "no" by going: data[1][3]

    test = []
    # It will look like:
    #[[0.2,0.1,0.9],
    #[0.5,0.6,0.7]]

    # Append our predictions to the end of each array so it looks like data
    # This will be done with test[position].append("yes")


    # Learning data
    #if not os.path.isfile(input[1]):
    #    print("Invalid path to data file.")
    #    exit()
    # Follow correct filepath and import files
    #else:
        # Import the data file
    with open(input[1]) as dataFile:
        for Line in dataFile:
            toAdd = Line.strip("\n").split(",")
            for i in range(len(toAdd)-1):
                toAdd[i] = float(toAdd[i])
            data.append(toAdd)

    # Testing data
    #if os.path.isfile(input[2]):
    #    print("Invalid path to testing file.")
    #    exit()
    # Follow correct filepath and import files
    #else:
    # Import the testing file
    with open(input[2]) as dataFile:
        for Line in dataFile:
            toAdd = Line.strip("\n").split(",")
            for i in range(len(toAdd)):
                if toAdd[i] != "yes" and toAdd[i] != "no":
                    toAdd[i] = float(toAdd[i])
            test.append(toAdd)


    Printing(Clasifier(test,data,input[3]))

if __name__ == "__main__":
    main()
