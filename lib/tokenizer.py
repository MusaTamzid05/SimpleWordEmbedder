import random

class Tokenizer:
    def __init__(self, corpus_path, word_count):
        text = None
        with open(corpus_path, "r") as f:
            text = f.read()

        self.words = text.split()[:word_count]

        self.word_to_id = {}
        self.id_to_word = {}

        for word in self.words:
            word = self._clear(word=word)
            word = word.strip()
            if word not in self.word_to_id:
                self.word_to_id[word] = -1
            else:
                if self.word_to_id[word] != -1:
                    continue

            word_id = len(self.word_to_id) - 1
            self.word_to_id[word] = word_id
            self.id_to_word[word_id] = word




    def _clear(self, word):
        word = word.lower().strip()
        new_word = ""

        ignore_chars = ["[", "]", "#", "="]

        for ch in word:
            if ch in ignore_chars:
                continue
            new_word += ch

        return new_word

    def encode(self, word_list):
        ids = []

        for word in word_list:
            if word in self.word_to_id:
                ids.append(self.word_to_id[word])
            else:
                index = random.randrange(0, len(self.word_to_id))
                ids.append(index)

        return ids




    def decode(self, id_list):
        return [self.id_to_word[_id] for _id in id_list]









