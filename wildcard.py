import os
import random
from typing import final

WILDCARD = '?'
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

class Trie:
    def __init__(self) -> None:
        self.children: dict[str: Trie] = {}
        self.is_leaf: bool = False
    
    def insert(self, word: str) -> None:
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = Trie()
            node = node.children[char]
        node.is_leaf = True
    
    def find(self, word: str) -> list[str]:
        stack = [(self, 0, '')]
        result = []
        
        while stack:
            current_node, count, current_node_word = stack.pop()
            
            if count == len(word):
                if current_node.is_leaf: result.append(current_node_word)
                continue
            
            current_node_char = word[count]
            if current_node_char == WILDCARD:
                for child_char, node in current_node.children.items():
                    stack.append((node, count + 1, current_node_word + child_char))
                continue
        
            if current_node_char in current_node.children:
                node = current_node.children[current_node_char]
                stack.append((node, count + 1, current_node_word + current_node_char))

        return result

    def __repr__(self):
        def recur(node, indent):
            return "".join(indent + key + ("$" if child.is_leaf else "")
                                  + recur(child, indent + "  ")
                           for key, child in node.children.items())

        return recur(self, "\n")

def main():
  trie = Trie()
  words = get_word_list()
  for word in words:
        trie.insert(word)

  d = random.choice(words)
  w = "?????"
  diag = [char for char in d]
  wildcards = [q for q in w]
  output = []

  for idx, char in enumerate(diag):
    wildcards[idx] = diag[idx]
    output.append(random.choice(trie.find(wildcards)))
    wildcards[idx] = "?"

  print(diag)
  final_output = [char.upper() for char in "".join(output)]
  print(final_output)


if __name__ == "__main__":
  main()