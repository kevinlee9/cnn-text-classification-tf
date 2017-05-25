# -*- coding: utf-8 -*-

import numpy as np
from gensim.models.keyedvectors import KeyedVectors

embedding_matrix = np.load("embedding")
model = KeyedVectors.load_word2vec_format("/DB/rhome/zkli/data/weibo.withstop.vector.copy")

model.syn0 = embedding_matrix

model.save_word2vec_format("new.vector")
