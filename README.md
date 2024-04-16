# geordrak2
This repo is about viewing the performance of the Element retrieval in a blockchain. 
Two methods are compared here, the brute force method in which every item in every block is checked and the bloom filter method in which only the blocks with positive bloom filter resposes are checked.
The performance is compared in blockchains that have [1, 10, 100, 1000, 10000, 100000] blocks and [1, 10, 100, 1000, 10000, 100000] elements in each block.
Every combination of the parameters is checked except the one with 100000 blocks and 100000 elements, that is 29 combinations.
In order to reduce the excecution time, a static database is created and stored in computer memory permanently. 
Due to limited computer memory the blockchain with 100000 blocks and 100000 elements is not stored, as it requires more than 20Gb.

The results of this performance test are ploted in a heatmap. In the position where the missing combination is, 0 is placed. 
The results are calculated in seconds.

This repo has 2 files, the bf_function.py file contains the classes and finctions that are used in the bloom_filter_LD.py file.
The bloom_filter_LD.py file is the one that should be compiled
