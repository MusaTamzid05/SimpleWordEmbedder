from lib.tokenizer import Tokenizer
import torch

if __name__ == "__main__":
    tokenizer = Tokenizer(corpus_path="./dracula.txt", word_count=1000)
    words = "If you are not located in the United States".split()
    words = [word.lower() for word in words]
    ids = tokenizer.encode(word_list=words)
    print(ids)
    decoded_words =  tokenizer.decode(id_list=ids)
    print(decoded_words)

