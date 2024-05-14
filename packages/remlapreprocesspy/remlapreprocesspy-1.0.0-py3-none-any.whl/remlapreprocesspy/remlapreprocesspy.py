from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

## TODO: This functionality should NOT be part of the final repo, but in lib-ml instead.

## open config.yml

def preprocess(arr):
    #arr : array of strings to preprocess for classifier

    test = [v.strip() for v in arr]

    ### Preprocess data
    ## Tokenizing Dataset

    tokenizer = Tokenizer(lower=True, char_level=True, oov_token='-n-')
    tokenizer.fit_on_texts(test)
    char_index = tokenizer.word_index
    char_index_size = len(char_index)

    sequence_length = 200

    x_test = pad_sequences(tokenizer.texts_to_sequences(test), maxlen=sequence_length)
    print("Succesfully tokenized dataset")
    return x_test

def main():
    print(preprocess(["http://www.test.com","http://vibes.se"]))

if __name__ == '__main__':
    main()
