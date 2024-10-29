from Crypto.Hash import keccak
from eth_bloom import BloomFilter
import time
import matplotlib.pyplot as plt
import random
import numpy as np
from real_Ethereum_data_functions import Log_Retrieval_bloom_filter_Offline, Log_Retrieval_brute_force_Offline


##  Parameters  ##
# Define the local path
global_path = your_path

## ## Dataset creation functions ##  ##
## Create a group bloom filter database from the scrap database (real Ethereum data)
# using the group bloom filter algorithm
def Create_Group_BF_from_Scraped_data_4G_Method1(Starting_block: int, Ending_block: int) -> None:
    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Group blockchain Method1 Dataset/"

    # Open the file read the logs that have been scrapped by the Ethereum blockchain
    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    # Create a file to store the logs that belong to each group
    Logs_write = open(path2 + "[4]M1 Group logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    # Create a file to store the group bloom filters
    Bloom_Filter_write = open(path2 + "[4]M1 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter1 = BloomFilter()
    bloom_filter2 = BloomFilter()
    bloom_filter3 = BloomFilter()
    bloom_filter4 = BloomFilter()

    block1 = []
    block2 = []
    block3 = []
    block4 = []
    block_list = [block1, block2, block3, block4]


    log_counter = 0

    bf1 = 0
    bf2 = 0
    bf3 = 0
    bf4 = 0

    multiple_block_logs = []
    logs_appended = 0
    blocks_to_be_grouped = 4
    count = 0
    ii = 0
    element_count = 0
    for block_number in range(len(All_logs_pile)):
        block_logs = All_logs_pile[block_number].split(",")
        for log in block_logs:
            if log != "\n":
                elements = log.split(" ")[:-1]
                for element in elements:
                    multiple_block_logs.append(element)
                    logs_appended += 1
        count += 1
        if count == blocks_to_be_grouped:
            count = 0
            ii +=1
            print(ii)

            # hash the elements (address and topics) of all the logs in a group of 4 blocks
            for element in multiple_block_logs:
                k = keccak.new(digest_bits=256)
                k.update(bytes.fromhex(element[2:]))
                hash = k.hexdigest()

                hash_number = int(bytes(hash[12], 'utf-8'), 16)

                # The element is placed in a group based on its hash
                if hash_number < 4:
                    block1.append(element)
                    bloom_filter1.add(bytes.fromhex(element[2:]))
                    bf1 += 1
                    element_count +=1
                elif hash_number >= 4 and hash_number < 8:
                    block2.append(element)
                    bloom_filter2.add(bytes.fromhex(element[2:]))
                    bf2 += 1
                    element_count +=1
                elif hash_number >= 8 and hash_number < 12:
                    block3.append(element)
                    bloom_filter3.add(bytes.fromhex(element[2:]))
                    bf3 += 1
                    element_count +=1
                elif hash_number >= 12:
                    block4.append(element)
                    bloom_filter4.add(bytes.fromhex(element[2:]))
                    bf4 += 1
                    element_count +=1

            Bloom_Filter_write.write(str(int(bloom_filter1)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter2)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter3)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter4)) + "\n")

            write_logs = ""
            for block in block_list:
                for log in block:
                    write_logs = write_logs + log + ","
                Logs_write.write(write_logs + "\n")
                write_logs = ""

            bloom_filter1 = BloomFilter()
            bloom_filter2 = BloomFilter()
            bloom_filter3 = BloomFilter()
            bloom_filter4 = BloomFilter()

            #print(bf1, bf2, bf3, bf4)
            bf1 = 0
            bf2 = 0
            bf3 = 0
            bf4 = 0

            multiple_block_logs = []
            block1 = []
            block2 = []
            block3 = []
            block4 = []
            block_list = [block1, block2, block3, block4]

            logs_appended = 0
    print("GBF elements are:", element_count)


def Create_Group_BF_from_Scraped_data_4G_Method2(Starting_block: int, Ending_block: int) -> None:
    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Group blockchain Method2 Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "[4]M2 Group logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "[4]M2 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter1 = BloomFilter()
    bloom_filter2 = BloomFilter()
    bloom_filter3 = BloomFilter()
    bloom_filter4 = BloomFilter()

    block1 = []
    block2 = []
    block3 = []
    block4 = []
    block_list = [block1, block2, block3, block4]


    blocks_to_be_grouped = 4
    count = 0
    ii = 0
    element_count = 0
    for block_number in range(len(All_logs_pile)):
        block_logs = All_logs_pile[block_number].split(",")
        for log in block_logs:
            if log != "\n":
                elements = log.split(" ")

                # The address of a log is hashed
                k = keccak.new(digest_bits=256)
                k.update(bytes.fromhex(elements[0][2:]))
                hash = k.hexdigest()

                hash_number = int(bytes(hash[12], 'utf-8'), 16)
                address_hash_number = int(hash_number / 4)

                # The log (address and topics) is stored in a group based on the hash
                if address_hash_number == 0:
                    block1.append(log)
                elif address_hash_number == 1:
                    block2.append(log)
                elif address_hash_number == 2:
                    block3.append(log)
                elif address_hash_number == 3:
                    block4.append(log)

                for element in elements[:-1]:

                    if address_hash_number == 0:
                        bloom_filter1.add(bytes.fromhex(element[2:]))
                        element_count += 1
                    elif address_hash_number == 1:
                        bloom_filter2.add(bytes.fromhex(element[2:]))
                        element_count += 1
                    elif address_hash_number == 2:
                        bloom_filter3.add(bytes.fromhex(element[2:]))
                        element_count += 1
                    elif address_hash_number == 3:
                        bloom_filter4.add(bytes.fromhex(element[2:]))
                        element_count += 1


        count += 1
        # print(len(multiple_block_logs[-1]))
        if count == blocks_to_be_grouped:
            count = 0
            ii +=1
            print(ii)

            write_logs = ""
            for block in block_list:
                for log in block:
                    write_logs = write_logs + log + ","
                Logs_write.write(write_logs + "\n")
                write_logs = ""

            Bloom_Filter_write.write(str(int(bloom_filter1)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter2)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter3)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter4)) + "\n")

            bloom_filter1 = BloomFilter()
            bloom_filter2 = BloomFilter()
            bloom_filter3 = BloomFilter()
            bloom_filter4 = BloomFilter()

            block1 = []
            block2 = []
            block3 = []
            block4 = []
            block_list = [block1, block2, block3, block4]

    print("GBF elements are:", element_count)


def Create_Group_BF_from_Scraped_data_4G_Method3(Starting_block: int, Ending_block: int) -> None:
    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Group blockchain Method3 Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "[4]M3 Group logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "[4]M3 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")


    bloom_filter1 = BloomFilter()
    bloom_filter2 = BloomFilter()
    bloom_filter3 = BloomFilter()
    bloom_filter4 = BloomFilter()

    block1 = []
    block2 = []
    block3 = []
    block4 = []
    block_list = [block1, block2, block3, block4]

    blocks_to_be_grouped = 4
    count = 0
    ii = 0
    element_count = 0
    for block_number in range(len(All_logs_pile)):
        block_logs = All_logs_pile[block_number].split(",")
        for log in block_logs:
            if log != "\n":
                elements = log.split(" ")

                address_plus_topics = ""
                for i in elements[:-1]:
                    address_plus_topics += i[2:]

                k = keccak.new(digest_bits=256)
                k.update(bytes.fromhex(address_plus_topics))
                hash = k.hexdigest()

                hash_number = int(bytes(hash[12], 'utf-8'), 16)
                address_hash_number = int(hash_number / 4)

                if address_hash_number == 0:
                    block1.append(log)
                elif address_hash_number == 1:
                    block2.append(log)
                elif address_hash_number == 2:
                    block3.append(log)
                elif address_hash_number == 3:
                    block4.append(log)

                for element in elements[:-1]:
                    if address_hash_number == 0:
                        bloom_filter1.add(bytes.fromhex(element[2:]))
                        element_count += 1
                    elif address_hash_number == 1:
                        bloom_filter2.add(bytes.fromhex(element[2:]))
                        element_count += 1
                    elif address_hash_number == 2:
                        bloom_filter3.add(bytes.fromhex(element[2:]))
                        element_count += 1
                    elif address_hash_number == 3:
                        bloom_filter4.add(bytes.fromhex(element[2:]))
                        element_count += 1
        count += 1
        if count == blocks_to_be_grouped:
            count = 0
            ii +=1
            print(ii)

            write_logs = ""
            for block in block_list:
                for log in block:
                    write_logs = write_logs + log + ","
                Logs_write.write(write_logs + "\n")
                write_logs = ""

            Bloom_Filter_write.write(str(int(bloom_filter1)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter2)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter3)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter4)) + "\n")

            bloom_filter1 = BloomFilter()
            bloom_filter2 = BloomFilter()
            bloom_filter3 = BloomFilter()
            bloom_filter4 = BloomFilter()

            block1 = []
            block2 = []
            block3 = []
            block4 = []
            block_list = [block1, block2, block3, block4]

    print("GBF elements are:", element_count)


def Create_Group_BF_from_Scraped_data_4G_Method4(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Group blockchain Method4 Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "[4]M4 Group logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "[4]M4 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter1 = BloomFilter()
    bloom_filter2 = BloomFilter()
    bloom_filter3 = BloomFilter()
    bloom_filter4 = BloomFilter()

    block1 = []
    block2 = []
    block3 = []
    block4 = []
    block_list = [block1, block2, block3, block4]

    blocks_to_be_grouped = 4
    count = 0
    ii = 0
    element_count = 0
    for block_number in range(len(All_logs_pile)):
        block_logs = All_logs_pile[block_number].split(",")
        for log in block_logs:
            if log != "\n":
                elements = log.split(" ")

                k = keccak.new(digest_bits=256)
                k.update(bytes.fromhex(elements[0][2:]))
                hash = k.hexdigest()

                hash_number = int(bytes(hash[12], 'utf-8'), 16)
                address_hash_number = int(hash_number / 4)

                if address_hash_number == 0:
                    block1.append(log)
                elif address_hash_number == 1:
                    block2.append(log)
                elif address_hash_number == 2:
                    block3.append(log)
                elif address_hash_number == 3:
                    block4.append(log)


                for element in elements[:-1]:

                    if address_hash_number == 0:
                        bloom_filter1.add(bytes.fromhex(element[2:]))
                        element_count += 1
                    elif address_hash_number == 1:
                        bloom_filter2.add(bytes.fromhex(element[2:]))
                        element_count += 1
                    elif address_hash_number == 2:
                        bloom_filter3.add(bytes.fromhex(element[2:]))
                        element_count += 1
                    elif address_hash_number == 3:
                        bloom_filter4.add(bytes.fromhex(element[2:]))
                        element_count += 1

        count += 1
        if count == blocks_to_be_grouped:
            count = 0
            ii +=1
            print(ii)

            write_logs = ""
            for block in block_list:
                for log in block:
                    write_logs = write_logs + log + ","
                Logs_write.write(write_logs + "\n")
                write_logs = ""

            Bloom_Filter_write.write(str(int(bloom_filter1)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter2)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter3)) + "\n")
            Bloom_Filter_write.write(str(int(bloom_filter4)) + "\n")

            bloom_filter1 = BloomFilter()
            bloom_filter2 = BloomFilter()
            bloom_filter3 = BloomFilter()
            bloom_filter4 = BloomFilter()

            block1 = []
            block2 = []
            block3 = []
            block4 = []
            block_list = [block1, block2, block3, block4]

    print("GBF elements are:", element_count)




##  ##  Log Retrieval functions ##  ##
def Log_Retrieval_Group_bloom_filter_4G_Method1(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:
    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Group blockchain Method1 Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "[4]M1 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()

    k = keccak.new(digest_bits=256)
    k.update(bytes.fromhex(address[2:]))
    hash = k.hexdigest()
    hash_number = int(bytes(hash[12], 'utf-8'), 16)
    hash_group_number_address = int(hash_number/4)

    hash_group_number_topics = []
    for topic in topics:
        k = keccak.new(digest_bits=256)
        k.update(bytes.fromhex(topic[2:]))
        hash = k.hexdigest()
        hash_number = int(bytes(hash[12], 'utf-8'), 16)
        hash_group_number = int(hash_number / 4)
        hash_group_number_topics.append(hash_group_number)


    itterational_bf_checks = len(list(set(hash_group_number_topics + [hash_group_number_address])))

    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_groups_checked = []
    num_of_blocks_checked = 0
    num_of_bfs_checked = 0
    for group_num in range(int(len(File_group_bloom_filter)/4)):

        block_number = group_num*4

        group1_bf = BloomFilter(int(File_group_bloom_filter[block_number]))
        group2_bf = BloomFilter(int(File_group_bloom_filter[block_number+1]))
        group3_bf = BloomFilter(int(File_group_bloom_filter[block_number+2]))
        group4_bf = BloomFilter(int(File_group_bloom_filter[block_number+3]))

        bloom_filter_list = [group1_bf, group2_bf, group3_bf, group4_bf]

        num_of_bfs_checked += 1
        topic_flag = 1
        for i in range(len(topics)):
            if bytes.fromhex(topics[i][2:]) not in bloom_filter_list[hash_group_number_topics[i]]:
                topic_flag = 0
                break

        if bytes.fromhex(address[2:]) in bloom_filter_list[hash_group_number_address]:
            if topic_flag:
                list_of_groups_checked.append(block_number)
                for num in range(4):
                    num_of_blocks_checked += 1
                    block_logs = All_logs[block_number + num].split(",")
                    for count, log in enumerate(block_logs):
                        log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                        if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                            if topics == log[1:-1]:
                                if transactionHash == "none":
                                    blocks_of_found_element.append(block_number + num)
                                    positions_of_found_element_in_block.append(count)

                                elif transactionHash == log[-1]:
                                    blocks_of_found_element.append(block_number + num)
                                    positions_of_found_element_in_block.append(count)

                    if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break

    time3 = time.time()

    # This function returns: the blocks in which the log is found (list)
    #                        the positions of the found log in each block (list)
    #                        the time required for the retrieval
    #                        the number of blocks checked, the number of bloom filters checked and the list of groups checked during the retrieval process
    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked * itterational_bf_checks, list_of_groups_checked)


def Log_Retrieval_Group_bloom_filter_4G_Method2(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:
    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Group blockchain Method2 Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "[4]M2 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()

    k = keccak.new(digest_bits=256)
    k.update(bytes.fromhex(address[2:]))
    hash = k.hexdigest()
    hash_number = int(bytes(hash[12], 'utf-8'), 16)
    hash_group_number_address = int(hash_number/4)


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_groups_checked = 0
    num_of_blocks_checked = 0
    num_of_bfs_checked = 0
    for group_num in range(int(len(File_group_bloom_filter)/4)):

        block_number = group_num*4

        group_bf = BloomFilter(int(File_group_bloom_filter[block_number + hash_group_number_address]))

        num_of_bfs_checked += 1
        topic_flag = 1
        for i in range(len(topics)):
            if bytes.fromhex(topics[i][2:]) not in group_bf:
                topic_flag = 0
                break

        if bytes.fromhex(address[2:]) in group_bf:
            if topic_flag:
                list_of_positive_bfs.append(block_number)
                num_of_groups_checked += 1
                for num in range(4):
                    num_of_blocks_checked +=1
                    block_logs = All_logs[block_number + num].split(",")
                    for count, log in enumerate(block_logs):
                        log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                        if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                            if topics == log[1:-1]:
                                if transactionHash == "none":
                                    blocks_of_found_element.append(block_number + num)
                                    positions_of_found_element_in_block.append(count)
                                elif transactionHash == log[-1]:
                                    blocks_of_found_element.append(block_number + num)
                                    positions_of_found_element_in_block.append(count)

                    if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break

    time3 = time.time()

    # This function returns: the blocks in which the log is found (list)
    #                        the positions of the found log in each block (list)
    #                        the time required for the retrieval
    #                        the number of blocks checked, the number of bloom filters checked and the list of positive bloom filters during the retrieval process
    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_Group_bloom_filter_4G_Method3(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Group blockchain Method3 Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "[4]M3 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()

    address_plus_topics = ""
    for i in [address] + topics:
        address_plus_topics += i[2:]


    k = keccak.new(digest_bits=256)
    k.update(bytes.fromhex(address_plus_topics))
    hash = k.hexdigest()
    hash_number = int(bytes(hash[12], 'utf-8'), 16)
    hash_group_number_address = int(hash_number/4)


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_groups_checked = 0
    num_of_blocks_checked = 0
    num_of_bfs_checked = 0
    for group_index in range(int(len(File_group_bloom_filter)/4)):

        block_number = group_index*4

        group_bf = BloomFilter(int(File_group_bloom_filter[block_number + hash_group_number_address]))

        num_of_bfs_checked += 1
        topic_flag = 1
        for i in range(len(topics)):
            if bytes.fromhex(topics[i][2:]) not in group_bf:
                topic_flag = 0
                break

        if bytes.fromhex(address[2:]) in group_bf:
            if topic_flag:
                list_of_positive_bfs.append(block_number)
                num_of_groups_checked += 1
                for num in range(4):

                    num_of_blocks_checked +=1
                    block_logs = All_logs[block_number + num].split(",")
                    for count, log in enumerate(block_logs):
                        log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                        if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                            if topics == log[1:-1]:
                                if transactionHash == "none":
                                    blocks_of_found_element.append(block_number + num)
                                    positions_of_found_element_in_block.append(count)
                                elif transactionHash == log[-1]:
                                    blocks_of_found_element.append(block_number + num)
                                    positions_of_found_element_in_block.append(count)

                    if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break

    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_Group_bloom_filter_4G_Method4(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path2 = global_path + "Group blockchain Method4 Dataset/"

    File_Logs = open(path2 + "[4]M4 Group logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "[4]M4 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()

    k = keccak.new(digest_bits=256)
    k.update(bytes.fromhex(address[2:]))
    hash = k.hexdigest()
    hash_number = int(bytes(hash[12], 'utf-8'), 16)
    hash_group_number_address = int(hash_number/4)

    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_groups_checked = 0
    num_of_blocks_checked = 0
    num_of_bfs_checked = 0
    for group_num in range(int(len(File_group_bloom_filter)/4)):

        block_number = group_num*4

        group_bf = BloomFilter(int(File_group_bloom_filter[block_number + hash_group_number_address]))

        num_of_bfs_checked += 1
        topic_flag = 1
        for i in range(len(topics)):
            if bytes.fromhex(topics[i][2:]) not in group_bf:
                topic_flag = 0
                break

        if bytes.fromhex(address[2:]) in group_bf:
            if topic_flag:
                list_of_positive_bfs.append(block_number + hash_group_number_address)
                num_of_groups_checked += 1
                num_of_blocks_checked +=1
                block_logs = All_logs[block_number + hash_group_number_address].split(",")
                for count, log in enumerate(block_logs):
                    log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                    if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                        if topics == log[1:-1]:
                            if transactionHash == "none":
                                blocks_of_found_element.append(block_number + hash_group_number_address)
                                positions_of_found_element_in_block.append(count)
                            elif transactionHash == log[-1]:
                                blocks_of_found_element.append(block_number + hash_group_number_address)
                                positions_of_found_element_in_block.append(count)

                    if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break

    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)




##  ##  False positive analysis functions  ##  ##
def False_positive_analysis_bloom_filter(address, topics, positive_bfs:list,dataset:tuple):
    Starting_block, Ending_block = dataset

    path1 = global_path + "Scrap Blockchain Database/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    given_log_elements = [address] + topics
    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs:
            elements = log.split(" ")[:-1]

            for element in elements:
                if element in given_log_elements:
                    same_element_indexes = [i for i in range(len(given_log_elements)) if given_log_elements[i] == element]

                    for i in same_element_indexes:
                        result_list[i] = 1
        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_4G_Method1(address, topics, positive_bfs:list,dataset:tuple):

    Starting_block, Ending_block = dataset

    path1 = global_path + "Group blockchain Method1 Dataset/"

    File_Logs = open(path1 +"[4]M1 Group logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    given_log_elements = [address] + topics
    given_log_elements_group = []

    for given_element_num in range(len(given_log_elements)):
        k = keccak.new(digest_bits=256)
        k.update(bytes.fromhex(given_log_elements[given_element_num][2:]))
        hash = k.hexdigest()
        hash_number = int(bytes(hash[12], 'utf-8'), 16)
        hash_group_number = int(hash_number / 4)
        given_log_elements_group.append(hash_group_number)


    justified_fp = 0
    compressed_fp = 0

    for group_num in positive_bfs[:-1]:
        result_list = [0 for i in range(len(given_log_elements))]

        for given_element_num in range(len(given_log_elements)):

            block_elements = All_logs_pile[group_num + given_log_elements_group[given_element_num]].split(",")

            for element in block_elements:
                if element == given_log_elements[given_element_num]:
                    result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_4G_Method2(address, topics, positive_bfs:list,dataset:tuple):

    Starting_block, Ending_block = dataset

    path1 = global_path + "Group blockchain Method2 Dataset/"

    File_Logs = open(path1 +"[4]M2 Group logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    given_log_elements = [address] + topics

    k = keccak.new(digest_bits=256)
    k.update(bytes.fromhex(address[2:]))
    hash = k.hexdigest()
    hash_number = int(bytes(hash[12], 'utf-8'), 16)
    hash_group_number = int(hash_number / 4)


    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num + hash_group_number].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                if element in given_log_elements:
                    same_element_indexes = [i for i in range(len(given_log_elements)) if given_log_elements[i] == element]

                    for i in same_element_indexes:
                        result_list[i] = 1
        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_4G_Method3(address, topics, positive_bfs:list,dataset:tuple):

    Starting_block, Ending_block = dataset

    path1 = global_path + "Group blockchain Method3 Dataset/"

    File_Logs = open(path1 +"[4]M3 Group logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    given_log_elements = [address] + topics

    address_plus_topics = ""
    for i in [address] + topics:
        address_plus_topics += i[2:]


    k = keccak.new(digest_bits=256)
    k.update(bytes.fromhex(address_plus_topics))
    hash = k.hexdigest()
    hash_number = int(bytes(hash[12], 'utf-8'), 16)
    hash_group_number = int(hash_number/4)


    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num + hash_group_number].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                if element in given_log_elements:
                    same_element_indexes = [i for i in range(len(given_log_elements)) if given_log_elements[i] == element]

                    for i in same_element_indexes:
                        result_list[i] = 1
        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_4G_Method4(address, topics, positive_bfs:list,dataset:tuple):

    Starting_block, Ending_block = dataset

    path1 = global_path + "Group blockchain Method4 Dataset/"

    File_Logs = open(path1 +"[4]M4 Group logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    given_log_elements = [address] + topics


    k = keccak.new(digest_bits=256)
    k.update(bytes.fromhex(address[2:0]))
    hash = k.hexdigest()
    hash_number = int(bytes(hash[12], 'utf-8'), 16)
    hash_group_number = int(hash_number/4)


    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                if element in given_log_elements:
                    same_element_indexes = [i for i in range(len(given_log_elements)) if given_log_elements[i] == element]

                    for i in same_element_indexes:
                        result_list[i] = 1
        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp




##  ##  Retrieval Test  ##  ##
def Log_Retrieval_Random_TopicBased_Bloom_Brute_GBF_plot(Number_of_logs_to_check: int, Scrap_database: tuple, Method_number: int, create_all_plots = True, show_plot = False):
    # The first argument that is required is the number of logs to check.
    # The second argument is the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database.
    # The Method_number: This refers to the group bloom filter method to be tested
    # The available methods with their coding are: Group bloom filter Method 1 -> 1
    #                                              Group bloom filter Method 2 -> 2
    #                                              Group bloom filter Method 3 -> 3
    #                                              Group bloom filter Method 4 -> 4
    # create_all_plots: if True, the plots that are created are blocks checked, bloom filters checked, positive bloom filters and false positive analysis
    #                   if False, only the blocks checked plot is created
    # show_plot: if True, the plots that are created are shown, If False no plots are shown
    # The plots that are created are stored locally

    start = time.time()
    print("Starting Time:", time.strftime("%H:%M:%S", time.gmtime(start)))
    Starting_block, Ending_block = Scrap_database
    path = global_path

    File_Logs = open(global_path + "Scrap Blockchain Database/Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()

    File_Logs.close()

    # Method Selection
    if Method_number == 1:
        GBF_Log_Retrieval = Log_Retrieval_Group_bloom_filter_4G_Method1
        GBF_False_positive_analysis = False_positive_analysis_4G_Method1
        Method_code = "Group_bf_M1"
    elif Method_number == 2:
        GBF_Log_Retrieval = Log_Retrieval_Group_bloom_filter_4G_Method2
        GBF_False_positive_analysis = False_positive_analysis_4G_Method2
        Method_code = "Group_bf_M2"
    elif Method_number == 3:
        GBF_Log_Retrieval = Log_Retrieval_Group_bloom_filter_4G_Method3
        GBF_False_positive_analysis = False_positive_analysis_4G_Method3
        Method_code = "Group_bf_M3"
    elif Method_number == 4:
        GBF_Log_Retrieval = Log_Retrieval_Group_bloom_filter_4G_Method4
        GBF_False_positive_analysis = False_positive_analysis_4G_Method4
        Method_code = "Group_bf_M4"


    ##  ##  Data Selection  ##  ##
    one_topic_logs = []
    two_topic_logs = []
    three_topic_logs = []
    four_topic_logs = []

    random.seed(2)

    num_of_logs = 0
    # The while loop is terminated only when the flag is set to 0
    while num_of_logs < Number_of_logs_to_check:
        # random_block_number: a random number between the number 0 and the number of blocks in the database
        random_block_number = random.randint(0,Ending_block - Starting_block - 1)

        # The Entries list is a list containing all the logs of the specific block
        Entries = All_logs[random_block_number].split(",")

        # entry is the random entry that is selected.
        # entry is initially a string but becomes a list representing the log in the following manner:
        # entry = [address, topic1, topic2, topic3, topic4, transactionHash]
        entry = random.choice(Entries) # entry: string
        if entry not in one_topic_logs + two_topic_logs + three_topic_logs + four_topic_logs:
            num_of_logs += 1
            entry = entry.split(" ") # entry: list
            entry.append(str(random_block_number))

            # num_of_topics is the number of topics
            num_of_topics = len(entry[1:-2])

            if num_of_topics == 1:
                one_topic_logs.append(entry)
            elif num_of_topics == 2:
                two_topic_logs.append(entry)
            elif num_of_topics == 3:
                three_topic_logs.append(entry)
            elif num_of_topics == 4:
                four_topic_logs.append(entry)

    ##  ##  Retrieval statistics recording  ##  ##

    # The following variables refer to the the blocks checked, bloom filters checked and the positive bloom filters plots
    one_topic_bloom_blocks_checked, two_topic_bloom_blocks_checked, three_topic_bloom_blocks_checked, four_topic_bloom_blocks_checked, total_bloom_blocks_checked = ([], 0), ([], 0), ([], 0), ([], 0), ([], 0)
    one_topic_brute_blocks_checked, two_topic_brute_blocks_checked, three_topic_brute_blocks_checked, four_topic_brute_blocks_checked, total_brute_blocks_checked = 0, 0, 0, 0, 0
    one_topic_group_blocks_checked, two_topic_group_blocks_checked, three_topic_group_blocks_checked, four_topic_group_blocks_checked, total_group_blocks_checked = (0, 0, []), (0, 0, []), (0, 0, []), (0, 0, []), (0, 0, [])

    # The following variables refer to the false positive analysis plot
    total_bloom_justified_fp = 0
    total_bloom_compressed_fp = 0
    total_groupbf_justified_fp = 0
    total_groupbf_compressed_fp = 0


    for log in one_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        justified_fp, compressed_fp = False_positive_analysis_bloom_filter(log[0], log[1:-2], bloom_blocks_checked[0], (Starting_block, Ending_block))
        total_bloom_justified_fp += justified_fp
        total_bloom_compressed_fp += compressed_fp

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,                                                    transactionHash=log[-2])

        block, position, group_time, group_blocks_checked = GBF_Log_Retrieval(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        justified_fp, compressed_fp = GBF_False_positive_analysis(log[0], log[1:-2], group_blocks_checked[2], (Starting_block, Ending_block))
        total_groupbf_justified_fp += justified_fp
        total_groupbf_compressed_fp += compressed_fp

        one_topic_bloom_blocks_checked = tuple([one_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(one_topic_bloom_blocks_checked))])
        one_topic_brute_blocks_checked = one_topic_brute_blocks_checked + block[0] + 1
        one_topic_group_blocks_checked = tuple([one_topic_group_blocks_checked[i] + group_blocks_checked[i] for i in range(len(one_topic_group_blocks_checked))])


    for log in two_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        justified_fp, compressed_fp = False_positive_analysis_bloom_filter(log[0], log[1:-2], bloom_blocks_checked[0], (Starting_block, Ending_block))
        total_bloom_justified_fp += justified_fp
        total_bloom_compressed_fp += compressed_fp

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, group_time, group_blocks_checked = GBF_Log_Retrieval(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        justified_fp, compressed_fp = GBF_False_positive_analysis(log[0], log[1:-2], group_blocks_checked[2], (Starting_block, Ending_block))
        total_groupbf_justified_fp += justified_fp
        total_groupbf_compressed_fp += compressed_fp

        two_topic_bloom_blocks_checked = tuple([two_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(two_topic_bloom_blocks_checked))])
        two_topic_brute_blocks_checked = two_topic_brute_blocks_checked + block[0] + 1
        two_topic_group_blocks_checked = tuple([two_topic_group_blocks_checked[i] + group_blocks_checked[i] for i in range(len(two_topic_group_blocks_checked))])


    for log in three_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        justified_fp, compressed_fp = False_positive_analysis_bloom_filter(log[0], log[1:-2], bloom_blocks_checked[0], (Starting_block, Ending_block))
        total_bloom_justified_fp += justified_fp
        total_bloom_compressed_fp += compressed_fp

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, group_time, group_blocks_checked = GBF_Log_Retrieval(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        justified_fp, compressed_fp = GBF_False_positive_analysis(log[0], log[1:-2], group_blocks_checked[2], (Starting_block, Ending_block))
        total_groupbf_justified_fp += justified_fp
        total_groupbf_compressed_fp += compressed_fp

        three_topic_bloom_blocks_checked = tuple([three_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(three_topic_bloom_blocks_checked))])
        three_topic_brute_blocks_checked = three_topic_brute_blocks_checked + block[0] + 1
        three_topic_group_blocks_checked = tuple([three_topic_group_blocks_checked[i] + group_blocks_checked[i] for i in range(len(three_topic_group_blocks_checked))])


    for log in four_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        justified_fp, compressed_fp = False_positive_analysis_bloom_filter(log[0], log[1:-2], bloom_blocks_checked[0], (Starting_block, Ending_block))
        total_bloom_justified_fp += justified_fp
        total_bloom_compressed_fp += compressed_fp

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, group_time, group_blocks_checked = GBF_Log_Retrieval(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        justified_fp, compressed_fp = GBF_False_positive_analysis(log[0], log[1:-2], group_blocks_checked[2], (Starting_block, Ending_block))
        total_groupbf_justified_fp += justified_fp
        total_groupbf_compressed_fp += compressed_fp

        four_topic_bloom_blocks_checked = tuple([four_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(four_topic_bloom_blocks_checked))])
        four_topic_brute_blocks_checked = four_topic_brute_blocks_checked + block[0] + 1
        four_topic_group_blocks_checked = tuple([four_topic_group_blocks_checked[i] + group_blocks_checked[i] for i in range(len(four_topic_group_blocks_checked))])


    total_bloom_blocks_checked = tuple([one_topic_bloom_blocks_checked[i] + two_topic_bloom_blocks_checked[i] + three_topic_bloom_blocks_checked[i] + four_topic_bloom_blocks_checked[i] for i in range(len(one_topic_bloom_blocks_checked))])
    total_brute_blocks_checked = one_topic_brute_blocks_checked + two_topic_brute_blocks_checked + three_topic_brute_blocks_checked + four_topic_brute_blocks_checked
    total_group_blocks_checked = tuple([one_topic_group_blocks_checked[i] + two_topic_group_blocks_checked[i] + three_topic_group_blocks_checked[i] + four_topic_group_blocks_checked[i] for i in range(len(one_topic_group_blocks_checked))])

    end = time.time()
    print("Total execution time of Log retrieval Position based comparison is: ", time.strftime("%H:%M:%S", time.gmtime(end - start)))


    # ##  ##  Plot  ##  ##
    x = np.arange(5)

    bloom_blocks_checked_measurments = [len(one_topic_bloom_blocks_checked[0]), len(two_topic_bloom_blocks_checked[0]), len(three_topic_bloom_blocks_checked[0]), len(four_topic_bloom_blocks_checked[0]), len(total_bloom_blocks_checked[0])]
    brute_blocks_checked_measurments = [one_topic_brute_blocks_checked, two_topic_brute_blocks_checked, three_topic_brute_blocks_checked, four_topic_brute_blocks_checked, total_brute_blocks_checked]
    group16_blocks_checked_measurments = [one_topic_group_blocks_checked[0], two_topic_group_blocks_checked[0], three_topic_group_blocks_checked[0], four_topic_group_blocks_checked[0], total_group_blocks_checked[0]]

    width = 0.25

    plt.figure().set_size_inches(14,5)

    # plot data in grouped manner of bar type
    plt.bar(x - width, bloom_blocks_checked_measurments, width, color='darkgoldenrod')
    plt.bar(x , brute_blocks_checked_measurments, width, color='cadetblue')
    plt.bar(x + width, group16_blocks_checked_measurments, width, color='darkmagenta')

    plt.xticks(x, ['One topic logs', 'Two topic logs', 'Three topic logs', 'Four topic logs', 'Total logs'])

    plt.ylabel("Number of blocks checked")
    bottom, top = plt.ylim()
    plt.ylim(bottom, 1.5*top)
    text = 'Total logs:   ' + str(Number_of_logs_to_check) + '\n1 topic logs: '+str(len(one_topic_logs))+'\n2 topic logs: '+str(len(two_topic_logs)) + '\n3 topic logs: '+str(len(three_topic_logs)) + '\n4 topic logs: '+str(len(four_topic_logs))
    plt.text(-1.5 * width, 1.5 * max([max(brute_blocks_checked_measurments), max(bloom_blocks_checked_measurments), max(group16_blocks_checked_measurments)]), text, ha='left', va='top', fontsize=10)
    plt.legend(["Bloom filter", "Brute force", Method_code], loc='upper right')
    # plt.legend(handles=['1 topic logs: '+str(number_of_1_topic_logs), "2 topic logs: "+str(number_of_2_topic_logs), "3 topic logs: "+str(number_of_3_topic_logs)], loc='upper left')
    plt.title('Blocks Checked based on number of topics ('+str(Starting_block)+" - "+str(Ending_block)+")")

    number_size = 9
    for i, v in enumerate(bloom_blocks_checked_measurments):
        plt.text( i - width, v + 0.02*top, v, ha="center", color='black', fontsize=number_size)

    for i, v in enumerate(brute_blocks_checked_measurments):
        plt.text( i , v + 0.02*top, v, ha="center", color='black', fontsize=number_size)

    for i, v in enumerate(group16_blocks_checked_measurments):
        plt.text( i + width, v + 0.02*top, v, ha="center", color='black', fontsize=number_size)


    plt.savefig(path + "Group bf plots/Blocks Checked BlF-BrF-" + Method_code + "(" + str(Number_of_logs_to_check) + ", " + str(Starting_block) + ").jpg", bbox_inches= 'tight') # , dpi= 500, bbox_inches= 'tight'
    if show_plot:
        plt.show()
    else:
        plt.close()


    if create_all_plots == True:
        ##  Bloom filters Checked plot  ##
        bloom_blocks_checked_measurments = [one_topic_bloom_blocks_checked[1], two_topic_bloom_blocks_checked[1], three_topic_bloom_blocks_checked[1], four_topic_bloom_blocks_checked[1], total_bloom_blocks_checked[1]]
        group16_blocks_checked_measurments = [one_topic_group_blocks_checked[1], two_topic_group_blocks_checked[1], three_topic_group_blocks_checked[1], four_topic_group_blocks_checked[1], total_group_blocks_checked[1]]

        width = 0.3

        plt.figure().set_size_inches(12, 5)

        # plot data in grouped manner of bar type
        plt.bar(x - width*0.5, bloom_blocks_checked_measurments, width, color='darkgoldenrod')
        plt.bar(x + width*0.5, group16_blocks_checked_measurments, width, color='darkmagenta')

        plt.xticks(x, ['One topic logs', 'Two topic logs', 'Three topic logs', 'Four topic logs', 'Total logs'])

        plt.ylabel("Number of bloom filters checked")
        bottom, top = plt.ylim()
        plt.ylim(bottom, 1.5*top)
        text = 'Total logs:   '+ str(Number_of_logs_to_check) + '\n1 topic logs: '+str(len(one_topic_logs))+'\n2 topic logs: '+str(len(two_topic_logs)) + '\n3 topic logs: '+str(len(three_topic_logs)) + '\n4 topic logs: '+str(len(four_topic_logs))
        plt.text(-1.5 * width, 1.5 * max([max(bloom_blocks_checked_measurments), max(group16_blocks_checked_measurments)]), text, ha='left', va='top', fontsize=10)
        plt.legend(["Bloom filter", Method_code], loc='upper right')
        # plt.legend(handles=['1 topic logs: '+str(number_of_1_topic_logs), "2 topic logs: "+str(number_of_2_topic_logs), "3 topic logs: "+str(number_of_3_topic_logs)], loc='upper left')
        plt.title('Bloom Filters Checked based on number of topics ('+str(Starting_block)+" - "+str(Ending_block)+")")


        for i, v in enumerate(bloom_blocks_checked_measurments):
            plt.text( i - width*0.5, v + 0.02*top, v, ha="center", color='black')

        for i, v in enumerate(group16_blocks_checked_measurments):
            plt.text( i + width*0.5, v + 0.02*top, v, ha="center", color='black')

        plt.savefig(path + "Group bf plots/BFs Checked BlF-BrF-" + Method_code + "(" + str(Number_of_logs_to_check) + ", " + str(Starting_block) + ").jpg",bbox_inches='tight')  # , dpi= 500, bbox_inches= 'tight'
        if show_plot:
            plt.show()
        else:
            plt.close()


        ##  Positive bloom filter responses plot  ##
        bloom_blocks_checked_measurments = [len(one_topic_bloom_blocks_checked[0]), len(two_topic_bloom_blocks_checked[0]), len(three_topic_bloom_blocks_checked[0]), len(four_topic_bloom_blocks_checked[0]), len(total_bloom_blocks_checked[0])]
        group16_blocks_checked_measurments = [len(one_topic_group_blocks_checked[2]), len(two_topic_group_blocks_checked[2]), len(three_topic_group_blocks_checked[2]), len(four_topic_group_blocks_checked[2]), len(total_group_blocks_checked[2])]

        width = 0.3

        plt.figure().set_size_inches(12, 5)

        # plot data in grouped manner of bar type
        plt.bar(x - width*0.5, bloom_blocks_checked_measurments, width, color='darkgoldenrod')
        plt.bar(x + width*0.5, group16_blocks_checked_measurments, width, color='darkmagenta')

        plt.xticks(x, ['One topic logs', 'Two topic logs', 'Three topic logs', 'Four topic logs', 'Total logs'])

        plt.ylabel("Number of positive bloom filters responses")
        bottom, top = plt.ylim()
        plt.ylim(bottom, 1.5*top)
        text = 'Total logs:   ' + str(Number_of_logs_to_check) + '\n1 topic logs: '+str(len(one_topic_logs))+'\n2 topic logs: '+str(len(two_topic_logs)) + '\n3 topic logs: '+str(len(three_topic_logs)) + '\n4 topic logs: '+str(len(four_topic_logs))
        plt.text(-1.5 * width, 1.5 * max([max(bloom_blocks_checked_measurments), max(group16_blocks_checked_measurments)]), text, ha='left', va='top', fontsize=10)
        plt.legend(["Bloom filter", Method_code], loc='upper right')
        # plt.legend(handles=['1 topic logs: '+str(number_of_1_topic_logs), "2 topic logs: "+str(number_of_2_topic_logs), "3 topic logs: "+str(number_of_3_topic_logs)], loc='upper left')
        plt.title('Positive Bloom Filters Responses based on number of topics ('+str(Starting_block)+" - "+str(Ending_block)+")")

        for i, v in enumerate(bloom_blocks_checked_measurments):
            plt.text( i - width*0.5, v + 0.02*top, v, ha="center", color='black')

        for i, v in enumerate(group16_blocks_checked_measurments):
            plt.text( i + width*0.5, v + 0.02*top, v, ha="center", color='black')

        plt.savefig(path + "Group bf plots/Positive Bf responses BlF-BrF-" + Method_code + "(" + str(Number_of_logs_to_check) + ", " + str(Starting_block) + ").jpg",bbox_inches='tight')  # , dpi= 500, bbox_inches= 'tight'
        if show_plot:
            plt.show()
        else:
            plt.close()


        ##  False Positive Analysis plot ##
        justified_measurments = [total_bloom_justified_fp, total_groupbf_justified_fp]
        compressed_measurments = [total_bloom_compressed_fp, total_groupbf_compressed_fp]

        x = np.arange(2)

        width = 0.25

        # plot data in grouped manner of bar type
        plt.bar(x - width*0.5, justified_measurments, width, color='darkviolet')
        plt.bar(x + width*0.5, compressed_measurments, width, color='forestgreen')

        plt.xticks(x, ['Bloom filter', Method_code])
        # plt.xlabel("Teams")
        plt.ylabel("number of false positives")
        plt.legend(["Justified", "Comperssed"])
        bottom, top = plt.ylim()
        plt.ylim(bottom, 1.5*top)
        text = 'Total logs:   '+ str(Number_of_logs_to_check) + '\n1 topic logs: '+str(len(one_topic_logs))+'\n2 topic logs: '+str(len(two_topic_logs)) + '\n3 topic logs: '+str(len(three_topic_logs)) + '\n4 topic logs: '+str(len(four_topic_logs))
        plt.text(-1 * width, 1.5 * max([max(justified_measurments), max(compressed_measurments)]), text, ha='left', va='top', fontsize=10)
        plt.title('False positive analysis ('+str(Starting_block)+" - "+str(Ending_block)+")")


        for i, v in enumerate(justified_measurments):
            plt.text( i - width*0.5, v + 0.02*top, v, ha="center", color='black')

        for i, v in enumerate(compressed_measurments):
            plt.text( i + width*0.5, v + 0.02*top, v, ha="center", color='black')

        plt.savefig(path + "Group bf plots/TB False positive analysis BlF-BrF-" + Method_code + "(" + str(Number_of_logs_to_check) + ", " + str(Starting_block) + ").jpg",bbox_inches='tight')  # , dpi= 500, bbox_inches= 'tight'
        if show_plot:
            plt.show()
        else:
            plt.close()




##  ##  Other Tests  ##  ##
def Address_frequency_plot(block_number, dataset: tuple):
    Starting_block, Ending_block = dataset


    File_Logs = open(global_path + "Scrap Blockchain Database/Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_Logs.close()

    block_logs = All_logs[block_number].split(",")

    address_list = []
    address_freq_list = []

    for log in block_logs:
        elements = log.split(" ")
        if elements[0] != "\n":

            if elements[0] in address_list:
                index = address_list.index(elements[0])
                num = address_freq_list[index][1]
                address_freq_list[index] = (elements[0],num+1)
            else:
                address_list.append(elements[0])
                address_freq_list.append((elements[0],1))


    address_freq_list.sort(key=lambda x: x[1],reverse=True)

    print(address_freq_list)

    ## Ploting  ##
    x_points = []
    y_points = []
    for i in address_freq_list:
        x_points.append(i[0])
        y_points.append(i[1])

    x_points = [i[2:6] for i in x_points]


    fig, ax = plt.subplots()


    ax.bar(x_points, y_points)

    ax.set_ylabel('Frrequency')
    ax.set_xlabel('Address')
    ax.set_title('Address frequency in block ' + str(Starting_block+block_number))
    plt.xticks(rotation=90)

    plt.show()


def Address_blockchain_frequency_test(num_of_elements: int, dataset: tuple):
    Starting_block, Ending_block = dataset

    File_Logs = open(global_path + "Scrap Blockchain Database/Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_Logs.close()


    random.seed(0)
    element_list = []
    for element_num in range(num_of_elements):

        random_block_number = random.randint(0,len(All_logs) - 1)

        block_logs = All_logs[random_block_number].split(",")
        while len(block_logs) < 2:
            random_block_number = random.randint(0, len(All_logs) - 1)
            block_logs = All_logs[random_block_number].split(",")

        random_element_number = random.randint(0,len(block_logs) - 2)

        log = block_logs[random_element_number].split(" ")[:-1]

        element = log[0]

        element_list.append((element,random_block_number, random_element_number))


    element_result_list = []
    total_same_block_hits = 0
    total_diff_block_hits = 0
    num_of_random_elements_to_be_compared = 100

    same_elements_diff_block = 0
    same_elements_same_block = 0
    for element in element_list:
        flag = 0
        total_same_block_hits += same_elements_same_block
        total_diff_block_hits += same_elements_diff_block
        same_elements_diff_block = 0
        diff_elements_diff_block = 0
        same_elements_same_block = 0
        diff_elements_same_block = 0

        while flag == 0:
            random_block_number = random.randint(0, len(All_logs) - 1)
            block_logs = All_logs[random_block_number].split(",")
            while len(block_logs) < 2:
                random_block_number = random.randint(0, len(All_logs) - 1)
                block_logs = All_logs[random_block_number].split(",")
            random_element_number = random.randint(0, len(block_logs) - 2)
            log = block_logs[random_element_number].split(" ")[:-1]
            # random_element = random.choice(log)
            random_element = log[0]

            if random_block_number != element[1] and (same_elements_diff_block + diff_elements_diff_block) < num_of_random_elements_to_be_compared:
                if random_element == element[0]:
                    same_elements_diff_block += 1
                else:
                    diff_elements_diff_block += 1

            block_logs = All_logs[element[1]].split(",")
            while len(block_logs) < 2:
                random_block_number = random.randint(0, len(All_logs) - 1)
                block_logs = All_logs[random_block_number].split(",")
            random_element_number = random.randint(0, len(block_logs) - 2)
            log = block_logs[random_element_number].split(" ")[:-1]
            random_element = log[0]

            if random_element_number != element[2] and (same_elements_same_block + diff_elements_same_block) < num_of_random_elements_to_be_compared:
                if random_element == element[0]:
                    same_elements_same_block += 1
                else:
                    diff_elements_same_block += 1

            if (same_elements_diff_block + diff_elements_diff_block) == num_of_random_elements_to_be_compared and (same_elements_same_block + diff_elements_same_block) == num_of_random_elements_to_be_compared:
                element_result_list.append((element, same_elements_same_block, same_elements_diff_block))
                flag = 1


    print("\nAddress blockchain frequency test for", num_of_elements, "elements (random compared elements:", num_of_random_elements_to_be_compared,") in dataset",dataset)
    print("Total same block hits:      ", total_same_block_hits)
    print("Total different block hits: ", total_diff_block_hits)


def Topics_blockchain_frequency_test(num_of_elements: int, dataset: tuple):
    Starting_block, Ending_block = dataset

    File_Logs = open(global_path + "Scrap Blockchain Database/Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_Logs.close()


    random.seed(0)
    element_list = []
    for element_num in range(num_of_elements):

        random_block_number = random.randint(0,len(All_logs) - 1)

        block_logs = All_logs[random_block_number].split(",")
        while len(block_logs) < 2:
            random_block_number = random.randint(0, len(All_logs) - 1)
            block_logs = All_logs[random_block_number].split(",")

        random_element_number = random.randint(0,len(block_logs) - 2)

        log = block_logs[random_element_number].split(" ")[1:-1]

        element = random.choice(log)

        element_list.append((element,random_block_number, random_element_number))


    element_result_list = []
    total_same_block_hits = 0
    total_diff_block_hits = 0
    num_of_random_elements_to_be_compared = 100

    same_elements_diff_block = 0
    same_elements_same_block = 0
    for element in element_list:
        flag = 0
        total_same_block_hits += same_elements_same_block
        total_diff_block_hits += same_elements_diff_block
        same_elements_diff_block = 0
        diff_elements_diff_block = 0
        same_elements_same_block = 0
        diff_elements_same_block = 0

        while flag == 0:
            random_block_number = random.randint(0, len(All_logs) - 1)
            block_logs = All_logs[random_block_number].split(",")
            while len(block_logs) < 2:
                random_block_number = random.randint(0, len(All_logs) - 1)
                block_logs = All_logs[random_block_number].split(",")
            random_element_number = random.randint(0, len(block_logs) - 2)
            log = block_logs[random_element_number].split(" ")[1:-1]
            random_element = random.choice(log)

            if random_block_number != element[1] and (same_elements_diff_block + diff_elements_diff_block) < num_of_random_elements_to_be_compared:
                if random_element == element[0]:
                    same_elements_diff_block += 1
                else:
                    diff_elements_diff_block += 1

            block_logs = All_logs[element[1]].split(",")
            while len(block_logs) < 2:
                random_block_number = random.randint(0, len(All_logs) - 1)
                block_logs = All_logs[random_block_number].split(",")
            random_element_number = random.randint(0, len(block_logs) - 2)
            log = block_logs[random_element_number].split(" ")[1:-1]
            random_element = random.choice(log)

            if random_element_number != element[2] and (same_elements_same_block + diff_elements_same_block) < num_of_random_elements_to_be_compared:
                if random_element == element[0]:
                    same_elements_same_block += 1
                else:
                    diff_elements_same_block += 1

            if (same_elements_diff_block + diff_elements_diff_block) == num_of_random_elements_to_be_compared and (same_elements_same_block + diff_elements_same_block) == num_of_random_elements_to_be_compared:
                element_result_list.append((element, same_elements_same_block, same_elements_diff_block))
                flag = 1

    print("\nTopics blockchain frequency test for",num_of_elements, "elements (random compared elements:",num_of_random_elements_to_be_compared,") in dataset",dataset)
    print("Total same block hits:      ", total_same_block_hits)
    print("Total different block hits: ", total_diff_block_hits)


def False_positive_rate_test(Scrap_database: tuple):
    Starting_block, Ending_block = Scrap_database

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Group blockchain Method1 Dataset/"
    path3 = global_path + "Group blockchain Method2 Dataset/"
    path4 = global_path + "Group blockchain Method3 Dataset/"
    path5 = global_path + "Group blockchain Method4 Dataset/"


    File_Trad_BloomFilters = open(path1 + "Bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group4_M1_BloomFilters = open(path2 + "[4]M1 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group4_M2_BloomFilters = open(path3 + "[4]M2 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group4_M3_BloomFilters = open(path4 + "[4]M3 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group4_M4_BloomFilters = open(path5 + "[4]M4 Group bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")


    Trad_bfs = File_Trad_BloomFilters.readlines()
    Group4_M1_bfs = File_Group4_M1_BloomFilters.readlines()
    Group4_M2_bfs = File_Group4_M2_BloomFilters.readlines()
    Group4_M3_bfs = File_Group4_M3_BloomFilters.readlines()
    Group4_M4_bfs = File_Group4_M4_BloomFilters.readlines()

    trad_bf_ones = 0
    group4_M1_bf_ones = 0
    group4_M2_bf_ones = 0
    group4_M3_bf_ones = 0
    group4_M4_bf_ones = 0


    for num in range(len(Trad_bfs)):
        trad_bloom_filter = BloomFilter(int(Trad_bfs[num]))
        for element in bin(trad_bloom_filter):
            if element == "1":
                trad_bf_ones += 1

    for bloom_filter in Group4_M1_bfs:
        group4_M1_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(group4_M1_bloom_filter):
            if element == "1":
                group4_M1_bf_ones += 1

    for bloom_filter in Group4_M2_bfs:
        group4_M2_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(group4_M2_bloom_filter):
            if element == "1":
                group4_M2_bf_ones += 1

    for bloom_filter in Group4_M3_bfs:
        group4_M3_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(group4_M3_bloom_filter):
            if element == "1":
                group4_M3_bf_ones += 1

    for bloom_filter in Group4_M4_bfs:
        group4_M4_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(group4_M4_bloom_filter):
            if element == "1":
                group4_M4_bf_ones += 1



    print("Traditional Bloom Filter one bits: ", trad_bf_ones, "  | ", "%.2f" % (trad_bf_ones/((Ending_block-Starting_block)*20.48)), "%")
    print("Group4 M1 Bloom Filter one bits  : ", group4_M1_bf_ones, "  | ", "%.2f" % (group4_M1_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("Group4 M2 Bloom Filter one bits  : ", group4_M2_bf_ones, "  | ", "%.2f" % (group4_M2_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("Group4 M3 Bloom Filter one bits  : ", group4_M3_bf_ones, "  | ", "%.2f" % (group4_M3_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("Group4 M4 Bloom Filter one bits  : ", group4_M4_bf_ones, "  | ", "%.2f" % (group4_M4_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("\nAll bits:                          ",(Ending_block-Starting_block)*2048)


def Mean_number_of_topics(dataset:tuple):
    Starting_block, Ending_block = dataset

    File_Logs = open(global_path + "Scrap Blockchain Database/Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_Logs.close()

    num_of_topics_list = []
    num_of_logs = 0

    for block_number in range(len(All_logs)):
        block_logs = All_logs[block_number].split(",")

        for log in block_logs:
            if log != "\n":
                num_of_logs += 1
                elements = log.split(" ")

                num_of_topics = len(elements[1:-1])
                num_of_topics_list.append(num_of_topics)

    num_of_one_topic_logs   = len([i for i in num_of_topics_list if i == 1])
    num_of_two_topic_logs   = len([i for i in num_of_topics_list if i == 2])
    num_of_three_topic_logs = len([i for i in num_of_topics_list if i == 3])
    num_of_four_topic_logs  = len([i for i in num_of_topics_list if i == 4])

    print("Statistics for dataset (",Starting_block, "-", Ending_block,")")
    print("Number of one topic logs:  ", num_of_one_topic_logs)
    print("Number of two topic logs:  ", num_of_two_topic_logs)
    print("Number of three topic logs:", num_of_three_topic_logs)
    print("Number of four topic logs: ", num_of_four_topic_logs)
    print("Total number of logs:      ", num_of_logs)
