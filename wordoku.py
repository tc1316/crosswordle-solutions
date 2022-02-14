import os

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
        self.word = ""

    def __repr__(self):
        return f"{self}"



class Trie:

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
        node.word = word

    def _dfs(self, node, prefix):
        if node.is_end:
            self.output.append((prefix + node.char))

        for child in node.children.values():
            print(f"Child: {child}, Current Node: {node}")
            self._dfs(child, prefix + node.char)

    def search(self, word, node=None):
        if node == None:
            node = self.root

        for char in word:
            if char in node.children:
                node = node.children[char]
                print(node.children)
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

def find_diagonal_word():
    # Select a word for our diagonal (call it diag)
    # For char in word: (from index 0 to 4)
    #   Find word where word[char] == diag[char]
    pass
 
def main():
    trie_zero = Trie()
    for word in words:
        trie_zero.insert(word)

    trie_one = Trie()
    for word in words:
        trie_one.insert(word[1:])

    # with open("trie_one.txt", "a") as f:
    #     f.write(trie_one.__repr__())


    diag = "bacon"
    print(trie_zero.search(diag))
 
    
if __name__ == "__main__":
    main()
