import json

if __name__ == "__main__":
  
    trainFile = open("Data/trainRemoved.txt", "r", encoding="utf16")
    trainLines = trainFile.readlines()
    trainFile.close()
    
    outputFile = open("Data/trainNew.txt", "w")

    outputFile.write("[\n")
    for i in range(len(trainLines) - 1):
        outputFile.write(trainLines[i] + ",")
    outputFile.write(trainLines[len(trainLines) - 1])
    outputFile.write("]")

    outputFile.close()

    #trainingFile = open("Data/train.jsonl", "r")
    #trainingData = json.loads(trainingFile.read())
    #trainingFile.close()

    #print(trainingData)
    #print(len(trainingData))

    #for i in range(len(trainingData)):
    #    print(trainingData[i]["uuid"])