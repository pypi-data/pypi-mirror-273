import re
from enum import Enum

from nltk import word_tokenize
from nltk.corpus import wordnet, wordnet as wn
import nltk

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


class PartOfSpeech(Enum):
    Noun = 'n'
    Verb = 'v'
    Adjective = 'a|s'
    Conjunction = 'c'


class SpeechTags(Enum):
    Noun = 'NN'
    NounPlural = 'NNS'
    ProperNoun = 'NNP'
    ProperNounPlural = 'NNPS'
    Verb = 'VB'
    VerbThirdPerson = 'VBZ'
    Adjective = 'JJ'
    Adverb = 'RB'
    Preposition = 'IN'
    Determiner = 'DT'
    PersonalPronoun = 'PRP'
    Conjunction = 'CC'
    PossessiveEnding = 'POS'


def get_synonyms(word, part_of_speech=PartOfSpeech.Noun):
    """
    Args:
        word: The word for which you want to find synonyms.
        part_of_speech: The part of speech of the word. Default value is PartOfSpeech.Noun.

    Returns:
        A list of synonyms for the given word and part of speech.

    """
    synonyms = set()
    synsets = wordnet.synsets(word)
    pattern = re.compile(f'^({part_of_speech.value})$') if part_of_speech is not None else re.compile(f'')
    for synset in [syn for syn in synsets if part_of_speech is None or pattern.match(syn.pos())]:
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)


def get_last_part_of_speech(words=None, part_of_speech=PartOfSpeech.Noun):
    if words is None:
        return None
    for word in reversed(words):
        if is_part_of_speech(word, part_of_speech):
            return word
    return None


def get_last_noun_sequence(words=None):
    if words is None:
        return None
    tokens = word_tokenize(' '.join(words))
    tagged_words = nltk.pos_tag(tokens)
    noun_tags = [SpeechTags.Noun.value, SpeechTags.NounPlural.value, SpeechTags.ProperNoun.value,
                 SpeechTags.ProperNounPlural.value]
    noun_list = []
    for word, tag in reversed(tagged_words):
        if len(noun_list) == 0 and tag in noun_tags:
            noun_list.append(word)
        elif len(noun_list) > 0 and tag not in noun_tags:
            return list(reversed(noun_list))
        elif len(noun_list) > 0 and tag in noun_tags:
            noun_list.append(word)
    return list(reversed(noun_list))


def split_cased_phrase(phrase):
    """
    Splits a camel-cased, snake-cased, or kebab-cased phrase into individual words.

    Args:
        phrase (str): The input phrase.

    Returns:
        list: A list of individual words.
    """
    # Split by underscores (snake case) or hyphens (kebab case)
    words = re.split(r'[_-]', phrase)

    # If the phrase is camel case, further split by capital letters
    if len(words) == 1:
        # Use a regex to find capital letters and split accordingly
        matches = re.finditer(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', phrase)
        split_string = []
        previous = 0
        for match in matches:
            split_string.append(phrase[previous:match.start()])
            previous = match.start()
        split_string.append(phrase[previous:])  # Add the last word
        words = split_string

    return words


def is_part_of_speech(word, part_of_speech=PartOfSpeech.Noun):
    pattern = re.compile(f'^({part_of_speech.value})$')
    for synset in wn.synsets(word):
        if pattern.match(synset.pos()):
            return True
    return False
