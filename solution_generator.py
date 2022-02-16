import os
import random
from trie import WILDCARD, Trie

WILDCARD = "?"
WORD_DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "wordle_data",
)
SHORT_WORD_LIST_FILE = os.path.join(WORD_DATA_DIR, "possible_words.txt")


def get_word_list():
    result = []
    file = SHORT_WORD_LIST_FILE
    with open(file) as fp:
        result.extend([word.strip() for word in fp.readlines()])
    return result


def generate_diagonal_solution(word_list, trie):
    diag = [char for char in random.choice(word_list)]
    wildcards = [q for q in WILDCARD*5]
    output = []

    for idx, _ in enumerate(diag):
        wildcards[idx] = diag[idx]
        output.append(random.choice(trie.find(wildcards)))
        wildcards[idx] = WILDCARD

    return "".join(output)


def generate_three_by_three_solution(word_list, trie):
    rows, cols = [], []
    top_row = random.choice(word_list)
    wildcards = [q for q in WILDCARD*5]
    rows.append(top_row)

    for idx in range(0, 5, 2):
        wildcards[0] = top_row[idx]
        if not trie.find(wildcards):
            return generate_three_by_three_solution(word_list, trie)
        else:
            cols.append(random.choice(trie.find(wildcards)))

    # Searching for valid word to put in the middle row
    wildcards[0] = WILDCARD
    wildcards[0] = cols[0][2]
    wildcards[2] = cols[1][2]
    wildcards[4] = cols[2][2]

    if not trie.find(wildcards):
        return generate_three_by_three_solution(word_list, trie)
    rows.append(random.choice(trie.find(wildcards)))

    # Searching for valid word to put in the last row
    wildcards[0] = cols[0][4]
    wildcards[2] = cols[1][4]
    wildcards[4] = cols[2][4]

    if not trie.find(wildcards):
        return generate_three_by_three_solution(word_list, trie)
    rows.append(random.choice(trie.find(wildcards)))

    output = [rows[0], cols[0][1], "*", cols[1][1], "*", cols[2][1],
              rows[1], cols[0][3], "*", cols[1][3], "*", cols[2][3], rows[2]]
    return "".join(output)


def main():
    trie = Trie()
    word_list = get_word_list()
    for word in word_list:
        trie.insert(word)

    with open("./outputs/diagonal.txt", "w") as f:
        final_output = []
        for _ in range(100):
            final_output.append(generate_diagonal_solution(word_list, trie))
        print(final_output, file=f)

    with open("./outputs/three_by_three.txt", "w") as f:
        final_output = []
        for _ in range(100):
            final_output.append(
                generate_three_by_three_solution(word_list, trie))
        print(final_output, file=f)


if __name__ == "__main__":
    main()
