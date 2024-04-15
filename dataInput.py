import json

# Function used for classifying the current document
# currently based only on the postText field
def categorize(thingToCheck):

    for i in range(1,20):
        if str(i) in thingToCheck:
            return "multi"

    for token in ["what", "who", "when", "where", "why", "how", "did you", "have you"]:
        if token in thingToCheck:
            return "passage"

    return "phrase"

if __name__ == "__main__":

    # Read the data from the training/validation/test corpus file
    trainingFile = open("Data/trainFinal.jsonl", "r")
    #trainingLines = trainingFile.readlines()
    trainingData = json.loads(trainingFile.read())
    trainingFile.close()

    #outputFile = open("Data/train.tsv", "w")

    id = 0

    countDoNotMatch = 0
    count = 0
    countCorrectMulti = 0
    countCorrectPassage = 0
    countCorrectPhrase = 0
    countWrong = 0
    countChecking = 0
    countMulti = 0
    countPassage = 0
    countPhrase = 0

    # print(trainingData[i]["postText"][0] + "\n")
    #         print("Spoiler: \n")
    #         for line in trainingData[i]["spoiler"]:
    #             print(line + "\n")

    #         print("-----------\n")

    for i in range(len(trainingData)):

        # thingToCheck = trainingData[i]["tags"][0]

        # if thingToCheck == "phrase":
        #     label = 0
        # elif thingToCheck == "passage":
        #     label = 1
        # elif thingToCheck == "multi":
        #     label = 2
            

        # for i in range(len(trainingData)):
        count += 1
        thingToCheck = trainingData[i]["postText"][0].lower()
            
        spoilerType = categorize(thingToCheck)

        if trainingData[i]["tags"][0] == "phrase":
            countPhrase += 1
            if spoilerType == "phrase":
                countCorrectPhrase += 1
        elif trainingData[i]["tags"][0] == "passage":
            countPassage += 1
            if spoilerType == "passage":
                countCorrectPassage += 1
        elif trainingData[i]["tags"][0] == "multi":
            countMulti += 1
            if spoilerType == "multi":
                countCorrectMulti += 1

        # if trainingData[i]["tags"][0] != "multi":
            #countMulti += 1

        for i in range(1,20):
            if str(i) in thingToCheck:
                countChecking += 1
                break

        #     for token in ["what", "who", "when", "where", "why", "how", "did you", "have you"]:
        #         if token in thingToCheck:
        #             countChecking += 1

        # for sentence in trainingData[i]["targetParagraphs"]:
        #     outputFile.write(sentence + " ")

        # outputFile.write("\n")

        # id += 1

        # if trainingData[i]["postText"][0] == trainingData[i]["targetTitle"]:
        #     countDoNotMatch += 1

    #outputFile.close()

    # print(countDoNotMatch)

    # # Initialize counts
    # count = 0
    # countCorrect = 0
    # countWrong = 0
    #countMultiActual = 0
    #countMultiCounting = 0
    #countPhraseActual = 0
    #ountPhraseCounting = 0
    #ountPassageActual = 0
    #countPassageCounting = 0

    # Process each document in the selected corpus
    # for i in range(len(trainingData)):
    #     count += 1
    #     thingToCheck = trainingData[i]["postText"][0].lower()
            
    #     spoilerType = categorize(thingToCheck)

    #     if trainingData[i]["tags"][0] == spoilerType:
    #         countCorrect += 1

    #     else:
    #         countWrong += 1

    """ This Section Not Being Used Right Now:
    for i in range(len(trainingData)):
        count += 1
        thingToCheck = trainingData[i]["targetTitle"].lower()

        if trainingData[i]["tags"][0] == "multi":
            countMultiActual += 1

            if any(char.isdigit() for char in thingToCheck):
                countMultiCounting += 1

        elif trainingData[i]["tags"][0] == "phrase":
            countPhraseActual += 1

            if any(char.isdigit() for char in thingToCheck):
                countPhraseCounting += 1

        else:
            countPassageActual += 1

            if any(char.isdigit() for char in thingToCheck):
                countPassageCounting += 1
    """

    # Print results
    print(countCorrectPassage)
    print(countCorrectPassage/countPassage)
    print(countCorrectPhrase)
    print(countCorrectPhrase/countPhrase)
    print(countCorrectMulti)
    print(countCorrectMulti/countMulti)
    print(countChecking)
    print(countChecking/count)

    #print(count)
    #print(countMultiActual)
    #print("Number Counted as Multi:")
    #print(countMultiCounting)
    #print(countMultiCounting/countMultiActual)
    #print("Number Counted as Non Multi")
    #print(count)
    #print(countWrong/countNonMulti)
    #print((countMultiCounting/countMultiActual)/(countWrong/countNonMulti))
    #print("Count Non Multi:")
    #print(countNonMulti)

# inputFile = open("train.tsv", "r")
# inputLines = inputFile.readlines()
# inputFile.close()

# outputFile = open("Data\output.tsv", "w")

# for line in inputLines:
#     newLine = line.split()
#     newText = "(" + newLine[0] + "," + newLine[1] + "," + newLine[2] + "," + newLine[3] + "),\n"
#     outputFile.write(newText)

# outputFile.close()