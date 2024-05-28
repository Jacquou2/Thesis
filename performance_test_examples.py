import fake_data_functions
import real_Ethereum_data_functions
import matplotlib.pyplot as plt
import numpy as np
from numpy import transpose
import time

###   ###   ###   FAKE DATA PERFORMANCE TEST STARTS HERE   ###   ###   ###
##  ##  FAKE DATA CREATION  ##  ##
##  ## First Create a Blockchain Database locally, to run tests more efficiently  ##  ##
# # We create a Database with Blockchains containing all combinations of the following parameters
# # Blocks = 1, 10, 100, 1000, 10000
# # Elements in each block = 1, 10, 100, 1000, 10000
# # This database is stored locally in the computer
# # This process needs to be executed only once, and should be commented # # afterwards


Blocks = [1, 10, 100, 1000, 10000]
Elements_in_each_block = [1, 10, 100, 1000, 10000]

for elements in Elements_in_each_block:
    for blocks in Blocks:
        print("Blockchain with",blocks,"blocks and", elements,"elements is being created" )
        bf_function.Create_Blockchain_Data(blocks,elements)



##  ##  RUN FAKE DATA TEST  ##  ##
# To have more robust results we repeat the performance test iteration_times(variable) times and store the mean
# of the results. The differences in the results between each performance test are small but not insignificant
iteration_times = 5

# The Final_BruteForce_list and Final_BloomFilter_list are the lists in which the mean of the results of each iteration
# are stored
Number_of_Blocks_toTest = [1, 10, 100, 1000]
Number_of_Elements_toTest = [1, 10, 100, 1000]

Final_BruteForce_list = np.zeros((len(Number_of_Elements_toTest), len(Number_of_Blocks_toTest)))
Final_BloomFilter_list = np.zeros((len(Number_of_Elements_toTest), len(Number_of_Blocks_toTest)))

Final_Brute_time = 0
Final_Bloom_time = 0

for i in range(iteration_times):
    ## The Number_of_Blocks_toTest and the Number_of_Elements_toTest lists contain the elements on which the performance
    ## of the Brute force and the Bloom filter methods will be tested.
    ## The Every possible combination of these parameters will be tested, except the one for 10000 blocks of 10000 elements,
    ## due to memory constrains.


    ## To test the performance, the Test_Loaded_Blockchain_Time_performance function is used. The queried element is not
    ## located on the blockchain.
    ## The BruteForce_list is a 2d list on which the execution times for the Brute Force method are stored.
    ## The BloomFilter_list is a 2d list on which the execution times for the Bloom Filter method are stored.
    ## On the place where the mising combination should be, 0 is placed.
    ## The rows of the 2d lists that are created are the number of elements in each block, while the columns are the number of blocks
    BruteForce_list, BloomFilter_list, BruteTime, BloomTime = fake_data_functions.Test_Loaded_Blockchain_Time_performance(Number_of_Blocks_toTest, Number_of_Elements_toTest, b'query')

    Final_Brute_time += BruteTime
    Final_Bloom_time += BloomTime

    BruteForce_list = transpose(np.array(BruteForce_list))
    BloomFilter_list = transpose(np.array(BloomFilter_list))

    Final_BruteForce_list = np.add(Final_BruteForce_list, BruteForce_list)
    Final_BloomFilter_list = np.add(Final_BloomFilter_list, BloomFilter_list)

    print("Iteration: ",i)


Final_BruteForce_list = Final_BruteForce_list / iteration_times
Final_BloomFilter_list = Final_BloomFilter_list / iteration_times



print("Resutls of the Brute Force Method:",BruteForce_list)
print("Resutls of the Bloom Filter Method:",BloomFilter_list)
print("Execution time of the Brute Force Method is",Final_Brute_time,"seconds")
print("Execution time of the Bloom Filter Method is",Final_Bloom_time,"seconds")


## To Visualize the results, a heatmap of the performance of each method is ploted
data1 = Final_BloomFilter_list
data2 = Final_BruteForce_list

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Performance Comparison (seconds)')
im1 = ax1.imshow(np.array(data1),cmap= "seismic")
im2 = ax2.imshow(np.array(data2),cmap= "seismic")

ax1.set_yticks(np.arange(len(data1)))
ax1.set_yticklabels(labels=[str(x) for x in Number_of_Elements_toTest])
ax1.set_xticks(np.arange(len(data1[0])))
ax1.set_xticklabels(labels=[str(x) for x in Number_of_Blocks_toTest])

ax1.set_ylabel("Number of elements")
ax1.set_xlabel("Number of Blocks")

ax2.set_yticks(np.arange(len(data2)))
ax2.set_yticklabels(labels=[str(x) for x in Number_of_Elements_toTest])
ax2.set_xticks(np.arange(len(data2[0])))
ax2.set_xticklabels(labels=[str(x) for x in Number_of_Blocks_toTest])

ax2.set_ylabel("Number of elements")
ax2.set_xlabel("Number of Blocks")

for i in range(len(data1)):
    for j in range(len(data1[0])):
        text = ax1.text(j, i, '{0:.2f}'.format(data1[i][j]), ha="center", va="center", color="w")

for i in range(len(data2)):
    for j in range(len(data2[0])):
        text = ax2.text(j, i, '{0:.2f}'.format(data2[i][j]), ha="center", va="center", color="w")


ax1.set_title("Bloom filter")
ax2.set_title("Brute force")
fig.tight_layout()
plt.show()
###   ###   ###   FAKE DATA PERFORMANCE TEST ENDS HERE   ###   ###   ###


###   ###   ###   REAL DATA PERFORMANCE TEST   ###   ###   ###
##  ##  DATA SCRAPPING  ##  ##
# # This process needs to be executed only once, and should be commented # # afterwards

Ethereum_functions.Scrap_Blockchain_Data(19850000, 19850100)
Ethereum_functions.Scrap_Blockchain_Data(19860000, 19861000)


##  ##  RUN REAL DATA TEST  ##  ##

##  ##  Log retrieval Topic based comparison Offline  ##  ##
start = time.time()
real_Ethereum_data_functions.Log_Retrieval_TimeComparison_TopicBased_OfflineTest_plot((1, 1, 1), (19860000, 19861000), (19850000, 19850100))
end = time.time()
print("Total execution time of Log retrieval Topic based comparison Offline is: ", time.strftime("%H:%M:%S", time.gmtime(end-start)))


##  ##  Log retrieval Position based comparison Offline  ##  ##
start = time.time()
real_Ethereum_data_functions.Log_Retrieval_TimeComparison_PositionBased_OfflineTest_plot((1, 1, 1), (19860000, 19861000))
end = time.time()
print("Total execution time of Log retrieval Position based comparison Offline is: ", time.strftime("%H:%M:%S", time.gmtime(end-start)))



##  ##  Log retrieval Topic based comparison Online  ##  ##
start = time.time()
real_Ethereum_data_functions.Log_Retrieval_TimeComparison_TopicBased_OnlineTest_plot((1, 1, 1), (19850000, 19850100), (19860000, 19861000))
end = time.time()
print("Total execution time of Log retrieval Topic based comparison Online is: ",time.strftime("%H:%M:%S", time.gmtime(end-start)))


##  ##  Log retrieval Position based comparison Online  ##  ##
start = time.time()
real_Ethereum_data_functions.Log_Retrieval_TimeComparison_PositionBased_OnlineTest_plot((1, 1, 1), (19850000, 19850100))
end = time.time()
print("Total execution time of Log retrieval Position based comparison Online is: ", time.strftime("%H:%M:%S", time.gmtime(end-start)))


