# geordrak2
There are two files in this repo. Their functionality is explained below

Bloom_functions

In this file are the functions that are used to interact with a bloom filter. These functions can be used to:
1. Add an element to the bloom filter
2. Check if a certain element is in the bloom filter
3. View the content of the bloom filter


Bloom filter test

This file is used to test the Bloom_function. 
Here we create a bloom filter and fill it with the elements "e", "f" and "m". Then we view the content of the bloom filter. Finaly, we check if the element "qwerty" is in the set. 
The answer for the final question is yes, but that doesn't mean that the functions are not working properly. We know that bloom filters can return false positive answers and ths is one of theese cases
