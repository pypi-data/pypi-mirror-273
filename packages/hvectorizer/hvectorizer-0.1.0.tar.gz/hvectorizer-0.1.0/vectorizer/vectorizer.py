class Vectorizer:
    def __init__(self, punctuation=" !#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"):
        self.punctuation = punctuation

    def standardize(self, text):
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        text = text.lower()
        return "".join([char for char in text if char not in self.punctuation])

    def tokenize(self, text):
        text = self.standardize(text)
        return text.split()

    def make_vocabulary(self, dataset):
        if not isinstance(dataset, list) or not all(
            isinstance(item, str) for item in dataset
        ):
            raise ValueError("Dataset must be a list of strings")

        self.vocabulary = {"": 0, "[UNK]": 1}
        for text in dataset:
            text = self.standardize(text)
            tokens = self.tokenize(text)
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)

        self.inverse_vocabulary = {
            index: word for word, index in self.vocabulary.items()
        }

    def encode(self, text):
        text = self.standardize(text)
        tokens = self.tokenize(text)
        return [self.vocabulary.get(token, 1) for token in tokens]

    def decode(self, input_sequence):
        return "".join(
            self.inverse_vocabulary.get(index, "[UNK]") for index in input_sequence
        )
