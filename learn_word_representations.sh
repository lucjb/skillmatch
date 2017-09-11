time word2vec -train ./corpus.txt -output word_embeddings.csv -cbow 1 -size 400 -window 5 -negative 0 -hs 1 -sample 1e-5 -threads 4 -min-count 50

