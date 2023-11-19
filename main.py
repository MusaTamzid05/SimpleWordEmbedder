from lib.tokenizer import Tokenizer
from lib.dataset import WordDataset
import torch

if __name__ == "__main__":
    tokenizer = Tokenizer(corpus_path="./dracula.txt", word_count=1000)
    word_dataset = WordDataset(tokenizer=tokenizer, context_size=5)

    for batch in word_dataset:
        print(batch)


