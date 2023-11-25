from lib.tokenizer import Tokenizer
from lib.dataset import WordDataset
from lib.models import GenerateModel
from lib.context import context


import torch
from torch import nn
from torch import optim 
import os
import pickle



class WordGenerator:
    def __init__(self):
        self.device = ("cuda" if torch.cuda.is_available() else "cpu")
        self.save_dir = "./models"



    def init_train(self, corpus_path, word_count):
        self.context_size = 5  
        self.embedding_dims = 10
        self.corpus_path = corpus_path
        self.word_count = word_count

        self.tokenizer = Tokenizer()
        self.tokenizer.init_train(corpus_path=corpus_path,word_count=word_count)
        self.word_dataset = WordDataset(tokenizer=self.tokenizer,context_size=self.context_size)

        self.model = GenerateModel(
                vocab_size=len(self.tokenizer.words),
                embedding_dims= self.embedding_dims,
                context_size=self.context_size
                ).to(self.device)



    def init_generator(self, model_dir_path, model_name):
        self.tokenizer = Tokenizer()
        self.tokenizer.load(path=model_dir_path, model_name=model_name)

        model_info_path = os.path.join(model_dir_path, model_name + ".pickle")
        model_info = {}

        with open(model_info_path, 'rb') as f:
            model_info = pickle.load(f)

        self.embedding_dims = model_info["embedding_dims"]
        self.context_size = model_info["context_size"]

        self.model = GenerateModel(
                vocab_size=len(self.tokenizer.words),
                embedding_dims= self.embedding_dims,
                context_size=self.context_size
                ).to(self.device)


        model_path = os.path.join(model_dir_path, model_name + ".model")
        self.model.load_state_dict(torch.load(model_path))


    def train(self, epochs, model_name=None):
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

                if model_name != None:
                    context.add(
                            model_name=model_name,
                            epochs=current_epoch,
                            loss=loss
                            )

        except KeyboardInterrupt:
            print(f"\nClosing training at {current_epoch}")

        finally:
            self._save(epoch_count=current_epoch, model_name=model_name)

    def _save(self, epoch_count, model_name=None):
        if os.path.isdir(self.save_dir) == False:
            os.mkdir(self.save_dir)

        if model_name is None:
            model_name = "model_" + str(epoch_count) + "_" +  str(len(os.listdir(self.save_dir)))

        model_path = os.path.join(self.save_dir, model_name + ".model")
        torch.save(self.model.state_dict(), model_path)

        self.tokenizer.save(path=self.save_dir,model_name=model_name)

        model_info_path = os.path.join(self.save_dir, model_name + ".pickle")

        with open(model_info_path, "wb") as f:
            pickle.dump({
                "embedding_dims" : self.embedding_dims,
                "vocab_count" : len(self.tokenizer.words),
                "context_size" : self.context_size


                }, f)




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
            word_ids =  self.tokenizer.encode(word_list=input_words)
            word_ids = torch.LongTensor(word_ids).to(self.device)
            prediction = int(self.model(word_ids).argmax(1))
            predicted_word = self.tokenizer.id_to_word[prediction]
            results.append(predicted_word)

            start_index += 1
            end_index += 1

        return " ".join(results)
 




