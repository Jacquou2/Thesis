# Evaluating the Performance of Bloom Filters on the Ethereum Blockchain

# Ethereum Performance tests
In this repo the bloom filter retrieval method and the brute force retrieval method are compared. Three test are presented here.

## Performance tests specifications
This repo is about viewing the performance of the Element retrieval in a blockchain. 
Two methods are compared here, the brute force method in which every item in every block is checked and the bloom filter method in which only the blocks with positive bloom filter resposes are checked.

The two methods are compared in fake data and real Ethereum blockchain data. The comparison in real Ethereum data can be offline or online.

### Fake data
In this test random data that do not have any corelation with the Ethereum blockchain are used.
In order to reduce the excecution time, a static database is created and stored in computer memory permanently. 
The data that are used in this test are randomly generated numbers. The test requires a database with multiple datasets to run. 
The datasets are blockchains consisting of random integers that represent the logs. 
For the data creation, the number of blocks and number of elements must be specified in a list format.
For example, number of blocks = [1, 10, 100] and number of elemnents = [1, 10, 100].
In the test, there will be ane blockchain for each possible combination of the two lists, so 9 blockchains in this example.
The retrieval time of an element that doesn't exist in any of the blockchains will be calculated.

The results of this performance test are ploted in a heatmap. In the position where the missing combination is, 0 is placed. 
The results are calculated in seconds.

### Real Ethereum data offline 
In this test, the performance is compared in data that are scrapped from the Ethereum blockchain. 
To run this test the user must first scrap the data from the Ethereum blockchain and then run the offline performance comparison test.
The test is then run locally in the scrapped dataset.

The advantage of this method is that it requires less time than the online method when the dataset has been created.
Although data scrapping can require a lot of time, the log retrieval time is significally less in the offline retrieval compared to the online.

### Real Ethereum data online
In this test, the performance is compared in data from the Ethereum blockchain. 
To run this test, it is also required to scrap the data from the Ethereum bockchain.
The difference from the offline test is that in this test, the retrieval is online. 

The advantage of this method is that it's results are more realistic because they refer to the actual retrieval time from the blockchain. 
The disadvantade is that the time required to run a test is much higher that the offline method. 

### Real Ethereum data tests
Two tests can be run in the real Ethereum data. The *Performance Comparison Position based test* and the *Performance Comparison Topic based test*.

**The Performance Comparison Position based test**
This test compares the log retrieval time of bloom filter/brute force when a log is located in the start, middle and end of the query block range. 

For this test the logs that are retrieved are located in the start (first 10% of the queried blocks), in the middle (45-55% of the queried blocks) and in the end (last 10% of the queried blocks).
For the test to be robust, the logs that are selected in each category have the same number of topics.
That means that if there are 10 1-topic logs in the start, there also need to be 10 1-topic logs in the middle and another 10 1-topic logs in the end
Therefore, the number of 1-topic, 2-topic and 3-topic logs is the same for the start, middle and end logs and needs to be specified.

The result of the test is a grouped bar plot. On the x-axis are the categories *logs at the start*, *logd at the middle*, *logs at the end* and *tatal logs*.
On the y-axis is the mean log retrieval time in seconds.

**The Performance Comparison Topic based test**
This test compares the log retrieval time of bloom filter/brute force between logs that have 1, 2 or 3 topics. The retrieval time for logs that are not on the specified block range is also calculated.

For this test, the logs that are selected have either 1, 2 or 3 topics and are in a random block in the specified block range.
Besides these logs, there are also logs from a different dataset that have 1, 2 or 3 topics and are not in the specified block range that are selected.

The result of the test is a grouped bar plot. On the x-axis are the categories logs *one topic logs*, *two topic logs*, *three topic logs* and *total*.
In each category there are 4 bars, 2 bars indicating the bloom filter retrieval time for existing and non existing logs and another 2 bars for the brute force retrieval time for existing and non existing logs.
On the y-axis is the mean log retrieval time in seconds.

## How to run a test
In order to run a test, the following instructions must be followed
### Fake data test
To run a fake data test, follow the steps:
1. create random data 
2. test the retrieval time of the random data 

**Creating random data**
First specify the number of blocks and elements in each block that the test should have in the Blocks and Elements_in_each_block lists.
Then create a dataset for every combination of the lists, like the code bellow

```
Blocks = [1, 10, 100, 1000, 10000]
Elements_in_each_block = [1, 10, 100, 1000, 10000]

for elements in Elements_in_each_block:
    for blocks in Blocks:
        print("Blockchain with",blocks,"blocks and", elements,"elements is being created" )
        bf_function.Create_Blockchain_Data(blocks,elements)
```

**test the retrieval time of the random data**
After the dataset creation, just call the function Test_Loaded_Blockchain_Time_performance that performes the test and returns the results. 
The arguments of the function are the Number_of_Blocks_toTest, Number_of_Elements_toTest and the word to query.
The code bellow is an example
```
BruteForce_list, BloomFilter_list, BruteTime, BloomTime = bf_function.Test_Loaded_Blockchain_Time_performance(Number_of_Blocks_toTest, Number_of_Elements_toTest, b'query')

BruteForce_list and BloomFilter_list can then be ploted in the form of a heatmap as shown in the code in the performance_test_examples.py file
```

### Real data topic based test
To run this test, first scrap two dataset, the main dataset in which the retrieval time will be tested and the second dataset from which the non existing logs are scraped.
To scrap the datasets, use the following code:

Ethereum_functions.Scrap_Blockchain_Data(Starting_block_number, Ending_block_number)

To run the test, use the following code for offline retrieval:

```
Ethereum_functions.Log_Retrieval_TimeComparison_TopicBased_OfflineTest_plot((Number_of_1_topic_logs, Number_of_2_topic_logs, Number_of_3_topic_logs), (Starting_block_number_Main_Dataset, Ending_block_number_Main_Dataset), (Starting_block_number_Secondary_Dataset, Ending_block_number_Secondary_Dataset))
```

Or the following code for online retrieval:

```
Ethereum_functions.Log_Retrieval_TimeComparison_TopicBased_OnlineTest_plot((Number_of_1_topic_logs, Number_of_2_topic_logs, Number_of_3_topic_logs), (Starting_block_number_Main_Dataset, Ending_block_number_Main_Dataset), (Starting_block_number_Secondary_Dataset, Ending_block_number_Secondary_Dataset))
```

This code produces the plot and stores the individual retrieval times of each element in a file locally

### Real data position based test
To run this test, first scrap the dataset in which the retrieval time will be tested.
To scrap the dataset, use the following code:
```
Ethereum_functions.Scrap_Blockchain_Data(Starting_block_number, Ending_block_number)
```

To run the test, use the following code for offline retrieval:
```
Ethereum_functions.Log_Retrieval_TimeComparison_PositionBased_OfflineTest_plot((Number_of_1_topic_logs, Number_of_2_topic_logs, Number_of_3_topic_logs), (Starting_block_number_Main_Dataset, Ending_block_number_Main_Dataset), (Starting_block_number_Secondary_Dataset, Ending_block_number_Secondary_Dataset))
```
Or the following code for online retrieval:
```
Ethereum_functions.Log_Retrieval_TimeComparison_PositionBased_OnlineTest_plot((Number_of_1_topic_logs, Number_of_2_topic_logs, Number_of_3_topic_logs), (Starting_block_number_Main_Dataset, Ending_block_number_Main_Dataset), (Starting_block_number_Secondary_Dataset, Ending_block_number_Secondary_Dataset))
```
This code produces the plot and stores the individual retrieval times of each element in a file locally

## Exaples 
Examples of how to run the test can be found in the performance_test_exaples.py file

The results of the tests should resemble the following

**fake data test**

![Performance Comparison (iter=20)](https://github.com/Jacquou2/Thesis/assets/115991799/4ba7c000-ebbf-4bba-9756-d99c09ce76a7)


**real data topic based test**

![Performance Comparison Topic based (1000,1000,1000)](https://github.com/Jacquou2/Thesis/assets/115991799/46ff3472-3dae-4ebd-89fb-f8f4b6b57db1)


**real data position based test**

![Performance Comparison Position based (1000,1000,1000)](https://github.com/Jacquou2/Thesis/assets/115991799/68455fbe-f79d-427c-b6a2-53586502b7cc)
