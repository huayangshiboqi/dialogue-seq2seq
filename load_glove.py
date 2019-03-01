import numpy as np
import pickle
import argparse
from tqdm import tqdm

from transformer import Constants

def create_glove_emb_table(word2idx, split_name, glove_path='data/glove/glove.6B.300d.txt', glove_size=300):
    ''' Creates GloVe embedding table and changes word2idx '''

    word2idx.pop(Constants.PAD_WORD, None)
    word2idx.pop(Constants.UNK_WORD, None)
    word2idx.pop(Constants.BOS_WORD, None)
    word2idx.pop(Constants.EOS_WORD, None)
    word2emb = {}

    print("[Info] Load GloVe model.")
    with open(glove_path,'r', encoding="utf-8") as f:
        for line in tqdm(f):
            split_line = line.split()
            word = split_line[0]
            if word in word2idx.keys():
                embedding = np.array([float(val) for val in split_line[1:]])
                word2emb[word] = embedding

    #- Create embedding table
    word2idx = {}
    emb_table = np.zeros(shape=(len(word2emb) + 4, glove_size))
    emb_table[Constants.PAD] = np.zeros(shape=(glove_size))
    emb_table[Constants.UNK] = np.zeros(shape=(glove_size))
    emb_table[Constants.BOS] = np.zeros(shape=(glove_size))
    emb_table[Constants.EOS] = np.zeros(shape=(glove_size))
    for idx, (word, emb) in enumerate(word2emb.items(), 4):
        emb_table[idx] = emb
        word2idx[word] = idx

    print('[Info] Final {} vocabulary size: {}'.format(split_name, len(word2idx)))

    np.save('data/glove/{}_emb_file.npy'.format(split_name), emb_table)

    return word2idx