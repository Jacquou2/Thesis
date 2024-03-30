from bf_function import Test_Loaded_Blockchain_Time_performance
import matplotlib.pyplot as plt
import numpy as np
from numpy import transpose


##  ## First Create a Blockchain Database locally, to run tests more efficiently  ##  ##
# # We create a Database with Blockchains containing all combinations of the following parameters
# # Blocks = 1, 10, 100, 1000, 10000, 100000
# # Elements in each block = 1, 10, 100, 1000, 10000, 100000
# # This database is stored locally in my computer in the path = "C:/Users/user/PycharmProjects/Bloom Filters/Blockchain Database/"
# # This process needs to be executed only once, this is why it is commented # #
# # The actual database that is stored in my computer does not have the combination for 10000 blocks of 10000 elements
# # due to memory constrains. It is estimated that storing this combination requires more than 20Gb


# Blocks = [1, 10, 100, 1000, 10000, 100000]
# Elements_in_each_block = [1, 10, 100, 1000, 10000, 100000]
#
# for elements in Elements_in_each_block:
#     for blocks in Blocks:
#         Create_Blockchain_Data(blocks,elements)




##  ## THE PERFORMANCE TEST BEGINS HERE  ##  ##


# To have more robust results we repeat the performance test iteration_times(variable) times and store the mean
# of the results. The differences in the results between each performance test are small but not insignificant
iteration_times = 20

# The Final_BruteForce_list and Final_BloomFilter_list are the lists in which the mean of the results of each iteration
# are stored
Final_BruteForce_list = np.zeros((6, 5))
Final_BloomFilter_list = np.zeros((6, 5))
for i in range(iteration_times):
    ## The Number_of_Blocks_toTest and the Number_of_Elements_toTest lists contain the elements on which the performance
    ## of the Brute force and the Bloom filter methods will be tested.
    ## The Every possible combination of these parameters will be tested, except the one for 10000 blocks of 10000 elements,
    ## due to memory constrains.
    Number_of_Blocks_toTest = [1, 10, 100, 1000, 10000]
    Number_of_Elements_toTest = [1, 10, 100, 1000, 10000, 100000]

    ## To test the performance, the Test_Loaded_Blockchain_Time_performance function is used. The queried element is not
    ## located on the blockchain.
    ## The BruteForce_list is a 2d list on which the execution times for the Brute Force method are stored.
    ## The BloomFilter_list is a 2d list on which the execution times for the Bloom Filter method are stored.
    ## On the place where the mising combination should be, 0 is placed.
    ## The rows of the 2d lists that are created are the number of elements in each block, while the columns are the number of blocks
    BruteForce_list, BloomFilter_list, BruteTime, BloomTime = Test_Loaded_Blockchain_Time_performance([1, 10, 100, 1000, 10000], [1, 10, 100, 1000, 10000], b'query')
    BruteForce_list_Comp, BloomFilter_list_Comp, BruteTime_Comp, BloomTime_Comp = Test_Loaded_Blockchain_Time_performance([1, 10, 100, 1000],[100000], b'query')

    BruteForce_list[0].append(BruteForce_list_Comp[0][0])
    BruteForce_list[1].append(BruteForce_list_Comp[1][0])
    BruteForce_list[2].append(BruteForce_list_Comp[2][0])
    BruteForce_list[3].append(BruteForce_list_Comp[3][0])
    BruteForce_list[4].append(0)
    BloomFilter_list[0].append(BloomFilter_list_Comp[0][0])
    BloomFilter_list[1].append(BloomFilter_list_Comp[1][0])
    BloomFilter_list[2].append(BloomFilter_list_Comp[2][0])
    BloomFilter_list[3].append(BloomFilter_list_Comp[3][0])
    BloomFilter_list[4].append(0)

    BruteTime += BruteTime_Comp
    BloomTime += BloomTime_Comp


    BruteForce_list = transpose(np.array(BruteForce_list))
    BloomFilter_list = transpose(np.array(BloomFilter_list))

    Final_BruteForce_list = np.add(Final_BruteForce_list, BruteForce_list)
    Final_BloomFilter_list = np.add(Final_BloomFilter_list, BloomFilter_list)


Final_BruteForce_list = Final_BruteForce_list / iteration_times
Final_BloomFilter_list = Final_BloomFilter_list / iteration_times



print("Resutls of the Brute Force Method:",BruteForce_list)
print("Resutls of the Bloom Filter Method:",BloomFilter_list)
print("Execution time of the Brute Force Method is",BruteTime,"seconds")
print("Execution time of the Bloom Filter Method is",BloomTime,"seconds")


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

##  ## THE PERFORMANCE TEST ENDS HERE  ##  ##




