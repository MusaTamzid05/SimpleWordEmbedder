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

        self._save()

    def _save(self):
        if os.path.isdir(self.save_dir) == False:
            os.mkdir(self.save_dir)

        model_name = "model_" + str(len(os.listdir(self.save_dir)))
        model_path = os.path.join(self.save_dir, model_name)
        torch.save(self.model.state_dict(), model_path)
        print(f"Saved {model_path}")



