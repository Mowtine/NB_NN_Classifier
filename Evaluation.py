# Import python libraries
import sys
import os
import copy

import MyClassifier

# Splits the data into the amounts shown by split
def SplitnStrat(data, split):
    splitData = [[] for i in range(split)]
    yesData = []
    noData = []
    for value in data:
        if value[-1] == "no":
            noData.append(value)
        else:
            yesData.append(value)
    while len(noData) + len(yesData) > 0:
        for i in range(split):
            if len(noData) + len(yesData) > 0:
                if len(noData) != 0:
                    splitData[i].append(noData.pop())
                else:
                    splitData[i].append(yesData.pop())
            else:
                break
    return splitData


# run script with: 'python Evaluation.py <how many splits for stratification>'
def main():
    # Inport system arguments
    input = sys.argv

    # Initiate variables

    # It will look like:
    #[[0.2,0.1,0.9,yes],
    #[0.5,0.6,0.7,no]]

    splits = int(input[1])

    for file in ["pima.csv", "pima-CFS.csv"]:

        data = []
        print()
        print(file)
        # Learning data
        if not os.path.isfile(file):
            print("Invalid path to the data file.")
            exit()
        # Follow correct filepath and import files
        else:
            # Import the data file
            with open(file) as dataFile:
                for Line in dataFile:
                    toAdd = Line.strip("\n").split(",")
                    for i in range(len(toAdd)-1):
                        toAdd[i] = float(toAdd[i])
                    data.append(toAdd)

        # Stratify data and split it
        splitData = SplitnStrat(data, splits)

        # Run the tests
        for nn in [1, 5]:
            percent = 0
            for i in range(splits):
                test = copy.deepcopy(splitData[i])
                testData = splitData[i]
                use = []
                for j in range(splits):
                    if j != i:
                        use = use + splitData[j]
                # Run the clasifier
                results = MyClassifier.Clasifier(test,use,str(nn)+"NN")

                prcnt = 0
                for j in range(len(results)):
                    if results[j][-1] == splitData[i][j][-1]:
                        prcnt += 1
                percent += prcnt*100/len(results)
            percent = percent/splits
            print(str(nn)+" neighbours")
            print(percent)

        # Run the tests
        percent = 0
        for i in range(splits):
            test = copy.deepcopy(splitData[i])
            testData = splitData[i]
            use = []
            for j in range(splits):
                if j != i:
                    use = use + splitData[j]
            # Run the clasifier
            results = MyClassifier.Clasifier(test,use,"NB")

            prcnt = 0
            for j in range(len(results)):
                if results[j][-1] == splitData[i][j][-1]:
                    prcnt += 1
            percent += prcnt*100/len(results)
        percent = percent/splits
        print("Byres")
        print(percent)


if __name__ == "__main__":
    main()
