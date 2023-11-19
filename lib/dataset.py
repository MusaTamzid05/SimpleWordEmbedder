from torch.utils.data import Dataset
import torch


class WordDataset(Dataset):
    def __init__(self, tokenizer, context_size):
        self.tokenizer = tokenizer
        self.context_size = context_size

    def __len__(self):
        return len(self.tokenizer.word_to_id)

    def __getitem__(self, index):
        start_index = index
        end_index = start_index + self.context_size

        words = self.tokenizer.get_words(start_index=start_index, end_index=end_index)
        target_word = self.tokenizer.get_word(index=end_index)


        x = self.tokenizer.encode(word_list=words)
        y = self.tokenizer.encode(word_list=[target_word])

        x = torch.LongTensor(x)
        y = torch.LongTensor(y)

        return x, y



