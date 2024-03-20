import json

if __name__ == "__main__":

    #
    # This section below reads the <train/validation/test>Final.jsonl file and returns the
    # uuid of each document and the number of documents in that file
    # Just replace validationFinal with the file you want to read
    #
    trainingFile = open("Data/trainFinal.jsonl", "r")
    trainingData = json.loads(trainingFile.read())
    trainingFile.close()

    count = 0

    for i in range(len(trainingData)):
        print(trainingData[i]["uuid"])
        count += 1

    print(count)
