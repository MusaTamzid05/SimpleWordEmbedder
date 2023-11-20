from lib.tokenizer import Tokenizer
from lib.dataset import WordDataset
from lib.word_genarator import WordGenerator

if __name__ == "__main__":
    generator = WordGenerator()
    generator.init_train(
            corpus_path="./dracula.txt",
            word_count=1000
            )

    generator.train(epochs=500)
    print(generator.generate(text="How these papers have been", output_word_count=100))



