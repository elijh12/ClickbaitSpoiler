import json

# Function used for classifying the current document
# currently based only on the postText field
def categorize(thingToCheck):

    for token in ["what", "who", "when", "where", "why", "wow", "did you", "have you"]:
        if token in thingToCheck:
            if thingToCheck[-1] == "?":
                return "phrase"
            else: 
                return "passage"
        

    for i in range(1,20):
        if str(i) in thingToCheck:
            return "multi"

    return "phrase"

if __name__ == "__main__":

    # Read the data from the training/validation/test corpus file
    trainingFile = open("Data/trainFinal.jsonl", "r")
    trainingData = json.loads(trainingFile.read())
    trainingFile.close()

    # Initialize counts
    count = 0
    countCorrect = 0
    countWrong = 0
    #countMultiActual = 0
    #countMultiCounting = 0
    #countPhraseActual = 0
    #ountPhraseCounting = 0
    #ountPassageActual = 0
    #countPassageCounting = 0

    # Process each document in the selected corpus
    for i in range(len(trainingData)):
        count += 1
        thingToCheck = trainingData[i]["postText"][0].lower()
            
        spoilerType = categorize(thingToCheck)

        if trainingData[i]["tags"][0] == spoilerType:
            countCorrect += 1

        else:
            countWrong += 1

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
    print(countCorrect)
    print(countWrong)
    print(countCorrect/count)

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
