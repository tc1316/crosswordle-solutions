import os
from re import sub

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


words = get_word_list()


class TrieNode:

    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.children = {}


class Trie(object):

    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word):
        node = self.root

        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.is_end = True

    def _dfs(self, node, prefix):
        if node.is_end:
            self.output.append((prefix + node.char))

        for child in node.children.values():
            self._dfs(child, prefix + node.char)

    def search(self, word):
        node = self.root

        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return []

        self.output = []
        self._dfs(node, word[:-1])

        return self.output

    def __repr__(self):
        def recur(node, indent):
            return "".join(indent + key + ("$" if child.is_end else "")
                                  + recur(child, indent + "  ")
                           for key, child in node.children.items())

        return recur(self.root, "\n")

def find_valid_words(prev_words: list, trie: Trie, words_to_exclude: list, words_to_consider: list):

    for word in filter(lambda word: word not in words_to_exclude, words):
        # Iterate through each character position from a column perspective and check if the substrings are valid
        # print("----" + word.upper())
        tmp = ""
        for i, char in enumerate(word):
            current_substring = "".join([w[i] for w in prev_words]) + char
            if len(trie.search(current_substring)) == 0:
                break
            tmp += current_substring[-1]
            if len(tmp) == 5:
                words_to_consider.append(tmp) 
                # Maybe use another tree e.g. {"aback": {"bacon": {third_word...}, "baler": {third_word...}, ...}}
    return words_to_consider

def main():
    trie = Trie()
    for word in words:
        trie.insert(word)

    # Take example word: "aback"

    # |a|b|a|c|k|
    # |b|a|c|o|n|
    # | | | | | |
    # | | | | | |
    # | | | | | |

    first_word = ["aback"]
    excludables = [first_word]
    possible_words = []

    second_words = find_valid_words(first_word, trie, excludables, possible_words)
    print(second_words)
    # for word in second_words:
    #     excludables.append(word)
    #     first_and_second_word = first_word
    #     first_and_second_word.append(word)
    #     print(first_and_second_word)
    #     # print(find_valid_words(first_and_second_word,trie,excludables, possible_words))
    #     first_and_second_word.pop()
    #     print(first_and_second_word)
    

    # with open("trie.txt", "a") as f:
    #     f.write(tr.__repr__())


if __name__ == "__main__":
    main()
