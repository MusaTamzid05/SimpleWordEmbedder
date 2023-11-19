from torch import nn
from torch.nn import functional as F
import torch

class GenerateModel(nn.Module):
    def __init__(self, vocab_size, embedding_dims, context_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dims)
        self.linear1 = nn.Linear(embedding_dims * context_size, 128)
        self.linear2 = nn.Linear(128, vocab_size)

    def forward(self, x):
        x = self.embedding(x).view((1, -1))
        x = self.linear1(x)
        x = F.relu(x)
        x = self.linear2(x)
        x = F.log_softmax(x, dim=1)

        return x

class GenerateModel2(nn.Module):
    def __init__(self, vocab_size, embedding_dims):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dims)
        self.lstm = nn.LSTM(input_size=embedding_dims, hidden_size=75, num_layers=1, batch_first=True)
        self.linear1 = nn.Linear(75, 128)
        self.linear2 = nn.Linear(128, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        x = torch.unsqueeze(x, 0)
        x, _  = self.lstm(x)
        x = self.linear1(x[:,-1])
        x = F.relu(x)
        x = self.linear2(x)
        x = F.log_softmax(x, dim=1)
        return x



if __name__ == "__main__":
    x = torch.LongTensor([1, 2, 3, 4, 5])
    #model = GenerateModel2(vocab_size=1000, embedding_dims=10, context_size=5)
    model = GenerateModel2(vocab_size=1000, embedding_dims=10)
    x = model(x)

    print(x.shape)

