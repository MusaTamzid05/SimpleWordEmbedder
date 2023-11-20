from lib.tokenizer import Tokenizer
from lib.dataset import WordDataset
from lib.models import GenerateModel
import torch
from torch import nn
from torch import optim 
import os


class WordGenerator:
    def __init__(self):
        self.corpus_path = None
        self.word_count= None
        self.context_size = 5  
        self.tokenizer = None
        self.word_dataset = None
        self.model = None

        self.device = ("cuda" if torch.cuda.is_available() else "cpu")
        self.save_dir = "./models"



    def init_train(self, corpus_path, word_count):
        self.corpus_path = corpus_path
        self.word_count = word_count
        self.tokenizer = Tokenizer(corpus_path=corpus_path,word_count=word_count)
        self.word_dataset = WordDataset(tokenizer=self.tokenizer,context_size=self.context_size)

        self.model = GenerateModel(
                vocab_size=len(self.tokenizer.words),
                embedding_dims= 10,
                context_size=5
                ).to(self.device)


    def train(self, epochs):
        loss_func = nn.NLLLoss()
        optimizer = optim.SGD(self.model.parameters(), lr=0.001)
        self.model.train()

        current_epoch = None

        try:

            for epoch in range(epochs):
                print(f"Epoch {epoch}", end="\t")
                epoch_losses = []

                for batch in self.word_dataset:
                    self.model.zero_grad()
                    x, y = batch
                    x = x.to(self.device)
                    y = y.to(self.device)

                    logits = self.model(x)

                    loss = loss_func(logits, y)
                    loss.backward()
                    optimizer.step()

                    epoch_losses.append(loss.item())

                loss = sum(epoch_losses) / len(epoch_losses)
                print(f"Loss {loss}")
                current_epoch = epoch

        except KeyboardInterrupt:
            print(f"\nClosing training at {current_epoch}")

        finally:
            self._save(epoch_count=current_epoch)

    def _save(self, epoch_count):
        if os.path.isdir(self.save_dir) == False:
            os.mkdir(self.save_dir)

        model_name = "model_" + str(epoch_count) + "_" +  str(len(os.listdir(self.save_dir)))
        model_path = os.path.join(self.save_dir, model_name)
        torch.save(self.model.state_dict(), model_path)
        print(f"Saved {model_path}")


    def generate(self, text, output_word_count):
        words = text.split()
        words = [word.lower() for word in words]

        if len(words) != self.context_size:
            print("Input size needs to be of {self.context_size} length")
            return

        start_index = 0
        end_index = self.context_size

        self.model.eval()

        results = words

        while len(results) < output_word_count:
            input_words = results[start_index:end_index]
            word_ids = [self.tokenizer.word_to_id[word] for word in input_words]
            word_ids = torch.LongTensor(word_ids).to(self.device)
            prediction = int(self.model(word_ids).argmax(1))
            predicted_word = self.tokenizer.id_to_word[prediction]
            results.append(predicted_word)

            start_index += 1
            end_index += 1

        return " ".join(results)
 




