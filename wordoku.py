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


def main():
    tr = Trie()
    for word in words:
        tr.insert(word)
    
    # Take example word: "aback"

    # |a|b|a|c|k|
    # |a|b|a|s|e|
    # | | | | | |
    # | | | | | |
    # | | | | | |

    first = "aback"
    
    first_index = words.index(first) 
    solution_array = [first]
    # print(tr.search(first))

    for i in range(first_index+1, len(words)):
      # Iterate through each word in words alphabetically
      current_word = words[i]
      # Iterate through each character position from a column perspective and check if the substrings are valid
      for index, _ in enumerate(current_word):
        substring = first[index] + current_word[index]
        if len(tr.search(substring)) == 0:
          break
        
      
        


    # with open("trie.txt", "a") as f:
    #     f.write(tr.__repr__())


if __name__ == "__main__":
    main()
