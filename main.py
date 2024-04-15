import json

trainingFile = open("Data/trainFinal.jsonl", "r")
#trainingLines = trainingFile.readlines()
trainingData = json.loads(trainingFile.read())
trainingFile.close()

outputFile = open("output.tsv", "w")

id = 0

for i in range(len(trainingData)):

  thingToCheck = trainingData[i]["tags"][0]

  if thingToCheck == "phrase":
      label = 0
  elif thingToCheck == "passage":
      label = 1
  elif thingToCheck == "multi":
      label = 2

  paragraphs = ""
  for sentence in trainingData[i]["targetParagraphs"]:
        paragraphs = paragraphs + " " + sentence

  outputFile.write('(' + str(id) + ", " + str(label) + ', "a", "' + trainingData[i]["postText"][0] + paragraphs + '"),\n')

  # for sentence in trainingData[i]["targetParagraphs"]:
  #     outputFile.write(sentence + " ")

  # outputFile.write("\n")

  id += 1

outputFile.close()