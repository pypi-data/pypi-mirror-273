from pluralizer import Pluralizer

pluralizer = Pluralizer()


def combine_words(word_lists, idx: int = 0):
    new_words = []
    if len(word_lists) == idx + 1:
        return list(set(
            [pluralizer.singular(word) for word in list(word_lists[idx])] +
            [pluralizer.plural(word) for word in word_lists[idx]]
        ))
    for other_word in combine_words(word_lists, idx + 1):
        for word in word_lists[idx]:
            new_words.append(pluralizer.plural(word) + ' ' + other_word)
            new_words.append(pluralizer.singular(word) + ' ' + other_word)
    return list(set(new_words))



