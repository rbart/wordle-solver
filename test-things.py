


import sys
from collections import defaultdict
import json

letter_pos_counts = defaultdict(lambda: defaultdict(lambda: 0))
pos_letter_counts = defaultdict(lambda: defaultdict(lambda: 0))

total_words = 0

words = []

# Remember to include all grays
# Use force_uniq sparingly.
greens = greens = ""
yellows = [""]
grays = ""
force_uniq = False




greens = [(c, i) for (i,c) in enumerate(greens) if c != '?']
yellows = [
    [(c, i) for (i,c) in enumerate(yellow) if c != '?']
    for yellow in yellows
]
yellows = [
    rule for rules in yellows for rule in rules
]
grays = [c for c in grays]

def filter_word(w):
    return (
        all(w[i] == c for (c,i) in greens) and
        all(c in w and w[i] != c for (c,i) in yellows) and
        all(c not in w for c in grays)
    )

for line in sys.stdin:
    line = line.strip()
    total_words += 1
    if filter_word(line):
        words.append(line)

for word in words:
    for (i, c) in enumerate(word):
        letter_pos_counts[c][i] += 1
        pos_letter_counts[i][c] += 1

total_letters = total_words * 5
conditional_probs = defaultdict(lambda: defaultdict(lambda: float(0)))
for letter, pos_counts in letter_pos_counts.items():
    for pos, count in pos_counts.items():
        joint_prob = float(count) / total_letters
        cond_prob = joint_prob / 5
        conditional_probs[letter][pos] = cond_prob

def word_prob(word):
    prob = 1.0
    for (i, c) in enumerate(word):
        prob *= conditional_probs[c][i]
    return prob

def all_uniq_letters(word):
    letters = {}
    for c in word:
        if c in letters:
            return False
        else:
            letters[c] = True
    return True

ranked_words = [
    (word, word_prob(word))
    for word in words
    if (not force_uniq or all_uniq_letters(word)) and filter_word(word)
]
ranked_words.sort(key=lambda x: x[1])
ranked_words = ranked_words[-25:]

for word, prob in ranked_words:
    print(word + "\t" + str(prob))
