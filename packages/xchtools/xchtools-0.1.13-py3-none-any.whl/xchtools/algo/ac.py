# %%


class ACNode:
    def __init__(self, char=None, parent=None):
        self.char = char
        self.parent = parent
        self.children = {}
        self.fail = None
        self.word = None


class ACAutomaton:
    def __init__(self):
        self.root = ACNode()

    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = ACNode(char, node)
            node = node.children[char]
        node.word = word

    def build(self):
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            for char, child in node.children.items():
                if node == self.root:
                    child.fail = self.root
                else:
                    p = node.fail
                    while p:
                        if char in p.children:
                            child.fail = p.children[char]
                            break
                        p = p.fail
                    if not p:
                        child.fail = self.root
                queue.append(child)

    def search(self, text):
        node = self.root
        found_words = []
        for char in text:
            while char not in node.children and node != self.root:
                node = node.fail
            if char in node.children:
                node = node.children[char]
            else:
                node = self.root
            temp = node
            while temp != self.root:
                if temp.word:
                    found_words.append(temp.word)
                temp = temp.fail
        return found_words


if __name__ == "__main__":
    # Usage
    ac_automaton = ACAutomaton()
    # words = ["he", "she", "his", "hers"]
    # text = "ushers"
    words = ["张坤", "易方达", "张凯", "阿里"]
    text = "易方达基金近日发布了一个智能助手，由阿里云智能提供。"
    for word in words:
        ac_automaton.add_word(word)
    ac_automaton.build()
    print(ac_automaton.search(text))  # 输出：['she', 'hers']

# %%
