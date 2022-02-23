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
    diag_word = "".join(diag)
    wildcards = [q for q in WILDCARD*5]
    output = []

    idx = 0
    while idx < len(diag):
        wildcards[idx] = diag[idx]
        candidate_word = random.choice(trie.find(wildcards))
        if candidate_word not in output and candidate_word != diag_word:
            output.append(candidate_word)
            wildcards[idx] = WILDCARD
            idx += 1

    return "".join(output)


def generate_three_by_three_solution(word_list, trie):

    def filter_duplicates(rows, cols, word_list):
        filtered_list = list(filter(lambda word: word not in rows and word not in cols, word_list))
        return filtered_list

    rows, cols = [], []
    top_row = random.choice(word_list)
    wildcards = [q for q in WILDCARD*5]
    rows.append(top_row)
   
    for idx in range(0, 5, 2):
        wildcards[0] = top_row[idx]
        candidate_words_list = trie.find(wildcards)
        if not candidate_words_list or not filter_duplicates(rows,cols,candidate_words_list):
            return generate_three_by_three_solution(word_list, trie)
        else:
            cols.append(random.choice(filter_duplicates(rows,cols,candidate_words_list)))

    # Searching for valid word to put in the middle row
    wildcards[0] = WILDCARD
    wildcards[0] = cols[0][2]
    wildcards[2] = cols[1][2]
    wildcards[4] = cols[2][2]

    candidate_words_list = trie.find(wildcards)
    if not candidate_words_list or not filter_duplicates(rows,cols,candidate_words_list):
        return generate_three_by_three_solution(word_list, trie)
    else:
        print(candidate_words_list)
        rows.append(random.choice(filter_duplicates(rows,cols,candidate_words_list)))
   
    # Searching for valid word to put in the last row
    wildcards[0] = cols[0][4]
    wildcards[2] = cols[1][4]
    wildcards[4] = cols[2][4]

    candidate_words_list = trie.find(wildcards)
    if not candidate_words_list or not filter_duplicates(rows,cols,candidate_words_list):
        return generate_three_by_three_solution(word_list, trie)
    else:
        print(candidate_words_list)
        rows.append(random.choice(filter_duplicates(rows,cols,candidate_words_list)))

    output = [rows[0], cols[0][1], "*", cols[1][1], "*", cols[2][1],
              rows[1], cols[0][3], "*", cols[1][3], "*", cols[2][3], rows[2]]
    
    return "".join(output)


def main():
    trie = Trie()
    word_list = get_word_list()
    for word in word_list:
        trie.insert(word)

    with open("./outputs/diagonal.txt", "w") as f:
        f.write("[")
        for _ in range(365):
            output = generate_diagonal_solution(word_list, trie)
            print(f"'{output}',", file=f)
        f.write("]")

    with open("./outputs/three_by_three.txt", "w") as f:
        f.write("[")
        for _ in range(365):
            output = generate_three_by_three_solution(word_list, trie)
            print(f"'{output}',", file=f)
        f.write("]")
 
    with open("./outputs/another_three_by_three.txt", "w") as f:
        f.write("[")
        for _ in range(365):
            output = generate_three_by_three_solution(word_list, trie)
            print(f"'{output}',", file=f)
        f.write("]")

if __name__ == "__main__":
    main()
