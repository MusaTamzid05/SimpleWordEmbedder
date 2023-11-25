import random
import os
import pickle

class Tokenizer:
    def __init__(self):
        pass

    def init_train(self, corpus_path, word_count):
        text = None
        with open(corpus_path, "r") as f:
            text = f.read()

        self.words = text.split()[:word_count]

        self.word_to_id = {}
        self.id_to_word = {}

        processed_words = []

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
            processed_words.append(word)

        self.words = processed_words





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

    def get_words(self, start_index, end_index):
        return self.words[start_index:end_index]

    def get_word(self, index):
        return self.words[index]

    def save(self, path, model_name):
        info = {
                "words" : self.words,
                "word_to_id" : self.word_to_id,
                "id_to_word" : self.id_to_word
                }

        model_path = os.path.join(path, model_name + "_tokenizer.pickle")

        with open(model_path, "wb") as f:
            pickle.dump(info, f)


    def load(self, path, model_name):

        model_path = os.path.join(path, model_name + "_tokenizer.pickle")

        with open(model_path, "rb") as f:
            info = pickle.load(f)
            self.words = info["words"]
            self.word_to_id = info["word_to_id"]
            self.id_to_word = info["id_to_word"]




















