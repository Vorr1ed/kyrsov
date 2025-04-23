class WordEntry:
    def __init__(self, word, clue):
        self.word = word.upper()
        self.clue = clue

class CrosswordModel:
    def __init__(self):
        self.word_list = []
        self.grid = []
        self.size = 10

    def add_word(self, word, clue):
        if word and clue:
            self.word_list.append(WordEntry(word, clue))
