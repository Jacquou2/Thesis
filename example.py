import real_Ethereum_data_functions
import group_bloom_filter
import dti_bloom_filter
import compressed_bloom_filter


##  ##  ##  ##  EXAMPLES FILE  ##  ##  ##  ##
## In this file there are examples on how to run the tests described on the thesis.

## The tests in this file are in a smaller scale than the ones depicted in the thesis.

## The first test refers to the creation of the scrapping dataset.
## This is necessary for almost every test.
## The datasets that were scrapped to run the thesis tests are (19860000, 19861000) and (19860000, 19861000).
## It is recommended not to scrapp datasets containing more than 10.000 blocks due to time constaints.
## The data scrapping process doesn't need to be repeated.
## Before the tests are executed, the local path to store the datasets needs to be defined.
## This path needs to be defined in each of the imporeted files.
## Also the Infura API key needs to be defined.

##  ##  Data Scrapping  ##  ##
real_Ethereum_data_functions.Scrap_Blockchain_Data(19850000, 19850100)


##  ##  ##  Time Comparisson between the bloom filter and the brute force retrieval methods  ##  ##  ##
## The following tests are shown in Chapter 3 of the thesis.

##  ##  Offline Time Comparisson Bloom filter - Brute force  ##  ##
real_Ethereum_data_functions.Log_Retrieval_TimeComparison_TopicBased_OfflineTest_plot((5,5,5), (19850000, 19850100))

##  ##  Online Time Comparisson Bloom filter - Brute force  ##  ##
real_Ethereum_data_functions.Log_Retrieval_TimeComparison_TopicBased_OnlineTest_plot((5,5,5), (19850000, 19850100))


##  ##  ##  Group bloom filter tests  ##  ##  ##
## The following tests are shown in Chapter 4 of the thesis.
## The test refers to the performance of the group bloom filters, compared to the bloom filter and brute force methods.
## To test the group bloom filter methods it is necessary to first create the group bloom filters.
##  ##  Group bloom filter creation  ##  ##
group_bloom_filter.Create_Group_BF_from_Scraped_data_4G_Method1(19850000, 19850100)
group_bloom_filter.Create_Group_BF_from_Scraped_data_4G_Method2(19850000, 19850100)
group_bloom_filter.Create_Group_BF_from_Scraped_data_4G_Method3(19850000, 19850100)
group_bloom_filter.Create_Group_BF_from_Scraped_data_4G_Method4(19850000, 19850100)


## There are 4 group bloom filter methods described in the thesis.
## The method to test can be passed as an argument in the test function.
## The coding of the methods is the following:     Group bloom filter Method 1 -> 1
##                                                 Group bloom filter Method 2 -> 2
##                                                 Group bloom filter Method 3 -> 3
##                                                 Group bloom filter Method 4 -> 4
## In this example all the group bloom filter methods are tested
group_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_GBF_plot(100, (19850000, 19850100), 1)
group_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_GBF_plot(100, (19850000, 19850100), 2)
group_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_GBF_plot(100, (19850000, 19850100), 3)
group_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_GBF_plot(100, (19850000, 19850100), 4)



##  ##  ##  DTI bloom filter tests  ##  ##  ##
## The test refers to the performance of the dti bloom filters, compared to the bloom filter and brute force methods.
## To test the dti bloom filter methods it is necessary to first create the group bloom filters.
##  ##  DTI bloom filter creation  ##  ##
##  First DTI method family  ##
dti_bloom_filter.Create_DTI_M1_BF_from_Scraped_data(19850000, 19850100)
dti_bloom_filter.Create_DTI_M2_BF_from_Scraped_data(19850000, 19850100)
dti_bloom_filter.Create_DTI_M3_BF_from_Scraped_data(19850000, 19850100)
dti_bloom_filter.Create_DTI_M8_BF_from_Scraped_data(19850000, 19850100)

##  Second DTI method family  ##
dti_bloom_filter.Create_DTI_M6_BF_from_Scraped_data(19850000, 19850100)
dti_bloom_filter.Create_DTI_M7_BF_from_Scraped_data(19850000, 19850100)

##  Third DTI method family  ##
dti_bloom_filter.Create_DTI_M11_BF_from_Scraped_data(19850000, 19850100)
dti_bloom_filter.Create_DTI_M12_BF_from_Scraped_data(19850000, 19850100)
dti_bloom_filter.Create_DTI_M13_BF_from_Scraped_data(19850000, 19850100)

## Compressed DTI ##
dti_bloom_filter.Create_DTI_M14_BF_from_Scraped_data(19850000, 19850100)

## There are 10 dti bloom filter methods described in the thesis.
## The method to test can be passed as an argument in the test function.
## The coding of the methods is the following: DTI Method 1.1 -> 1, DTI Method 1.2 -> 2, DTI Method 1.3 -> 3, DTI Method 1.4 -> 8
#                                              DTI Method 2.1 -> 6, DTI Method 2.2 -> 7
#                                              DTI Method 3.1 -> 11, DTI Method 3.2 -> 12, DTI Method 3.3 -> 13
#                                              Compressed DTI -> 14
## In this example all the dti methods are tested
dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 1)
dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 2)
dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 3)
dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 8)

dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 6)
dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 7)

dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 11)
dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 12)
dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 13)

dti_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(100, (19850000, 19850100), 14)



##  ##  ##  Compressed bloom filter tests  ##  ##  ##
## The following tests are shown in Chapter 4 of the thesis.
## The test refers to the performance of the compressed bloom filters, compared to the bloom filter and brute force methods.
## The compressed bloom filter methods are the compressed bloom filter and the dynamically compressed bloom filter.
## To test the compressed bloom filter methods it is necessary to first create the compressed bloom filters.
##  ##  Compressed bloom filter creation  ##  ##
compressed_bloom_filter.Create_dynamic_compressed_bf_dataset((19850000, 19850100))
compressed_bloom_filter.Create_compressed_bf_dataset_M1((19850000, 19850100))

## In this example both the compressed bf and the dynamically compressed bf methids are checked
compressed_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_DCBF_plot(10, (19850000, 19850100))
compressed_bloom_filter.Log_Retrieval_Random_TopicBased_Bloom_Brute_CompBF_plot(100, (19850000, 19850100))






