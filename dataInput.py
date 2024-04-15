import json
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
from heapq import nlargest


def summarizePassage(targetParagraphs):
    text = ""
    for i in targetParagraphs:
        text += i

    # print(text)
    # print("\n\n\n\n")

    stopwords = list(STOP_WORDS)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tokens = [token.text for token in doc]
    # print(tokens)

    punctuation = string.punctuation + "\n"
    # print(punctuation)

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    # print(word_frequencies)

    max_frequency = max(word_frequencies.values())
    # print(max_frequency)

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    # print(word_frequencies)

    sentence_tokens = [sent for sent in doc.sents]
    # print(sentence_tokens)

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    # print(sentence_scores)

    select_length = min(int(len(sentence_tokens) * 0.3), 4)
    # select_length = 2
    # print(select_length)

    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    # print(summary)

    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)
    # print(text)

    # print(summary)
    return summary


# Function used for classifying the current document
# currently based only on the postText field
def categorize(thingToCheck):

    for token in ["what", "who", "when", "where", "why", "wow", "did you", "have you"]:
        if token in thingToCheck:
            if thingToCheck[-1] == "?":
                return "phrase"
            else:
                return "passage"

    for i in range(1, 20):
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
    # countMultiActual = 0
    # countMultiCounting = 0
    # countPhraseActual = 0
    # ountPhraseCounting = 0
    # ountPassageActual = 0
    # countPassageCounting = 0

    # Process each document in the selected corpus
    # for i in range(len(trainingData)):
    for i in range(20):
        count += 1
        print("count: ", count)
        # thingToCheck = trainingData[i]["postText"][0].lower()

        # spoilerType = categorize(thingToCheck)

        if trainingData[i]["tags"][0] == "passage":
            text = trainingData[i]["targetParagraphs"]
            # for j in text:
            #     j.replace('"', "'")
            # # print(text)
            summary = summarizePassage(text)
            checkKey = 0
            if trainingData[i]["targetKeywords"] == None:
                summary = summarizePassage(text)
                if trainingData[i]["spoiler"][0] in summary:
                    countCorrect += 1
                else:
                    countWrong += 1
                    print(summary)
                    print(trainingData[i]["spoiler"][0])
                    # break
            else:
                print(
                    trainingData[i]["targetKeywords"].strip(" ").strip(".").split(",")
                )
                for j in (
                    trainingData[i]["targetKeywords"].strip(" ").strip(".").split(",")
                ):
                    if j in summary:
                        checkKey += 1
                if (
                    checkKey
                    / len(
                        trainingData[i]["targetKeywords"]
                        .strip(" ")
                        .strip(".")
                        .split(",")
                    )
                    >= 0.5
                ):
                    countCorrect += 1
                else:
                    countWrong += 1
                    print(summary)
                    print(trainingData[i]["spoiler"][0])
                    # break

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
    print(countCorrect / count)

    # print(count)
    # print(countMultiActual)
    # print("Number Counted as Multi:")
    # print(countMultiCounting)
    # print(countMultiCounting/countMultiActual)
    # print("Number Counted as Non Multi")
    # print(count)
    # print(countWrong/countNonMulti)
    # print((countMultiCounting/countMultiActual)/(countWrong/countNonMulti))
    # print("Count Non Multi:")
    # print(countNonMulti)
