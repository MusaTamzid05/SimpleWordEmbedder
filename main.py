from lib.models import GenerateModel
import torch

if __name__ == "__main__":
    x = torch.LongTensor([1, 2, 3, 4, 5])
    model = GenerateModel(vocab_size=1000, embedding_dims=10, context_size=5)
    x = model(x)

    print(x.shape)

