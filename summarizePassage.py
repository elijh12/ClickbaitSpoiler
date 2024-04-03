import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

# text = """
#     Maria Sharapova has basically no friends as tennis players on the WTA Tour. The Russian player has no problems in openly speaking about it and in a recent interview she said: 'I don't really hide any feelings too much.
#     I think everyone knows this is my job here. When I'm on the courts or when I'm on the court playing, I'm a competitor and I want to beat every single person whether they're in the locker room or across the net.
#     So I'm not the one to strike up a conversation about the weather and know that in the next few minutes I have to go and try to win a tennis match.
#     I'm a pretty competitive girl. I say my hellos, but I'm not sending any players flowers as well. Uhm, I'm not really friendly or close to many players.
#     I have not a lot of friends away from the courts.' When she said she is not really close to a lot of players, is that something strategic that she is doing? Is it different on the men's tour than the women's tour? 'No, not at all.
#     I think just because you're in the same sport doesn't mean that you have to be friends with everyone just because you're categorized, you're a tennis player, so you're going to get along with tennis players.
#     I think every person has different interests. I have friends that have completely different jobs and interests, and I've met them in very different parts of my life.
#     I think everyone just thinks because we're tennis players we should be the greatest of friends. But ultimately tennis is just a very small part of what we do.
#     There are so many other things that we're interested in, that we do.'
# """

targetParagraphs = [
    "The hole in the space station is superficial but a little unsettling for Earthbound folk.",
    "When you sit around imagining life aboard the International Space Station (we all do that, right?) one thing you probably don't want to think about is space junk slamming into your vessel. And you almost certainly don't want to imagine a piece of that junk taking a chunk of your spacecraft's window with it.",
    "Especially not when the chipped window in question is the one that provides some of the best views of Earth.",
    "[NASA reminds us that astronaut poop burns up 'like shooting stars']",
    "But that's exactly what happened last month in the space station's Cupola, a European-built 2010 addition that you're sure to recognize - it's where those great pictures and videos showing stunning shots of our planet are taken.",
    '"I am often asked if the International Space Station is hit by space debris," British astronaut Tim Peake, who took the freaky photo of the damaged window, said in a statement. "Yes - this is the chip in one of our Cupola windows, glad it is quadruple glazed!"',
    "Um, yeah. You can say that again.",
    "NASA released an animation depicting space trash in motion around Earth. (YouTube/NASA)",
    "The astronauts, of course, are perfectly safe - they generally don't tweet photos during life-threatening station crises. And the views are safe, too - the chip is less than a centimeter across. According to the European Space Agency, the damage was likely caused by something as unassuming as a flake of paint or a metal fragment just a few thousandths of a millimeter across.",
    "A FLAKE OF PAINT. Let that sink in.",
    "Because of the incredibly high speeds of these orbiting pieces of debris, something 1 centimeter across could disable critical instruments on the space station, and anything larger could penetrate the sturdy shields that protect crew modules. Debris 10 centimeters across could shatter the spacecraft into pieces. In 2013, experts estimated that there were at least 29,000 objects of this size orbiting Earth.",
    'The danger posed by errant space debris were dramatized in the 2013 film "Gravity," in which astronauts on a shuttle mission are terrorized by speeding chunks of space junk.',
    "Space junk is definitely a real concern. Mashable reports that NASA tracks more than 500,000 pieces of defunct satellites and old rocket bits orbiting Earth, some no larger than marbles, so that the space station can be maneuvered away from close encounters - but many small pieces, like the one that hit the space station, are too difficult to keep track of.",
    "These days space agencies try to be more mindful of the waste left behind by missions, but no one has found an ideal solution for cleaning up the junk that's already there.",
]

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

punctuation = punctuation + "\n"
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

# select_length = int(len(sentence_tokens) * 0.3)
select_length = 2
# print(select_length)

summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
# print(summary)

final_summary = [word.text for word in summary]
summary = " ".join(final_summary)
# print(text)

print(summary)
print(type(summary))
