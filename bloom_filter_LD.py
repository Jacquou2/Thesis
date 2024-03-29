from eth_bloom import BloomFilter
from bf_function import Compare_BF_BF, Create_Blockchain_Data, Loaded_Blockchain, Test_Loaded_Blockchain_Time_performance
import matplotlib.pyplot as plt
import numpy as np
import time
from numpy import transpose


##  ## First Create a Blockchain Database locally, to run tests more efficiently  ##  ##
# # We create a Database with Blockchains containing all combinations of the following parameters
# # Blocks = 1, 10, 100, 1000, 10000
# # Elements in each block = 1, 10, 100, 1000, 10000
# # This database is stored locally in my computer in the path = "C:/Users/user/PycharmProjects/Bloom Filters/Blockchain Database/"
# # This process needs to be executed only once, this is why it is commented # #


# Blocks = [1000]
# Elements_in_each_block = [100000]
#
# for elements in Elements_in_each_block:
#     for blocks in Blocks:
#         Create_Blockchain_Data(blocks,elements)

# Create_Blockchain_Data(1000,100000)




# Number_of_blocks = 1000
# Number_of_elements = 1000
#
#
# Blockchain = Loaded_Blockchain(Number_of_blocks, Number_of_elements)
# Blockchain.Retrieve_Element_BruteForce(b'0.6166500426836184')
# print("The element is in the block:",Blockchain.Block_numbers_retrieved_BruteForce," (brute force)")
# print("The Execution time is:",Blockchain.ExTime_retrieve_BruteForce,"seconds\n")
#
#
# Blockchain2 = Loaded_Blockchain(Number_of_blocks, Number_of_elements)
# Blockchain2.Retrieve_Element_BloomFIlter(b'0.6166500426836184')
# print("The element is in the block:",Blockchain2.Block_numbers_retrieved_BloomFilter," (bloom filters)")
# print("The Execution time is:",Blockchain2.ExTime_retrieve_BloomFilter,"seconds\n")
#
#
# Blockchain3 = Loaded_Blockchain(Number_of_blocks, Number_of_elements)
# Blockchain3.Retrieve_Element_BloomFIlter2(b'0.6166500426836184')
# print("The element is in the block:",Blockchain3.Block_numbers_retrieved_BloomFilter2," (bloom filters2)")
# print("The Execution time is:",Blockchain3.ExTime_retrieve_BloomFilter2,"seconds\n")
#
#
# Blockchain.Check_bloom_filters_for_element(b'0.6166500426836184')
# a = Blockchain.Block_numbers_of_positive_BF
# print(len(a))






Number_of_Blocks_toTest = [1, 10, 100, 1000, 10000]
Number_of_Elements_toTest = [1, 10, 100, 1000, 10000, 100000]


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

# print(BruteForce_list, "\n\n", BloomFilter_list,"\n", BruteTime + BruteTime_Comp,"\n", BloomTime+ BloomTime_Comp)

BruteForce_list = transpose(np.array(BruteForce_list))
BloomFilter_list = transpose(np.array(BloomFilter_list))


print("Resutls of the Brute Force Method:",BruteForce_list)
print("Resutls of the Bloom Filter Method:",BloomFilter_list)
print("Execution time of the Brute Force Method is",BruteTime,"seconds")
print("Execution time of the Bloom Filter Method is",BloomTime,"seconds")



data1 = BloomFilter_list
data2 = BruteForce_list

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






##  ##  Experiment 1  ##  ##
##  This Experiment is about measuring the execution time of the creation of Bloom filters.
##  The variables are 2, the number of bloom filters that are created and the number of elements contained in each bloom filter.
##  For each combination of the variables the time is measured.
##  The results are presented in the form of a heatmap.

# NumOfEle = [1, 10, 100, 1000]
# NumOfBFs = [1, 10, 100]
#
# Time_Results = RME_TO(NumOfEle, NumOfBFs)
# #Per_Results = RME_IO(NumOfEle, NumOfBFs)
#
# Heatmap(Time_Results, NumOfEle, NumOfBFs, "Number of BFs","Number of Elements in each BF", "Time(seconds) required for BF construction")
# # Heatmap(Per_Results, NumOfEle, NumOfBFs,"Number of BFs","Number of Elements in each BF","Percentage(%) that BF is filled")
# plt.show()


##  ##  Experiment 2  ##  ##
##  In this Experiment we measure the time required for the creation o 1 bloom filter changing the number of elements of the bloom filter.


# NumOfEle = [1, 10, 100, 1000, 10000, 100000]
# NumOfBFs = [1]
#
# Time_Results = RME_TO(NumOfEle,NumOfBFs)
# Per_Results = RME_IO(NumOfEle, NumOfBFs)
#
#
# Time_Results = [Time_Results[v][0] for v in range(len(Time_Results))]
# Per_Results = [Per_Results[v][0] for v in range(len(Per_Results))]
# plt.title("Performance of BF (log scale)")
# plt.xlabel("Number of Elements in each BF")
# plt.ylabel("Time (seconds)")
# plt.xscale("log")
# # plt.yscale("log")
# plt.subplot(1, 2, 1)
# plt.plot(np.array(NumOfEle),np.array(Time_Results),"o--")
# plt.subplot(1, 2, 2)
# # plt.xscale("linear")
# # plt.yscale("linear")
# plt.plot(np.array(NumOfEle),np.array(Per_Results),"o--")
# plt.show()


# plot_line(Time_Results,NumOfEle,"Number of Elements in each BF", "Time (seconds)","Performance of BF (log scale)")
# plot_line(Per_Results,NumOfEle,"Number of Elements in each BF","Percentage(%) of the bloom filter that is filled","Performance of BF (log scale)")




 #  Plot Results  #  #
# fig, ax = plt.subplots()
# im = ax.imshow(np.array(Time_Results))
#
# ax.set_yticks(np.arange(len(NumOfEle)))
# ax.set_yticklabels(labels=[str(x) for x in NumOfEle])
# ax.set_xticks(np.arange(len(NumOfBFs)))
# ax.set_xticklabels(labels=[str(x) for x in NumOfBFs])
#
# ax.set_ylabel("Number of Elements in each BF")
# ax.set_xlabel("Number of BFs")
#
# for i in range(len(NumOfEle)):
#     for j in range(len(NumOfBFs)):
#         text = ax.text(j, i, '{0:.3f}'.format(Time_Results[i][j]),ha="center", va="center", color="w")
#
# ax.set_title("Heatmap (seconds)")
# fig.tight_layout()
# plt.show()







# fig = plt.figure(figsize=(8, 3))
# ax1 = fig.add_subplot(projection='3d')
#
# top = [x*20 for x in Zelement]
# width = depth = 10
#
# ax1.bar3d(Xelement, Yelement, Zelement, width, depth, top)
# ax1.set_title('Shaded')
#
# plt.show()




# bf1 = Bloom_Filter_Experiment(10,4).Result()
# print(len(bf1[0][0]))
# print(bf1[1])
# print(sum(bf1[1]))

# print(Bloom_Filter_Experiment(12,5).Result() )




# # Record the start time of the program
# start = time.time()
#
# # Set the bloom filter
# b = BloomFilter()
#
# # Define the seed of the random generated numbers
# random.seed(0)
#
# # Create a list of random numbers
# NumOfElements = 100
# rlist = [str(int(random.random()*(10**str(random.random())[::-1].find('.')))) for x in [None]*NumOfElements]
#
# for x in rlist:
#     b.add(bytes(x,'utf-8'))
#
#
# # Print the indexes of 1s in the bloom filter
# indexes_1 = []
# for i in range(len(bin(b))):
#     if bin(b)[::-1][i] == "1":
#         indexes_1.append(i)
#
# # for i in indexes_1:
# #     print(i)
#
#
# print("Number of Elements inserted in the bloom filter: " + "\033[1m" + str(NumOfElements) + "\033[0m")
# print("Number of 1 in the bloom filter: ","\033[1m" + str(len(indexes_1)) + "\033[0m")
# print("The bloom filter is "+"\033[1m"+ '{0:.2f}'.format(len(indexes_1)/20.48) + "%" + "\033[0m" + " filled\n")
#
#
#
# # Record the end time of the program
# end = time.time()
# print("Execution time of the program: " + "\033[1m" + str((end-start) * 10**3) + "\033[0m" + " ms")
#
