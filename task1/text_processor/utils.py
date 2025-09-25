"""Text processor utils."""
# Standard Library
import random


def reverse_word(word):
    """Shuffle inner characters of a word, keeping first and last fixed."""
    if len(word) <= 3:
        return word
    middle_part = word[1:-1][::-1]

    return word[0] + ''.join(random.sample(middle_part, len(middle_part))) + word[-1]
