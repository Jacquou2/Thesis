import time
from eth_bloom import BloomFilter
from web3 import Web3
import winsound
import random
import matplotlib.pyplot as plt
import numpy as np


##  Parameters  ##
global_path = your_path
API_key = your_Infura_API_key


# This funtion is used for the creation of the Scrap Blockchain Database
def Scrap_Blockchain_Data(Starting_block: int, Ending_block: int) -> None:
    # This function scrapes data from the Ethereum blockchain and stores them locally.
    # Two files are created in computer memory in the specified path.
    # The file that is named "Logs for blocks x to y" contains all the logs that are located in the blocks x to y.
    # The file that is named "Bloom filters for blocks x to y" contains the bloom filters of the blocks x to y.

    web3 = Web3(Web3.HTTPProvider(API_key))

    # path: local path
    path = global_path + "Scrap Blockchain Database/"


    # File_BloomFilters: file in which the bloom filters are stored
    # File_Logs: file in which the logs are stored
    File_BloomFilters = open(path + "Bloom filters for blocks " + str(Starting_block)+ " to " + str(Ending_block), "w")
    File_Logs = open(path + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    get_block_error_counter = 0
    event_filter_error_counter = 0
    get_all_entries_error_counter = 0

    for count, block_number in enumerate(range(Starting_block, Ending_block)):
        ## Storing the bloom filter ##
        ## The bloom filter is stored in the form of an integer. Each bloom filter is separated from the next with \n.

        while True:
            try:
                block = web3.eth.get_block(block_number)
                break
            except:
                print("get_block error in block:",block_number)
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                get_block_error_counter = get_block_error_counter + 1


        # bloom_filter: integer form of the bloom filter
        bloom_filter = int(block["logsBloom"].hex(), 0)
        File_BloomFilters.write(str(bloom_filter) + "\n")

        ## Storing the logs ##

        ## The logs are stored in the following form log = "address topic1 topic2 topic3 topic4 transactionHash"
        ## The number of topics is 0,1,2,3 or 4 so topic1, tipic2, topic3 and topic4 may not exist.
        ## The address, topics and transactionHash are in hexadecimal form.
        ## The logs of the same block are separated by ",".
        ## The last log of a block is separated from the first log of the next block by ",\n"

        ## Example ##
        ## The database that is created looks like this:
        ## 0xC02 0xddf 0xff8 0x3c9 0x11b,0x2b8 0x3ef 0x3c9 0xff8 0x11b, ...
        ## Where 0xC02 is the address, 0xddf 0xff8 0x3c9 are the topics, 0x11b is the transactionHash of the first log

        while True:
            try:
                event_filter = web3.eth.filter({
                    "fromBlock": block_number,
                    "toBlock": block_number,
                    # 'topics':[event_signature_hash, "0x000000000000000000000000000000000000000000000000000000000000000a"],
                })
                break
            except:
                print("event_filter error in block:",block_number)
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                event_filter_error_counter = event_filter_error_counter + 1

        # Entries: list of all the logs of the block

        while True:
            try:
                Entries = event_filter.get_all_entries()
                break
            except:
                print("get_all_entries error in block:",block_number)
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                get_all_entries_error_counter = get_all_entries_error_counter + 1



        for entry in Entries:
            File_Logs.write(str(entry["address"]) + " ")
            topic_list = entry["topics"]
            for topic in topic_list:
                File_Logs.write(str(topic.hex()) + " ")
            File_Logs.write(str(entry["transactionHash"].hex()))
            File_Logs.write(",")
        File_Logs.write("\n")

        print(count, " blocks have been created")

    print("get_block errors occurred: ", get_block_error_counter)
    print("event_filter errors occurred: ", event_filter_error_counter)
    print("get_all_entries errors occurred: ", get_all_entries_error_counter)

    File_BloomFilters.close()
    File_Logs.close()



    # Transactions = block["transactions"]
    # for transaction in Transactions:
    #     Receipt = web3.eth.get_transaction_receipt(transaction)
    #     logs = Receipt["logs"]
    #     for log in logs:
    #         File_Logs.write(str(log["address"]) + " ")
    #         topic_list = log["topics"]
    #         for topic in topic_list:
    #             File_Logs.write(str(topic.hex()) + " ")
    #         File_Logs.write(",")
    # File_Logs.write("\n")
    # print(count, " blocks have been created")


# This function is used to search a log (locally) utilizing the bloom filters.
def Log_Retrieval_bloom_filter_Offline(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none"):
    # This function needs the address and topics of the log to query and optionally the transactionHash.
    # It is also necessary to specify the blocks to query with the Starting_block and Ending_block parameters.
    # The return of the function are two lists. The first one for the blocks in which the log was found and the second
    # one for the corresponding log indexes in each block.
    # If the log is not found, the function returns two empty lists

    time1 = time.time()

    path = global_path + "/Scrap Blockchain Database/"
    File_Logs = open(path + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_BloomFilters = open(path + "Bloom filters for blocks " + str(Starting_block)+ " to "+ str(Ending_block), "r")

    blocks_of_found_element = []
    positions_of_found_element_in_block = []

    # All_logs is the variable containing all the logs of all the blocks
    All_logs = File_Logs.readlines()
    time2 = time.time()

    blocks_checked_list = []
    num_of_bfs_checked = 0
    for count, block_number in enumerate(range(Starting_block, Ending_block)):
        # The block_logs list contains all the logs of one block
        block_logs = All_logs[count].split(",")

        bloom_filter = BloomFilter(int(File_BloomFilters.readline()))

        num_of_bfs_checked += 1
        topic_flag = 1
        for topic in topics:
            if bytes.fromhex(topic[2:]) not in bloom_filter:
                topic_flag = 0
                break

        if bytes.fromhex(address[2:]) in bloom_filter:
            if topic_flag:
                blocks_checked_list.append(count)
                # print("TBF Block number",block_number)
                for count2, log in enumerate(block_logs):
                    log = log.split(" ")      ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                    if address == log[0]:     ##  the number of topics is 0,1,2,3 or 4
                        if topics == log[1:-1]:
                            if transactionHash == "none":
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count2)
                                # results.append((block_number,count2))
                                # break
                            elif transactionHash == log[-1]:
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count2)
                                # results.append((block_number,count2))
                                # break
        if (transactionHash != "none") & (blocks_of_found_element != []): break
    time3 = time.time()
    # print("|||")

    return blocks_of_found_element, positions_of_found_element_in_block, time3-time1, (blocks_checked_list,num_of_bfs_checked)



# This function is used to search a log (locally) without utilizing the bloom filters.
def Log_Retrieval_brute_force_Offline(address: str, topics: list, Starting_block: int, Ending_block: int, transactionHash:str="none"):
    # This function needs the address and topics of the log to query and optionally the transactionHash.
    # It is also necessary to specify the blocks to query with the Starting_block and Ending_block parameters.
    # The return of the function are two lists. The first one for the blocks in which the log was found and the second
    # one for the corresponding log indexes in each block.
    # If the log is not found, the function returns two empty lists

    time1 = time.time()

    path = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    blocks_of_found_element = []
    positions_of_found_element_in_block = []

    # All_logs is the variable containing all the logs of all the blocks
    All_logs = File_Logs.readlines()

    time2 = time.time()
    # every log of every block is checked
    for count,block_number in enumerate(range(Starting_block, Ending_block)):
        # block_logs is the logs that are contained in the block
        block_logs = All_logs[count].split(",")

        for count, log in enumerate(block_logs):
            # log is a list of the following form log = [address, topic1, topic2, topic3, topic4, transactionHash]
            log = log.split(" ")

            # Checking if the log is identical with the one that was specified in the function parameters
            if address == log[0]:
                if topics == log[1:-1]:
                    if transactionHash == "none":
                        blocks_of_found_element.append(block_number)
                        positions_of_found_element_in_block.append(count)
                    elif transactionHash == log[-1]:
                        blocks_of_found_element.append(block_number)
                        positions_of_found_element_in_block.append(count)
        # if the transactionHash is specified the search is stopped when one log is found otherwise the search continues
        if (transactionHash != "none") & (blocks_of_found_element != []): break
    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3-time1



# This function tests the Offline log retrieval time based on the log topic number
def Log_Retrieval_TimeComparison_TopicBased_OfflineTest_plot(Number_of_1_2_3_topic_logs: tuple, Scrap_database: tuple, Non_existing_log_database: tuple):
    # The arguments that are required are the number of 1 log topics, number of 2 log topics, number of 3 log topics,
    # this is given in the form of a tuple with 3 positions where 1st position is the number of 1 log topics,
    # 2nd position is the number of 2 log topics and 3rd position is the number of 3 log topics.
    #
    # The second argument is the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database
    #
    # The third argument is the non existing log database. This is the database from which the non existing logs are
    # selected to be queried in the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database
    #
    # The datasets are stored locally in the computer memory and are retrieved from the database when
    # the Scrap_database variable is given
    start = time.time()

    number_of_1_topic_logs, number_of_2_topic_logs, number_of_3_topic_logs = Number_of_1_2_3_topic_logs
    Starting_block, Ending_block = Scrap_database
    non_existing_starting_block, non_existing_ending_block = Non_existing_log_database

    path = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()

    File_Logs.close()

    ##  ##  Data Selection  ##  ##
    ##  Existing log selection  ##

    # one_topic_logs,two_topic_logs, three_topic_logs are the 1,2,3 topic logs that are randomly selected to be queried
    one_topic_logs = []
    two_topic_logs = []
    three_topic_logs = []

    random.seed(0)

    flag = 1
    # The while loop is terminated only when the flag is set to 0
    while flag == 1:
        # random_block_number: a random number between the number 0 and the number of blocks in the database
        random_block_number = random.randint(0,Ending_block - Starting_block - 1)

        # The Entries list is a list containing all the logs of the specific block
        Entries = All_logs[random_block_number].split(",")

        # entry is the random entry that is selected.
        # entry is initially a string but becomes a list representing the log in the following manner:
        # entry = [address, topic1, topic2, topic3, topic4, transactionHash]
        entry = random.choice(Entries) # entry: string
        entry = entry.split(" ") # entry: list
        entry.append(str(random_block_number))

        # num_of_topics is the number of topics
        num_of_topics = len(entry[1:-2])

        # if the number of topics is 1 and the one_topic_logs list is not full, then the entry is appended in the
        # one_topic_logs.
        # if the number of topics is 2 and the two_topic_logs list is not full, then the entry is appended in the
        # two_topic_logs.
        # if the number of topics is 3 and the three_topic_logs list is not full, then the entry is appended in the
        # three_topic_logs.
        if (num_of_topics == 1) & (len(one_topic_logs) < number_of_1_topic_logs):
            one_topic_logs.append(entry)
        elif (num_of_topics == 2) & (len(two_topic_logs) < number_of_2_topic_logs):
            two_topic_logs.append(entry)
        elif (num_of_topics == 3) & (len(three_topic_logs) < number_of_3_topic_logs):
            three_topic_logs.append(entry)

        # The while loop stops only when the one_topic_logs, two_topic_logs, three_topic_logs are full
        if (len(one_topic_logs) == number_of_1_topic_logs) & (len(two_topic_logs) == number_of_2_topic_logs) & (len(three_topic_logs) == number_of_3_topic_logs):
            flag = 0

    ##  Non existing log selection  ##

    File_non_existing_Logs = open(path + "Logs for blocks " + str(non_existing_starting_block) + " to " + str(non_existing_ending_block), "r")
    All_non_existing_logs = File_non_existing_Logs.readlines()
    File_non_existing_Logs.close()

    # non_exist_one_topic_logs,non_exist_two_topic_logs, non_exist_three_topic_logs are the non existing 1,2,3 topic
    # logs that are randomly selected to be queried
    non_exist_one_topic_logs = []
    non_exist_two_topic_logs = []
    non_exist_three_topic_logs = []

    num_of_non_exist_1_topic_logs = 0
    num_of_non_exist_2_topic_logs = 0
    num_of_non_exist_3_topic_logs = 0

    flag = 1
    # The while loop is terminated only when the flag is set to 0
    while flag == 1:
        # random_block_number: a random number between the number 0 and the number of blocks in the database
        random_block_number = random.randint(0, non_existing_ending_block - non_existing_starting_block - 1)

        # The Entries list is a list containing all the logs of the specific block
        Entries = All_non_existing_logs[random_block_number].split(",")

        # entry is the random entry that is selected.
        # entry is initially a string but becomes a list representing the log in the following manner:
        # entry = [address, topic1, topic2, topic3, topic4, transactionHash]
        entry = random.choice(Entries) # entry: string
        entry = entry.split(" ") # entry: list
        entry.append("NEB")


        # num_of_topics is the number of topics
        num_of_topics = len(entry[1:-2])

        # if the number of topics is 1 and the non_exist_one_topic_logs list is not full, then the entry is
        # appended in the one_topic_logs.
        # if the number of topics is 2 and the non_exist_two_topic_logs list is not full, then the entry is
        # appended in the two_topic_logs.
        # if the number of topics is 3 and the non_exist_three_topic_logs list is not full, then the entry is
        # appended in the three_topic_logs.
        if (num_of_topics == 1) & (len(non_exist_one_topic_logs) < number_of_1_topic_logs):
            non_exist_one_topic_logs.append(entry)

        elif (num_of_topics == 2) & (len(non_exist_two_topic_logs) < number_of_2_topic_logs):
            non_exist_two_topic_logs.append(entry)

        elif (num_of_topics == 3) & (len(non_exist_three_topic_logs) < number_of_3_topic_logs):
            non_exist_three_topic_logs.append(entry)

        # The while loop stops only when the non_exist_one_topic_logs, non_exist_two_topic_logs,
        # non_exist_three_topic_logs are full
        if (len(non_exist_one_topic_logs) == number_of_1_topic_logs) & (len(non_exist_two_topic_logs) == number_of_2_topic_logs) & (
                len(non_exist_three_topic_logs) == number_of_3_topic_logs):
            flag = 0



    ##  ##  Retrieval time recording  ##  ##

    # In the following file, the time required for each individual retrieval is stored. The file can be read as csv.
    # The file contains the block number of the log followed by the bloom filter retrieval time and the brute force
    # retrieval time. Each value is separated by comma and each log is separated by newline(\n). For the non existing
    # logs, in the block number there is "NEB" that stands for Non Existing Block
    # For example: 13,0.4255,0.5232
    #              22,0.3224,0.4011
    #              18,0.5622,0.5239
    #              NEB,0.8574,0.7889

    individual_time_file = open(global_path + "Individual retrieval time dataset/Time for each query(TB)(offline) ("+ str(number_of_1_topic_logs) + ", " + str(number_of_2_topic_logs) + ", " + str(number_of_3_topic_logs) + ") blocks " + str(Starting_block) + " to " + str(Ending_block), "w")


    ##  existing logs bloom filter retrieval time  ##

    # The following variables are used for time recording, each variable stores the time that is indicated by it's name.
    # For example, one_topic_bloom_time: stores the time required for the retrieval of all one topic logs using the
    # bloom filter method. These variables refer to the total time required.
    # These variables are later used to refer to the mean time.
    one_topic_bloom_time, two_topic_bloom_time, three_topic_bloom_time, total_topic_bloom_time = 0, 0, 0, 0
    one_topic_brute_time, two_topic_brute_time, three_topic_brute_time, total_topic_brute_time = 0, 0, 0, 0
    non_exist_one_topic_bloom_time, non_exist_two_topic_bloom_time, non_exist_three_topic_bloom_time, non_exist_total_topic_bloom_time = 0, 0, 0, 0
    non_exist_one_topic_brute_time, non_exist_two_topic_brute_time, non_exist_three_topic_brute_time, non_exist_total_topic_brute_time = 0, 0, 0, 0

    # One topic log retrieval time for bloom filter method and brute force method for existing logs
    for log in one_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time, blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        if block == []: print("Not found")
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()
        if block == []: print("Not found")


        one_topic_bloom_time = one_topic_bloom_time + individual_time_med - individual_time_start
        one_topic_brute_time = one_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")

    # Two topic log retrieval time for bloom filter method and brute force method for existing logs
    for log in two_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time, blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        if block == []: print("Not found")
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()
        if block == []: print("Not found")


        two_topic_bloom_time = two_topic_bloom_time + individual_time_med - individual_time_start
        two_topic_brute_time = two_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")

    # Three topic log retrieval time for bloom filter method and brute force method for existing logs
    for log in three_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time, blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        if block == []: print("Not found")
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()
        if block == []: print("Not found")


        three_topic_bloom_time = three_topic_bloom_time + individual_time_med - individual_time_start
        three_topic_brute_time = three_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")

    ##  Non existing logs bloom filter retrieval time  ##
    # One topic log retrieval time for bloom filter method and brute force method for non existing logs
    for log in non_exist_one_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time, blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()

        non_exist_one_topic_bloom_time = non_exist_one_topic_bloom_time + individual_time_med - individual_time_start
        non_exist_one_topic_brute_time = non_exist_one_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(log[-1] + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")
        if block != []: print("Found in ","one_topic_logs", "bloom")

    # Two topic log retrieval time for bloom filter method and brute force method for non existing logs
    for log in non_exist_two_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time, blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()

        non_exist_two_topic_bloom_time = non_exist_two_topic_bloom_time + individual_time_med - individual_time_start
        non_exist_two_topic_brute_time = non_exist_two_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(log[-1] + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")
        if block != []: print("Found in ", "two_topic_logs","bloom")

    # Three topic log retrieval time for bloom filter method and brute force method for non existing logs
    for log in non_exist_three_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time, blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()

        non_exist_three_topic_bloom_time = non_exist_three_topic_bloom_time + individual_time_med - individual_time_start
        non_exist_three_topic_brute_time = non_exist_three_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(log[-1] + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")
        if block != []: print("Found in ", "three_topic_logs","bloom")


    individual_time_file.close()

    # the total retrieval time is calculated for bloom filter and brute force, for existing and non existing logs
    total_topic_bloom_time = one_topic_bloom_time + two_topic_bloom_time + three_topic_bloom_time
    non_exist_total_topic_bloom_time = non_exist_one_topic_bloom_time + non_exist_two_topic_bloom_time + non_exist_three_topic_bloom_time
    total_topic_brute_time = one_topic_brute_time + two_topic_brute_time + three_topic_brute_time
    non_exist_total_topic_brute_time = non_exist_one_topic_brute_time + non_exist_two_topic_brute_time + non_exist_three_topic_brute_time

    # At this point the time refers to the mean time and not to the total time
    one_topic_bloom_time = one_topic_bloom_time/number_of_1_topic_logs
    two_topic_bloom_time = two_topic_bloom_time/number_of_2_topic_logs
    three_topic_bloom_time = three_topic_bloom_time/number_of_3_topic_logs
    total_topic_bloom_time = total_topic_bloom_time/(number_of_1_topic_logs+number_of_2_topic_logs+ number_of_3_topic_logs)

    non_exist_one_topic_bloom_time = non_exist_one_topic_bloom_time/number_of_1_topic_logs
    non_exist_two_topic_bloom_time = non_exist_two_topic_bloom_time/number_of_2_topic_logs
    non_exist_three_topic_bloom_time = non_exist_three_topic_bloom_time/number_of_3_topic_logs
    non_exist_total_topic_bloom_time = non_exist_total_topic_bloom_time/(number_of_1_topic_logs+number_of_2_topic_logs+ number_of_3_topic_logs)

    one_topic_brute_time = one_topic_brute_time/number_of_1_topic_logs
    two_topic_brute_time = two_topic_brute_time/number_of_2_topic_logs
    three_topic_brute_time = three_topic_brute_time/number_of_3_topic_logs
    total_topic_brute_time = total_topic_brute_time/(number_of_1_topic_logs+number_of_2_topic_logs+ number_of_3_topic_logs)

    non_exist_one_topic_brute_time = non_exist_one_topic_brute_time/number_of_1_topic_logs
    non_exist_two_topic_brute_time = non_exist_two_topic_brute_time/number_of_2_topic_logs
    non_exist_three_topic_brute_time = non_exist_three_topic_brute_time/number_of_3_topic_logs
    non_exist_total_topic_brute_time = non_exist_total_topic_brute_time/(number_of_1_topic_logs + number_of_2_topic_logs + number_of_3_topic_logs)

    ##  ##  Plot  ##  ##
    x = np.arange(4)
    bloom_measurments = [one_topic_bloom_time, two_topic_bloom_time, three_topic_bloom_time, total_topic_bloom_time]
    brute_measurments = [one_topic_brute_time, two_topic_brute_time, three_topic_brute_time, total_topic_brute_time]
    non_exist_bloom_measurments = [non_exist_one_topic_bloom_time, non_exist_two_topic_bloom_time, non_exist_three_topic_bloom_time, non_exist_total_topic_bloom_time]
    non_exist_brute_measurments = [non_exist_one_topic_brute_time, non_exist_two_topic_brute_time, non_exist_three_topic_brute_time, non_exist_total_topic_brute_time]
    width = 0.10

    # plot data in grouped manner of bar type
    plt.bar(x - 0.15, bloom_measurments, width, color='lightseagreen', label="Bloom filter")
    plt.bar(x - 0.05, brute_measurments, width, color='navy', label="Brute force")
    plt.bar(x + 0.05, non_exist_bloom_measurments, width, color='indianred', label="Bloom filter (non existing logs)")
    plt.bar(x + 0.15, non_exist_brute_measurments, width, color='darkred', label="Brute force (non existing logs)")

    plt.xticks(x, ['One topic logs\n(' + str(number_of_1_topic_logs) + ")", 'Two topic logs\n(' + str(number_of_2_topic_logs)+")", 'Three topic logs\n(' + str(number_of_3_topic_logs)+")", 'Total\n(' + str(number_of_1_topic_logs+number_of_2_topic_logs+number_of_3_topic_logs)+")"])
    # plt.xlabel("Teams")
    bottom, top = plt.ylim()
    plt.ylim(bottom, 1.2*top)
    plt.ylabel("Mean time (seconds)")
    plt.legend(ncol=2, mode="expand") # ["Bloom filter", "Brute force","Bloom filter (non existing logs)", "Brute
    # force (non existing logs)"],
    plt.title('Performance Comparison based on number of topics (offline search)')

    end = time.time()
    print("Total execution time of Log retrieval Position based comparison Offline is: ",time.strftime("%H:%M:%S", time.gmtime(end - start)))
    plt.show()


## The following test is not used in the thesis  ##
# This function tests the Offline log retrieval time based on the log position
def Log_Retrieval_TimeComparison_PositionBased_OfflineTest_plot(Number_of_1_2_3_topic_logs: tuple, Scrap_database: tuple):
    # The arguments that are required are the number of 1 log topics, number of 2 log topics, number of 3 log topics,
    # this is given in the form of a tuple with 3 positions where 1st position is the number of 1 log topics,
    # 2nd position is the number of 2 log topics and 3rd position is the number of 3 log topics.
    # The second argument is the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database
    # The database is the stored locally in the computer memory and it is retrieved from the database when
    # the Scrap_database variable is given
    start = time.time()

    number_of_1_topic_logs, number_of_2_topic_logs, number_of_3_topic_logs = Number_of_1_2_3_topic_logs
    Starting_block, Ending_block = Scrap_database

    path = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_Logs.close()


    ##  ##  Data selection  ##  ##

    # start_logs, middle_logs, end_logs are the lists that in the end contains the logs to be tested.
    # In the end, each list must have the specified number of 1 topic, 2 topic and 3 topic logs
    start_logs = []
    middle_logs = []
    end_logs = []

    num_of_1_topic_logs_start = 0
    num_of_2_topic_logs_start = 0
    num_of_3_topic_logs_start = 0

    num_of_1_topic_logs_middle = 0
    num_of_2_topic_logs_middle = 0
    num_of_3_topic_logs_middle = 0

    num_of_1_topic_logs_end = 0
    num_of_2_topic_logs_end = 0
    num_of_3_topic_logs_end = 0

    random.seed(0)

    start_flag = 1
    middle_flag = 1
    end_flag = 1

    number_of_blocks = Ending_block - Starting_block

    # The while loop is terminated only when all three flags are set to 0
    while start_flag + middle_flag + end_flag > 0:
        # random_block_number: a random number between the number 0 and the number of blocks in the database
        random_block_number = random.randint(0, number_of_blocks - 1)

        # if this number is in the first 10% blocks of the database, a random log from this block is selected.
        # Depending from the number of topics of this log, it is either appended into the start_logs, or ignored
        if random_block_number < 0.1 * number_of_blocks:

            # The Entries list is a list containing all the logs of the specific block
            Entries = All_logs[random_block_number].split(",")

            # entry is the random entry that is selected.
            # entry is initially a string but becomes a list representing the log in the following manner:
            # entry = [address, topic1, topic2, topic3, topic4, transactionHash]
            entry = random.choice(Entries) # entry: string
            entry = entry.split(" ") # entry: list
            entry.append(str(random_block_number))

            # num_of_topics is the number of topics
            num_of_topics = len(entry[1:-2])

            # if the start_logs list requires a log with the number of topics of the entry, then the entry is appended
            # in the start_logs list, otherwise it is ignored
            # To keep track of the number of 1, 2 nad 3 topic logs that the start_log list requires, the
            # num_of_1_topic_logs_start, num_of_2_topic_logs_start, num_of_3_topic_logs_start variables are used
            # as counters.
            if (num_of_topics == 1) & (num_of_1_topic_logs_start < number_of_1_topic_logs):
                start_logs.append(entry)
                num_of_1_topic_logs_start = num_of_1_topic_logs_start + 1
            elif (num_of_topics == 2) & (num_of_2_topic_logs_start < number_of_2_topic_logs):
                start_logs.append(entry)
                num_of_2_topic_logs_start = num_of_2_topic_logs_start + 1
            elif (num_of_topics == 3) & (num_of_3_topic_logs_start < number_of_3_topic_logs):
                start_logs.append(entry)
                num_of_3_topic_logs_start = num_of_3_topic_logs_start + 1

            # This flag is set to 0 when all the logs from the start of the database are selected for testing
            if (num_of_1_topic_logs_start == number_of_1_topic_logs) & (num_of_2_topic_logs_start == number_of_2_topic_logs) & (
                    num_of_3_topic_logs_start == number_of_3_topic_logs):
                start_flag = 0


        # if this number is int he 45-55% blocks of the database, a random log from this block is selected.
        # Depending from the number of topics of this log, it is either appended into the middle_logs, or ignored
        elif (random_block_number > 0.45 * number_of_blocks) & (random_block_number < 0.55 * number_of_blocks):
            # The logic is the same as the start_logs

            Entries = All_logs[random_block_number].split(",")

            entry = random.choice(Entries)
            entry = entry.split(" ")
            entry.append(str(random_block_number))

            num_of_topics = len(entry[1:-2])

            if (num_of_topics == 1) & (num_of_1_topic_logs_middle < number_of_1_topic_logs):
                middle_logs.append(entry)
                num_of_1_topic_logs_middle = num_of_1_topic_logs_middle + 1
            elif (num_of_topics == 2) & (num_of_2_topic_logs_middle < number_of_2_topic_logs):
                middle_logs.append(entry)
                num_of_2_topic_logs_middle = num_of_2_topic_logs_middle + 1
            elif (num_of_topics == 3) & (num_of_3_topic_logs_middle < number_of_3_topic_logs):
                middle_logs.append(entry)
                num_of_3_topic_logs_middle = num_of_3_topic_logs_middle + 1

            # This flag is set to 0 when all the logs from the middle of the database are selected for testing
            if (num_of_1_topic_logs_middle == number_of_1_topic_logs) & (
                    num_of_2_topic_logs_middle == number_of_2_topic_logs) & (
                    num_of_3_topic_logs_middle == number_of_3_topic_logs):
                middle_flag = 0

        # if this number is in the last 10% blocks of the database, a random log from this block is selected.
        # Depending from the number of topics of this log, it is either appended into the end_logs, or ignored
        elif random_block_number > 0.9 * number_of_blocks:
            # The logic is the same as the start_logs
            Entries = All_logs[random_block_number].split(",")

            entry = random.choice(Entries)
            entry = entry.split(" ")
            entry.append(str(random_block_number))

            num_of_topics = len(entry[1:-2])

            if (num_of_topics == 1) & (num_of_1_topic_logs_end < number_of_1_topic_logs):
                end_logs.append(entry)
                num_of_1_topic_logs_end = num_of_1_topic_logs_end + 1
            elif (num_of_topics == 2) & (num_of_2_topic_logs_end < number_of_2_topic_logs):
                end_logs.append(entry)
                num_of_2_topic_logs_end = num_of_2_topic_logs_end + 1
            elif (num_of_topics == 3) & (num_of_3_topic_logs_end < number_of_3_topic_logs):
                end_logs.append(entry)
                num_of_3_topic_logs_end = num_of_3_topic_logs_end + 1

            # This flag is set to 0 when all the logs from the middle of the database are selected for testing
            if (num_of_1_topic_logs_end == number_of_1_topic_logs) & (
                    num_of_2_topic_logs_end == number_of_2_topic_logs) & (
                    num_of_3_topic_logs_end == number_of_3_topic_logs):
                end_flag = 0

    ##  ##  Retrieval time recording  ##  ##

    # In the following file, the time required for each individual retrieval is stored. The file can be read as csv.
    # The file contains the block of the log followed by the bloom filter retrieval time and the brute force retrieval
    # time. Each value is separated by comma and each log is separated by newline(\n).
    # For example: 13,0.4255,0.5232
    #              22,0.3224,0.4011
    #              18,0.5622,0.5239
    individual_time_file = open(global_path + "Individual retrieval time dataset/Time for each query(PB)(offline) ("+ str(number_of_1_topic_logs) + ", "+ str(number_of_2_topic_logs) + ", " + str(number_of_3_topic_logs) + ") blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    # The following variables are used for time recording, each variable stores the time that is indicated by it's name.
    # For example, start_bloom_time: stores the time required for the retrieval of all the logs at the start of the
    # blockchain using the bloom filter method. These variables refer to the total time required.
    # These variables later refer to the mean time.
    start_bloom_time, middle_bloom_time, end_bloom_time, total_bloom_time = 0, 0, 0, 0
    start_brute_time, middle_brute_time, end_brute_time, total_brute_time = 0, 0, 0, 0


    # The bloom filter retrieval time for all the logs in the start_logs list
    for log in start_logs:
        individual_time_start = time.time()
        block, position, bloom_time, blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()

        start_bloom_time = start_bloom_time + bloom_time
        start_brute_time = start_brute_time + brute_time
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(bloom_time) + "," + str(brute_time) + "\n")


    # The bloom filter retrieval time for all the logs in the middle_logs list
    for log in middle_logs:
        individual_time_start = time.time()
        block, position, bloom_time, blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()


        middle_bloom_time = middle_bloom_time + bloom_time
        middle_brute_time = middle_brute_time + brute_time
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(bloom_time) + "," + str(brute_time) + "\n")


    # The bloom filter retrieval time for all the logs in the end_logs list
    for log in end_logs:
        individual_time_start = time.time()
        block, position, bloom_time, blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()


        end_bloom_time = end_bloom_time + bloom_time
        end_brute_time = end_brute_time + brute_time
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(bloom_time) + "," + str(brute_time) + "\n")

    individual_time_file.close()

    # log_number: the number of logs in the start_logs list, which is the same as the number
    # of logs in the middle_logs and end_logs lists
    log_number = len(start_logs)

    # total_bloom_time: the time for bloom filter retrieval of all the logs
    # total_brute_time: the time for brute force retrieval of all the logs
    total_bloom_time = start_bloom_time + middle_bloom_time + end_bloom_time
    total_brute_time = start_brute_time + middle_brute_time + end_brute_time

    # At this point the time refers to the mean time and not to the total time
    start_bloom_time, middle_bloom_time, end_bloom_time, total_bloom_time = start_bloom_time/log_number, middle_bloom_time/log_number, end_bloom_time/log_number, total_bloom_time/(log_number*3)
    start_brute_time, middle_brute_time, end_brute_time, total_brute_time = start_brute_time/log_number, middle_brute_time/log_number, end_brute_time/log_number, total_brute_time/(log_number*3)

    # ##  ##  Plot  ##  ##
    x = np.arange(4)
    bloom_measurments = [start_bloom_time, middle_bloom_time, end_bloom_time, total_bloom_time]
    brute_measurments = [start_brute_time, middle_brute_time, end_brute_time, total_brute_time]
    width = 0.35

    # plot data in grouped manner of bar type
    plt.bar(x - width/2, bloom_measurments, width, color='lightseagreen')
    plt.bar(x + width/2, brute_measurments, width, color='navy')

    plt.xticks(x, ['logs at the start','logs at the middle','logs at the end','Total logs'])

    plt.ylabel("Mean time (seconds)")
    bottom, top = plt.ylim()
    plt.ylim(bottom, 1.2*top)
    text = '1 topic logs: '+str(number_of_1_topic_logs)+'\n2 topic logs: '+str(number_of_2_topic_logs) + '\n3 topic logs: '+str(number_of_3_topic_logs)
    plt.text(-width, 1.2 * max([max(brute_measurments),max(bloom_measurments)]), text, ha='left', va='top', fontsize=10)
    plt.legend(["Bloom filter", "Brute force"],loc='upper right')
    plt.title('Offline Performance Comparison based on log position ' + str((Starting_block,Ending_block)))

    for i, v in enumerate(bloom_measurments):
        plt.text( i - 0.1*width, v + 0.02*top, "%.3f" % v, ha="right", color='black')

    for i, v in enumerate(brute_measurments):
        plt.text( i + 0.1*width, v + 0.02*top, "%.3f" % v, ha="left", color='black')


    end = time.time()
    print("Total execution time of Log retrieval Position based comparison Online is: ",time.strftime("%H:%M:%S", time.gmtime(end - start)))
    print()
    plt.show()



###   ###   ###   Online features   ###   ###   ###
# This function is used to search a log (online) utilizing the bloom filters.
def Log_Retrieval_bloom_filter_Online(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none"):
    ## THIS FUNCTION NEEDS A LOCAL DATASET ##
    # This function needs the address and topics of the log to query and optionally the transactionHash.
    # It is also necessary to specify the blocks to query with the Starting_block and Ending_block parameters.
    # The return of the function are two lists. The first one for the blocks in which the log was found and the second
    # one for the corresponding log indexes in each block.
    # If the log is not found, the function returns two empty lists

    time1 = time.time()

    # web3: connection to the Ethereum blockchain
    web3 = Web3(Web3.HTTPProvider(API_key))

    # blocks_of_found_element: the block in which the element is found
    # positions_of_found_element_in_block: the position of the found log in the block
    blocks_of_found_element = []
    positions_of_found_element_in_block = []

    # Every block is being checked in the given block range
    for block_number in range(Starting_block,Ending_block):

        error_times = 0
        while True:
            try:
                block = web3.eth.get_block(block_number)
                break
            except:
                print("get_block error in block:",block_number)
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                error_times = error_times + 1
            if error_times == 5:
                infura_key = input("It is possible that this Infura key is not working anymore. Please enter new Infura key to continue: ")
                web3 = Web3(Web3.HTTPProvider(infura_key))


        # bloom_filter: the bloom filter of the specified block
        bloom_filter = BloomFilter(int(block["logsBloom"].hex(), 0))

        # Checkng if the topics are in the bloom filter
        topic_flag = 1
        for topic in topics:
            if bytes.fromhex(topic[2:]) not in bloom_filter:
                topic_flag = 0
                break

        # Only if the topics and address are in the bloom filter, the whole block is checked for the log
        if topic_flag:
            if bytes.fromhex(address[2:]) in bloom_filter:

                error_times = 0
                while True:
                    try:
                        event_filter = web3.eth.filter({
                            "fromBlock": block_number,
                            "toBlock": block_number,
                        })
                        break
                    except:
                        print("event_filter error in block:", block_number)
                        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                        error_times = error_times + 1
                    if error_times == 5:
                        infura_key = input(
                            "It is possible that this Infura key is not working anymore. Please enter new Infura key to continue: ")
                        web3 = Web3(Web3.HTTPProvider(infura_key))

                error_times = 0
                while True:
                    try:
                        Entries = event_filter.get_all_entries()
                        break
                    except:
                        print("get_all_entries error in block:", block_number)
                        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                        error_times = error_times + 1
                    if error_times == 5:
                        infura_key = input(
                            "It is possible that this Infura key is not working anymore. Please enter new Infura key to continue: ")
                        web3 = Web3(Web3.HTTPProvider(infura_key))

                # Each log of the block is compared with the queried log
                for count, log in enumerate(Entries):
                    if address == log["address"]:  ##  the number of topics is 0,1,2,3 or 4
                        log_topics = [topic.hex() for topic in log["topics"]]
                        if topics == log_topics:
                            if transactionHash == "none":
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count)
                                # break
                            elif transactionHash == log["transactionHash"].hex():
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count)
                                # break
            # if the transactionHash argument is given and a log is found, the search stops
            if (transactionHash != "none") & (blocks_of_found_element != []): break
    time2 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time2- time1


# This function is used to search a log (online) without utilizing the bloom filters.
def Log_Retrieval_brute_force_Online(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none"):
    ## THIS FUNCTION NEEDS A LOCAL DATASET ##

    time1 = time.time()

    # web3: connection to the Ethereum blockchain
    web3 = Web3(Web3.HTTPProvider(API_key))

    # blocks_of_found_element: the block in which the element is found
    # positions_of_found_element_in_block: the position of the found log in the block
    blocks_of_found_element = []
    positions_of_found_element_in_block = []

    event_filter_error_counter = 0
    get_all_entries_error_counter = 0

    # Every block is being checked in the given block range
    for block_number in range(Starting_block, Ending_block):

        error_times = 0
        while True:
            try:
                event_filter = web3.eth.filter({
                    "fromBlock": block_number,
                    "toBlock": block_number,
                })
                break
            except:
                print("event_filter error in block:", block_number)
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                error_times = error_times + 1
            if error_times == 5:
                infura_key = input("It is possible that this Infura key is not working anymore. Please enter new Infura key to continue: ")
                web3 = Web3(Web3.HTTPProvider(infura_key))

        error_times = 0
        while True:
            try:
                Entries = event_filter.get_all_entries()
                break
            except:
                print("get_all_entries error in block:", block_number)
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                error_times = error_times + 1
            if error_times == 5:
                infura_key = input("It is possible that this Infura key is not working anymore. Please enter new Infura key to continue: ")
                web3 = Web3(Web3.HTTPProvider(infura_key))

        # Every log of every block is checked for the given block range
        for count, log in enumerate(Entries):
            if address == log["address"]:  ##  the number of topics is 0,1,2,3 or 4
                log_topics = [topic.hex() for topic in log["topics"]]
                if topics == log_topics:
                    if transactionHash == "none":
                        blocks_of_found_element.append(block_number)
                        positions_of_found_element_in_block.append(count)
                        # break
                    elif transactionHash == log["transactionHash"].hex():
                        blocks_of_found_element.append(block_number)
                        positions_of_found_element_in_block.append(count)
                        # break
        # if the transactionHash argument is given and a log is found, the search stops
        if (transactionHash != "none") & (blocks_of_found_element != []): break
    time2 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time2 - time1


# This function tests the Online log retrieval time based on the log topic number
def Log_Retrieval_TimeComparison_TopicBased_OnlineTest_plot(Number_of_1_2_3_topic_logs: tuple, Scrap_database: tuple, Non_existing_log_database: tuple):
    ## THIS FUNCTION NEEDS TWO LOCAL DATASETS ##

    # The arguments that are required are the number of 1 log topics, number of 2 log topics, number of 3 log topics,
    # this is given in the form of a tuple with 3 positions where 1st position is the number of 1 log topics,
    # 2nd position is the number of 2 log topics and 3rd position is the number of 3 log topics.
    #
    # The second argument is the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database
    #
    # The third argument is the non existing log database. This is the database from which the non existing logs are
    # selected to be queried in the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database
    #
    # The dataset are stored locally in the computer memory and are retrieved from the database when
    # the Scrap_database variable is given

    start = time.time()
    number_of_1_topic_logs, number_of_2_topic_logs, number_of_3_topic_logs = Number_of_1_2_3_topic_logs
    Starting_block, Ending_block = Scrap_database
    non_existing_starting_block, non_existing_ending_block = Non_existing_log_database

    path = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()

    File_Logs.close()

    ##  ##  Data Selection  ##  ##
    ##  Existing log selection  ##

    # one_topic_logs,two_topic_logs, three_topic_logs are the 1,2,3 topic logs that are randomly selected to be queried
    one_topic_logs = []
    two_topic_logs = []
    three_topic_logs = []

    random.seed(0)

    flag = 1
    # The while loop is terminated only when the flag is set to 0
    while flag == 1:
        # random_block_number: a random number between the number 0 and the number of blocks in the database
        random_block_number = random.randint(0,Ending_block - Starting_block - 1)

        # The Entries list is a list containing all the logs of the specific block
        Entries = All_logs[random_block_number].split(",")

        # entry is the random entry that is selected.
        # entry is initially a string but becomes a list representing the log in the following manner:
        # entry = [address, topic1, topic2, topic3, topic4, transactionHash]
        entry = random.choice(Entries) # entry: string
        entry = entry.split(" ") # entry: list
        entry.append(str(random_block_number))

        # num_of_topics is the number of topics
        num_of_topics = len(entry[1:-2])

        # if the number of topics is 1 and the one_topic_logs list is not full, then the entry is appended in the
        # one_topic_logs.
        # if the number of topics is 2 and the two_topic_logs list is not full, then the entry is appended in the
        # two_topic_logs.
        # if the number of topics is 3 and the three_topic_logs list is not full, then the entry is appended in the
        # three_topic_logs.
        if (num_of_topics == 1) & (len(one_topic_logs) < number_of_1_topic_logs):
            one_topic_logs.append(entry)
        elif (num_of_topics == 2) & (len(two_topic_logs) < number_of_2_topic_logs):
            two_topic_logs.append(entry)
        elif (num_of_topics == 3) & (len(three_topic_logs) < number_of_3_topic_logs):
            three_topic_logs.append(entry)

        # The while loop stops only when the one_topic_logs, two_topic_logs, three_topic_logs are full
        if (len(one_topic_logs) == number_of_1_topic_logs) & (len(two_topic_logs) == number_of_2_topic_logs) & (len(three_topic_logs) == number_of_3_topic_logs):
            flag = 0

    ##  Non existing log selection  ##

    File_non_existing_Logs = open(path + "Logs for blocks " + str(non_existing_starting_block) + " to " + str(non_existing_ending_block), "r")
    All_non_existing_logs = File_non_existing_Logs.readlines()
    File_non_existing_Logs.close()

    # non_exist_one_topic_logs,non_exist_two_topic_logs, non_exist_three_topic_logs are the non existing 1,2,3 topic
    # logs that are randomly selected to be queried
    non_exist_one_topic_logs = []
    non_exist_two_topic_logs = []
    non_exist_three_topic_logs = []

    num_of_non_exist_1_topic_logs = 0
    num_of_non_exist_2_topic_logs = 0
    num_of_non_exist_3_topic_logs = 0

    flag = 1
    # The while loop is terminated only when the flag is set to 0
    while flag == 1:
        # random_block_number: a random number between the number 0 and the number of blocks in the database
        random_block_number = random.randint(0, non_existing_ending_block - non_existing_starting_block - 1)

        # The Entries list is a list containing all the logs of the specific block
        Entries = All_non_existing_logs[random_block_number].split(",")

        # entry is the random entry that is selected.
        # entry is initially a string but becomes a list representing the log in the following manner:
        # entry = [address, topic1, topic2, topic3, topic4, transactionHash]
        entry = random.choice(Entries) # entry: string
        entry = entry.split(" ") # entry: list
        entry.append("NEB")


        # num_of_topics is the number of topics
        num_of_topics = len(entry[1:-2])

        # if the number of topics is 1 and the non_exist_one_topic_logs list is not full, then the entry is
        # appended in the one_topic_logs.
        # if the number of topics is 2 and the non_exist_two_topic_logs list is not full, then the entry is
        # appended in the two_topic_logs.
        # if the number of topics is 3 and the non_exist_three_topic_logs list is not full, then the entry is
        # appended in the three_topic_logs.
        if (num_of_topics == 1) & (len(non_exist_one_topic_logs) < number_of_1_topic_logs):
            non_exist_one_topic_logs.append(entry)

        elif (num_of_topics == 2) & (len(non_exist_two_topic_logs) < number_of_2_topic_logs):
            non_exist_two_topic_logs.append(entry)

        elif (num_of_topics == 3) & (len(non_exist_three_topic_logs) < number_of_3_topic_logs):
            non_exist_three_topic_logs.append(entry)

        # The while loop stops only when the non_exist_one_topic_logs, non_exist_two_topic_logs,
        # non_exist_three_topic_logs are full
        if (len(non_exist_one_topic_logs) == number_of_1_topic_logs) & (len(non_exist_two_topic_logs) == number_of_2_topic_logs) & (
                len(non_exist_three_topic_logs) == number_of_3_topic_logs):
            flag = 0


    ##  ##  Retrieval time recording  ##  ##

    # In the following file, the time required for each individual retrieval is stored. The file can be read as csv.
    # The file contains the block number of the log followed by the bloom filter retrieval time and the brute force
    # retrieval time. Each value is separated by comma and each log is separated by newline(\n). For the non existing
    # logs, in the block number there is "NEB" that stands for Non Existing Block
    # For example: 13,0.4255,0.5232
    #              22,0.3224,0.4011
    #              18,0.5622,0.5239
    #              NEB,0.8574,0.7889
    individual_time_file = open(global_path + "Individual retrieval time dataset/Time for each query(TB)(Online) ("+ str(number_of_1_topic_logs) + ", " + str(number_of_2_topic_logs) + ", " + str(number_of_3_topic_logs) + ") blocks " + str(Starting_block) + " to " + str(Ending_block), "w")


    ##  existing logs bloom filter retrieval time  ##

    # The following variables are used for time recording, each variable stores the time that is indicated by it's name.
    # For example, one_topic_bloom_time: stores the time required for the retrieval of all one topic logs using the
    # bloom filter method. These variables refer to the total time required.
    # These variables are later used to refer to the mean time.
    one_topic_bloom_time, two_topic_bloom_time, three_topic_bloom_time, total_topic_bloom_time = 0, 0, 0, 0
    one_topic_brute_time, two_topic_brute_time, three_topic_brute_time, total_topic_brute_time = 0, 0, 0, 0
    non_exist_one_topic_bloom_time, non_exist_two_topic_bloom_time, non_exist_three_topic_bloom_time, non_exist_total_topic_bloom_time = 0, 0, 0, 0
    non_exist_one_topic_brute_time, non_exist_two_topic_brute_time, non_exist_three_topic_brute_time, non_exist_total_topic_brute_time = 0, 0, 0, 0

    # One topic log retrieval time for bloom filter method and brute force method for existing logs
    for log in one_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time = Log_Retrieval_bloom_filter_Online(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])
        if block == []: print("Not found")
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Online(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])
        individual_time_end = time.time()
        if block == []: print("Not found")


        one_topic_bloom_time = one_topic_bloom_time + individual_time_med - individual_time_start
        one_topic_brute_time = one_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")

    # Two topic log retrieval time for bloom filter method and brute force method for existing logs
    for log in two_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time = Log_Retrieval_bloom_filter_Online(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])
        if block == []: print("Not found")
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Online(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])
        individual_time_end = time.time()
        if block == []: print("Not found")


        two_topic_bloom_time = two_topic_bloom_time + individual_time_med - individual_time_start
        two_topic_brute_time = two_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")

    # Three topic log retrieval time for bloom filter method and brute force method for existing logs
    for log in three_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time = Log_Retrieval_bloom_filter_Online(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])
        if block == []: print("Not found")
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Online(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])
        individual_time_end = time.time()
        if block == []: print("Not found")


        three_topic_bloom_time = three_topic_bloom_time + individual_time_med - individual_time_start
        three_topic_brute_time = three_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")

    ##  Non existing logs bloom filter retrieval time  ##
    # One topic log retrieval time for bloom filter method and brute force method for non existing logs
    for log in non_exist_one_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time = Log_Retrieval_bloom_filter_Online(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Online(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()

        non_exist_one_topic_bloom_time = non_exist_one_topic_bloom_time + individual_time_med - individual_time_start
        non_exist_one_topic_brute_time = non_exist_one_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(log[-1] + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")
        if block != []: print("Found in ","one_topic_logs", "bloom")

    # Two topic log retrieval time for bloom filter method and brute force method for non existing logs
    for log in non_exist_two_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time = Log_Retrieval_bloom_filter_Online(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Online(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()

        non_exist_two_topic_bloom_time = non_exist_two_topic_bloom_time + individual_time_med - individual_time_start
        non_exist_two_topic_brute_time = non_exist_two_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(log[-1] + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")
        if block != []: print("Found in ", "two_topic_logs","bloom")

    # Three topic log retrieval time for bloom filter method and brute force method for non existing logs
    for log in non_exist_three_topic_logs:
        individual_time_start = time.time()
        block, position, bloom_time = Log_Retrieval_bloom_filter_Online(log[0], log[1:-2], Starting_block, Ending_block,
                                                             transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Online(log[0], log[1:-2], Starting_block, Ending_block,
                                                            transactionHash=log[-2])
        individual_time_end = time.time()

        non_exist_three_topic_bloom_time = non_exist_three_topic_bloom_time + individual_time_med - individual_time_start
        non_exist_three_topic_brute_time = non_exist_three_topic_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(log[-1] + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")
        if block != []: print("Found in ", "three_topic_logs","bloom")


    individual_time_file.close()

    # the total retrieval time is calculated for bloom filter and brute force, for existing and non existing logs
    total_topic_bloom_time = one_topic_bloom_time + two_topic_bloom_time + three_topic_bloom_time
    non_exist_total_topic_bloom_time = non_exist_one_topic_bloom_time + non_exist_two_topic_bloom_time + non_exist_three_topic_bloom_time
    total_topic_brute_time = one_topic_brute_time + two_topic_brute_time + three_topic_brute_time
    non_exist_total_topic_brute_time = non_exist_one_topic_brute_time + non_exist_two_topic_brute_time + non_exist_three_topic_brute_time

    # At this point the time refers to the mean time and not to the total time
    one_topic_bloom_time = one_topic_bloom_time/number_of_1_topic_logs
    two_topic_bloom_time = two_topic_bloom_time/number_of_2_topic_logs
    three_topic_bloom_time = three_topic_bloom_time/number_of_3_topic_logs
    total_topic_bloom_time = total_topic_bloom_time/(number_of_1_topic_logs+number_of_2_topic_logs+ number_of_3_topic_logs)

    non_exist_one_topic_bloom_time = non_exist_one_topic_bloom_time/number_of_1_topic_logs
    non_exist_two_topic_bloom_time = non_exist_two_topic_bloom_time/number_of_2_topic_logs
    non_exist_three_topic_bloom_time = non_exist_three_topic_bloom_time/number_of_3_topic_logs
    non_exist_total_topic_bloom_time = non_exist_total_topic_bloom_time/(number_of_1_topic_logs+number_of_2_topic_logs+ number_of_3_topic_logs)

    one_topic_brute_time = one_topic_brute_time/number_of_1_topic_logs
    two_topic_brute_time = two_topic_brute_time/number_of_2_topic_logs
    three_topic_brute_time = three_topic_brute_time/number_of_3_topic_logs
    total_topic_brute_time = total_topic_brute_time/(number_of_1_topic_logs+number_of_2_topic_logs+ number_of_3_topic_logs)

    non_exist_one_topic_brute_time = non_exist_one_topic_brute_time/number_of_1_topic_logs
    non_exist_two_topic_brute_time = non_exist_two_topic_brute_time/number_of_2_topic_logs
    non_exist_three_topic_brute_time = non_exist_three_topic_brute_time/number_of_3_topic_logs
    non_exist_total_topic_brute_time = non_exist_total_topic_brute_time/(number_of_1_topic_logs + number_of_2_topic_logs + number_of_3_topic_logs)

    ##  ##  Plot  ##  ##
    x = np.arange(4)
    bloom_measurments = [one_topic_bloom_time, two_topic_bloom_time, three_topic_bloom_time, total_topic_bloom_time]
    brute_measurments = [one_topic_brute_time, two_topic_brute_time, three_topic_brute_time, total_topic_brute_time]
    non_exist_bloom_measurments = [non_exist_one_topic_bloom_time, non_exist_two_topic_bloom_time, non_exist_three_topic_bloom_time, non_exist_total_topic_bloom_time]
    non_exist_brute_measurments = [non_exist_one_topic_brute_time, non_exist_two_topic_brute_time, non_exist_three_topic_brute_time, non_exist_total_topic_brute_time]
    width = 0.10

    # plot data in grouped manner of bar type
    plt.bar(x - 0.15, bloom_measurments, width, color='lightseagreen', label="Bloom filter")
    plt.bar(x - 0.05, brute_measurments, width, color='navy', label="Brute force")
    plt.bar(x + 0.05, non_exist_bloom_measurments, width, color='indianred', label="Bloom filter (non existing logs)")
    plt.bar(x + 0.15, non_exist_brute_measurments, width, color='darkred', label="Brute force (non existing logs)")

    plt.xticks(x, ['One topic logs\n(' + str(number_of_1_topic_logs) + ")", 'Two topic logs\n(' + str(number_of_2_topic_logs)+")", 'Three topic logs\n(' + str(number_of_3_topic_logs)+")", 'Total\n(' + str(number_of_1_topic_logs+number_of_2_topic_logs+number_of_3_topic_logs)+")"])
    # plt.xlabel("Teams")
    bottom, top = plt.ylim()
    plt.ylim(bottom, 1.2*top)
    plt.ylabel("Mean time (seconds)")
    plt.legend(ncol=2, mode="expand") # ["Bloom filter", "Brute force","Bloom filter (non existing logs)", "Brute
    # force (non existing logs)"],
    plt.title('Performance Comparison based on number of topics (online search)')

    end = time.time()
    print("Total execution time of Log retrieval Position based comparison Online is: ",time.strftime("%H:%M:%S", time.gmtime(end - start)))
    plt.show()

## The following test is not used in the thesis  ##
# This function tests the Online log retrieval time based on the log position
def Log_Retrieval_TimeComparison_PositionBased_OnlineTest_plot(Number_of_1_2_3_topic_logs: tuple, Scrap_database: tuple):
    ## THIS FUNCTION NEEDS A LOCAL DATASET ##
    start = time.time()

    # The arguments that are required are the number of 1 log topics, number of 2 log topics, number of 3 log topics,
    # this is given in the form of a tuple with 3 positions where 1st position is the number of 1 log topics,
    # 2nd position is the number of 2 log topics and 3rd position is the number of 3 log topics.
    # The second argument is the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database
    # The database is the stored locally in the computer memory and it is retrieved from the database when
    # the Scrap_database variable is given
    number_of_1_topic_logs, number_of_2_topic_logs, number_of_3_topic_logs = Number_of_1_2_3_topic_logs
    Starting_block, Ending_block = Scrap_database

    path = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_Logs.close()


    ##  ##  Data selection  ##  ##

    # start_logs, middle_logs, end_logs are the lists that in the end contains the logs to be tested.
    # In the end, each list must have the specified number of 1 topic, 2 topic and 3 topic logs
    start_logs = []
    middle_logs = []
    end_logs = []

    num_of_1_topic_logs_start = 0
    num_of_2_topic_logs_start = 0
    num_of_3_topic_logs_start = 0

    num_of_1_topic_logs_middle = 0
    num_of_2_topic_logs_middle = 0
    num_of_3_topic_logs_middle = 0

    num_of_1_topic_logs_end = 0
    num_of_2_topic_logs_end = 0
    num_of_3_topic_logs_end = 0

    random.seed(0)

    start_flag = 1
    middle_flag = 1
    end_flag = 1

    number_of_blocks = Ending_block - Starting_block

    # The while loop is terminated only when all three flags are set to 0
    while start_flag + middle_flag + end_flag > 0:
        # random_block_number: a random number between the number 0 and the number of blocks in the database
        random_block_number = random.randint(0, number_of_blocks - 1)

        # if this number is in the first 10% blocks of the database, a random log from this block is selected.
        # Depending from the number of topics of this log, it is either appended into the start_logs, or ignored
        if random_block_number < 0.1 * number_of_blocks:

            # The Entries list is a list containing all the logs of the specific block
            Entries = All_logs[random_block_number].split(",")

            # entry is the random entry that is selected.
            # entry is initially a string but becomes a list representing the log in the following manner:
            # entry = [address, topic1, topic2, topic3, topic4, transactionHash]
            entry = random.choice(Entries) # entry: string
            entry = entry.split(" ") # entry: list
            entry.append(str(random_block_number))

            # num_of_topics is the number of topics
            num_of_topics = len(entry[1:-2])

            # if the start_logs list requires a log with the number of topics of the entry, then the entry is appended
            # in the start_logs list, otherwise it is ignored
            # To keep track of the number of 1, 2 nad 3 topic logs that the start_log list requires, the
            # num_of_1_topic_logs_start, num_of_2_topic_logs_start, num_of_3_topic_logs_start variables are used
            # as counters.
            if (num_of_topics == 1) & (num_of_1_topic_logs_start < number_of_1_topic_logs):
                start_logs.append(entry)
                num_of_1_topic_logs_start = num_of_1_topic_logs_start + 1
            elif (num_of_topics == 2) & (num_of_2_topic_logs_start < number_of_2_topic_logs):
                start_logs.append(entry)
                num_of_2_topic_logs_start = num_of_2_topic_logs_start + 1
            elif (num_of_topics == 3) & (num_of_3_topic_logs_start < number_of_3_topic_logs):
                start_logs.append(entry)
                num_of_3_topic_logs_start = num_of_3_topic_logs_start + 1

            # This flag is set to 0 when all the logs from the start of the database are selected for testing
            if (num_of_1_topic_logs_start == number_of_1_topic_logs) & (num_of_2_topic_logs_start == number_of_2_topic_logs) & (
                    num_of_3_topic_logs_start == number_of_3_topic_logs):
                start_flag = 0


        # if this number is int he 45-55% blocks of the database, a random log from this block is selected.
        # Depending from the number of topics of this log, it is either appended into the middle_logs, or ignored
        elif (random_block_number > 0.45 * number_of_blocks) & (random_block_number < 0.55 * number_of_blocks):
            # The logic is the same as the start_logs

            Entries = All_logs[random_block_number].split(",")

            entry = random.choice(Entries)
            entry = entry.split(" ")
            entry.append(str(random_block_number))

            num_of_topics = len(entry[1:-2])

            if (num_of_topics == 1) & (num_of_1_topic_logs_middle < number_of_1_topic_logs):
                middle_logs.append(entry)
                num_of_1_topic_logs_middle = num_of_1_topic_logs_middle + 1
            elif (num_of_topics == 2) & (num_of_2_topic_logs_middle < number_of_2_topic_logs):
                middle_logs.append(entry)
                num_of_2_topic_logs_middle = num_of_2_topic_logs_middle + 1
            elif (num_of_topics == 3) & (num_of_3_topic_logs_middle < number_of_3_topic_logs):
                middle_logs.append(entry)
                num_of_3_topic_logs_middle = num_of_3_topic_logs_middle + 1

            # This flag is set to 0 when all the logs from the middle of the database are selected for testing
            if (num_of_1_topic_logs_middle == number_of_1_topic_logs) & (
                    num_of_2_topic_logs_middle == number_of_2_topic_logs) & (
                    num_of_3_topic_logs_middle == number_of_3_topic_logs):
                middle_flag = 0

        # if this number is in the last 10% blocks of the database, a random log from this block is selected.
        # Depending from the number of topics of this log, it is either appended into the end_logs, or ignored
        elif random_block_number > 0.9 * number_of_blocks:
            # The logic is the same as the start_logs
            Entries = All_logs[random_block_number].split(",")

            entry = random.choice(Entries)
            entry = entry.split(" ")
            entry.append(str(random_block_number))

            num_of_topics = len(entry[1:-2])

            if (num_of_topics == 1) & (num_of_1_topic_logs_end < number_of_1_topic_logs):
                end_logs.append(entry)
                num_of_1_topic_logs_end = num_of_1_topic_logs_end + 1
            elif (num_of_topics == 2) & (num_of_2_topic_logs_end < number_of_2_topic_logs):
                end_logs.append(entry)
                num_of_2_topic_logs_end = num_of_2_topic_logs_end + 1
            elif (num_of_topics == 3) & (num_of_3_topic_logs_end < number_of_3_topic_logs):
                end_logs.append(entry)
                num_of_3_topic_logs_end = num_of_3_topic_logs_end + 1

            # This flag is set to 0 when all the logs from the middle of the database are selected for testing
            if (num_of_1_topic_logs_end == number_of_1_topic_logs) & (
                    num_of_2_topic_logs_end == number_of_2_topic_logs) & (
                    num_of_3_topic_logs_end == number_of_3_topic_logs):
                end_flag = 0

    ##  ##  Retrieval time recording  ##  ##

    # In the following file, the time required for each individual retrieval is stored. The file can be read as csv.
    # The file contains the block of the log followed by the bloom filter retrieval time and the brute force retrieval
    # time. Each value is separated by comma and each log is separated by newline(\n).
    # For example: 13,0.4255,0.5232
    #              22,0.3224,0.4011
    #              18,0.5622,0.5239
    individual_time_file = open(global_path + "/Individual retrieval time dataset/Time for each query(PB)(online) ("+ str(number_of_1_topic_logs) + ", "+ str(number_of_2_topic_logs) + ", " + str(number_of_3_topic_logs) + ") blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    # The following variables are used for time recording, each variable stores the time that is indicated by it's name.
    # For example, start_bloom_time: stores the time required for the retrieval of all the logs at the start of the
    # blockchain using the bloom filter method. These variables refer to the total time required.
    # These variables later refer to the mean time.
    start_bloom_time, middle_bloom_time, end_bloom_time, total_bloom_time = 0, 0, 0, 0
    start_brute_time, middle_brute_time, end_brute_time, total_brute_time = 0, 0, 0, 0


    # The bloom filter retrieval time for all the logs in the start_logs list
    for log in start_logs:
        individual_time_start = time.time()
        block, position, bloom_time  = Log_Retrieval_bloom_filter_Online(log[0], log[1:-2], Starting_block,Ending_block,transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Online(log[0], log[1:-2], Starting_block,Ending_block,transactionHash=log[-2])
        individual_time_end = time.time()

        start_bloom_time = start_bloom_time + individual_time_med - individual_time_start
        start_brute_time = start_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")


    # The bloom filter retrieval time for all the logs in the middle_logs list
    for log in middle_logs:
        individual_time_start = time.time()
        block, position, bloom_time = Log_Retrieval_bloom_filter_Online(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Online(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])
        individual_time_end = time.time()


        middle_bloom_time = middle_bloom_time + individual_time_med - individual_time_start
        middle_brute_time = middle_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")


    # The bloom filter retrieval time for all the logs in the end_logs list
    for log in end_logs:
        individual_time_start = time.time()
        block, position, bloom_time = Log_Retrieval_bloom_filter_Online(log[0], log[1:-2], Starting_block,Ending_block,transactionHash=log[-2])
        individual_time_med = time.time()
        block, position, brute_time = Log_Retrieval_brute_force_Online(log[0], log[1:-2], Starting_block,Ending_block,transactionHash=log[-2])
        individual_time_end = time.time()


        end_bloom_time = end_bloom_time + individual_time_med - individual_time_start
        end_brute_time = end_brute_time + individual_time_end - individual_time_med
        individual_time_file.write(str(Starting_block + int(log[-1])) + "," + str(individual_time_med - individual_time_start) + "," + str(individual_time_end - individual_time_med) + "\n")

    individual_time_file.close()

    # log_number: the number of logs in the start_logs list, which is the same as the number
    # of logs in the middle_logs and end_logs lists
    log_number = len(start_logs)

    # total_bloom_time: the time for bloom filter retrieval of all the logs
    # total_brute_time: the time for brute force retrieval of all the logs
    total_bloom_time = start_bloom_time + middle_bloom_time + end_bloom_time
    total_brute_time = start_brute_time + middle_brute_time + end_brute_time

    # At this point the time refers to the mean time and not to the total time
    start_bloom_time, middle_bloom_time, end_bloom_time, total_bloom_time = start_bloom_time/log_number, middle_bloom_time/log_number, end_bloom_time/log_number, total_bloom_time/(log_number*3)
    start_brute_time, middle_brute_time, end_brute_time, total_brute_time = start_brute_time/log_number, middle_brute_time/log_number, end_brute_time/log_number, total_brute_time/(log_number*3)

    # ##  ##  Plot  ##  ##
    x = np.arange(4)
    bloom_measurments = [start_bloom_time, middle_bloom_time, end_bloom_time, total_bloom_time]
    brute_measurments = [start_brute_time, middle_brute_time, end_brute_time, total_brute_time]
    width = 0.35

    # plot data in grouped manner of bar type
    plt.bar(x - width/2, bloom_measurments, width, color='lightseagreen')
    plt.bar(x + width/2, brute_measurments, width, color='navy')

    plt.xticks(x, ['logs at the start','logs at the middle','logs at the end','Total logs'])

    plt.ylabel("Mean time (seconds)")
    bottom, top = plt.ylim()
    plt.ylim(bottom, 1.2*top)
    text = '1 topic logs: '+str(number_of_1_topic_logs)+'\n2 topic logs: '+str(number_of_2_topic_logs) + '\n3 topic logs: '+str(number_of_3_topic_logs)
    plt.text(-width, 1.2 * max([max(brute_measurments),max(bloom_measurments)]), text, ha='left', va='top', fontsize=10)
    plt.legend(["Bloom filter", "Brute force"],loc='upper right')
    plt.title('Online Performance Comparison based on log position ' + str((Starting_block,Ending_block)))


    for i, v in enumerate(bloom_measurments):
        plt.text( i - 0.1*width, v + 0.02*top, "%.3f" % v, ha="right", color='black')

    for i, v in enumerate(brute_measurments):
        plt.text( i + 0.1*width, v + 0.02*top, "%.3f" % v, ha="left", color='black')

    end = time.time()
    print("Total execution time of Log retrieval Position based comparison Online is: ", time.strftime("%H:%M:%S", time.gmtime(end - start)))
    plt.show()



