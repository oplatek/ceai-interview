#!/bin/bash

# mkdir -p jm_corpus
# wget http://j2m.cz/~jm/corpus_ebooks -O jm_corpus/corpus_ebooks.raw

# ./extract_training_data.py ./jm_corpus/corpus_ebooks.raw \
#     ./jm_corpus/jm.input \
#     ./jm_corpus/jm.gold

# todo shuffle
lines=$(wc ./jm_corpus/jm.input | cut -d ' ' -f 4)
train_end=$(python3 -c "print(int($lines * 0.7))")
dev_end=$(python3 -c "print(int($lines * 0.8))")
dev_count=$(python3 -c "print($dev_end - $train_end)")
test_end=$lines
test_count=$(python3 -c "print($test_end - $dev_end)")
cat ./jm_corpus/jm.input | head -n $train_end > ./jm_corpus/train.input
cat ./jm_corpus/jm.gold | head -n $train_end > ./jm_corpus/train.gold

cat ./jm_corpus/jm.input | head -n $dev_end | tail -n $dev_count > ./jm_corpus/dev.input
cat ./jm_corpus/jm.gold | head -n $dev_end | tail -n $dev_count > ./jm_corpus/dev.gold

cat ./jm_corpus/jm.input | head -n $test_end | tail -n $test_count > ./jm_corpus/test.input
cat ./jm_corpus/jm.gold | head -n $test_end | tail -n $test_count > ./jm_corpus/test.gold
