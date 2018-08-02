#!/bin/bash

# mkdir -p jm_corpus
# wget http://j2m.cz/~jm/corpus_ebooks -O jm_corpus/corpus_ebooks.raw

./extract_training_data.py ./jm_corpus/corpus_ebooks.raw \
    ./jm_corpus/jm.input \
    ./jm_corpus/jm.gold
