WILDCARD = '?'

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
                if current_node.is_leaf:
                    result.append(current_node_word)
                continue

            current_node_char = word[count]
            if current_node_char == WILDCARD:
                for child_char, node in current_node.children.items():
                    stack.append(
                        (node, count + 1, current_node_word + child_char))
                continue

            if current_node_char in current_node.children:
                node = current_node.children[current_node_char]
                stack.append(
                    (node, count + 1, current_node_word + current_node_char))

        return result

    def __repr__(self):
        def recur(node, indent):
            return "".join(indent + key + ("$" if child.is_leaf else "")
                                  + recur(child, indent + "  ")
                           for key, child in node.children.items())

        return recur(self, "\n")