from Crypto.Hash import keccak
from eth_bloom import BloomFilter
import time
import matplotlib.pyplot as plt
import random
import numpy as np
from real_Ethereum_data_functions import Log_Retrieval_bloom_filter_Offline, Log_Retrieval_brute_force_Offline
from arithmetic_compressor import AECompressor
from arithmetic_compressor.models import StaticModel


##  Parameters  ##
global_path = your_path


## ## Dataset creation functions ##  ##
def Create_DTI_M1_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M1 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M1 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M1 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = BloomFilter()

    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []


        for log in block_logs:
            if log != "\n":
                elements = log.split(" ")

                DTI_element_list = []

                DTI_element_list.append(elements[0])
                bloom_filter.add(bytes.fromhex(elements[0][2:]))

                for element in elements[1:-1]:
                    DTI_topic = elements[0] + element[2:]

                    DTI_element_list.append(DTI_topic)
                    bloom_filter.add(bytes.fromhex(DTI_topic[2:]))


                DTI_log = ""
                for element in DTI_element_list:
                    DTI_log += element + " "

                DTI_log += elements[-1]

                DTI_block_logs.append(DTI_log)


        Bloom_Filter_write.write(str(int(bloom_filter)) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = BloomFilter()


def Create_DTI_M2_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M2 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M2 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M2 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = BloomFilter()

    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []


        for log in block_logs:
            if log != "\n":
                elements = log.split(" ")

                DTI_element_list = []

                DTI_element_list.append(elements[0])
                bloom_filter.add(bytes.fromhex(elements[0][2:]))

                topics = elements[1:-1]

                for i in range(len(topics)):
                    DTI_topic = "0x"
                    for topic in topics:
                        DTI_topic += topic[2:]
                    DTI_element_list.append(DTI_topic)
                    bloom_filter.add(bytes.fromhex(DTI_topic[2:]))

                    first_element = topics.pop(0)
                    topics.append(first_element)


                DTI_log = ""
                for element in DTI_element_list:
                    DTI_log += element + " "

                DTI_log += elements[-1]

                DTI_block_logs.append(DTI_log)


        Bloom_Filter_write.write(str(int(bloom_filter)) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = BloomFilter()


def Create_DTI_M3_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M3 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M3 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M3 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = BloomFilter()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":
                DTI_log = ""
                elements = log.split(" ")

                address_plus_topics = "0x"
                for element in elements[:-1]:
                    address_plus_topics += element[2:]

                bloom_filter.add(bytes.fromhex(address_plus_topics[2:]))
                DTI_log += address_plus_topics + " "


                for topic in elements[1:-1]:
                    DTI_log += topic + " "
                    bloom_filter.add(bytes.fromhex(topic[2:]))

                DTI_log += elements[-1]

                DTI_block_logs.append(DTI_log)


        Bloom_Filter_write.write(str(int(bloom_filter)) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = BloomFilter()


def Create_DTI_M4_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M4 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M4 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M4 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M4()

    a = 0

    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":
                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]])

                DTI_block_logs.append(log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        a += bloom_filter.a
        bloom_filter = Bloom_filter_DTI_M4()
    print(a)


def Create_DTI_M5_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M5 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M5 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M5 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M5()

    a = 0

    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":
                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]])

                DTI_block_logs.append(log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        a += bloom_filter.a
        bloom_filter = Bloom_filter_DTI_M5()
    print(a)


def Create_DTI_M6_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M6 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M6 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M6 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M6()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":

                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]])

                address_plus_topics = "0x"
                for element in elements[:-1]:
                    address_plus_topics += element[2:]

                DTI_log = ""
                for element in [address_plus_topics] + elements[1:-1]:
                    DTI_log += element + " "
                DTI_log += elements[-1]

                DTI_block_logs.append(DTI_log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = Bloom_filter_DTI_M6()


def Create_DTI_M7_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M7 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M7 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M7 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M7()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":

                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]])

                address_plus_topics = "0x"
                for element in elements[:-1]:
                    address_plus_topics += element[2:]

                DTI_log = ""
                for element in [address_plus_topics] + elements[1:-1]:
                    DTI_log += element + " "
                DTI_log += elements[-1]

                DTI_block_logs.append(DTI_log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = Bloom_filter_DTI_M7()


def Create_DTI_M8_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M8 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M8 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M8 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M8()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":

                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]])

                address_plus_topics = elements[0]
                for topic in elements[1:-1]:
                    address_plus_topics += topic[2:]


                DTI_log = address_plus_topics + " "

                DTI_log += elements[-1]

                DTI_block_logs.append(DTI_log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = Bloom_filter_DTI_M8()


def Create_DTI_M9_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M9 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M9 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M9 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M9()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":

                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]])

                address_plus_topics = elements[0]
                for topic in elements[1:-1]:
                    address_plus_topics += topic[2:]


                DTI_log = address_plus_topics + " "

                DTI_log += elements[-1]

                DTI_block_logs.append(DTI_log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = Bloom_filter_DTI_M9()


def Create_DTI_M10_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M10 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M10 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M10 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M10()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":

                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]])

                address_plus_topics = "0x"
                for element in elements[:-1]:
                    address_plus_topics += element[2:]

                DTI_log = ""
                for element in [address_plus_topics] + elements[1:-1]:
                    DTI_log += element + " "
                DTI_log += elements[-1]

                DTI_block_logs.append(DTI_log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = Bloom_filter_DTI_M10()


def Create_DTI_M11_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M11 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M11 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M11 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M11()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":

                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]], bytes.fromhex(elements[-1][2:]))

                address_plus_topics = "0x"
                for element in elements:
                    address_plus_topics += element[2:]

                DTI_log = ""
                for element in [address_plus_topics] + elements[1:]:
                    DTI_log += element + " "

                DTI_block_logs.append(DTI_log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = Bloom_filter_DTI_M11()


def Create_DTI_M12_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M12 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M12 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M12 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M12()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":

                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]], bytes.fromhex(elements[-1][2:]))

                address_plus_topics = "0x"
                for element in elements:
                    address_plus_topics += element[2:]

                DTI_log = ""
                for element in [address_plus_topics] + [elements[-1]]:
                    DTI_log += element + " "

                DTI_block_logs.append(DTI_log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = Bloom_filter_DTI_M12()


def Create_DTI_M13_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M13 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M13 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M13 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M13()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":

                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]], bytes.fromhex(elements[-1][2:]))

                address_plus_topics = "0x"
                for element in elements:
                    address_plus_topics += element[2:]

                DTI_log = ""
                for element in [address_plus_topics] + [elements[-1]]:
                    DTI_log += element + " "

                DTI_block_logs.append(DTI_log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = Bloom_filter_DTI_M13()


def Create_DTI_M14_BF_from_Scraped_data(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M14 blockchain Dataset/"

    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    Logs_write = open(path2 + "DTI M14 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")
    Bloom_Filter_write = open(path2 + "DTI M14 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "w")

    bloom_filter = Bloom_filter_DTI_M14()


    for block_number in range(len(All_logs_pile)):
        print(block_number)
        block_logs = All_logs_pile[block_number].split(",")
        DTI_block_logs = []

        for log in block_logs:
            if log != "\n":

                elements = log.split(" ")

                bloom_filter.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]], bytes.fromhex(elements[-1][2:]))

                address_plus_topics = "0x"
                for element in elements:
                    address_plus_topics += element[2:]

                DTI_log = ""
                for element in [address_plus_topics] + [elements[-1]]:
                    DTI_log += element + " "

                DTI_block_logs.append(DTI_log)

        Bloom_Filter_write.write(str(bloom_filter.int_form()) + "\n")

        write_logs = ""
        for log in DTI_block_logs:
            write_logs += log + ","
        Logs_write.write(write_logs + "\n")

        bloom_filter = Bloom_filter_DTI_M14()




##  ##  Log Retrieval functions ##  ##
def Log_Retrieval_DTI_M1_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M1 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M1 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()

    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0
    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = BloomFilter(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        topic_flag = 1
        for i in range(len(topics)):
            if bytes.fromhex(address[2:] + topics[i][2:]) not in DTI_bloom_filter:
                topic_flag = 0
                break

        if bytes.fromhex(address[2:]) in DTI_bloom_filter:
            if topic_flag:
                list_of_positive_bfs.append(block_number)
                num_of_blocks_checked += 1
                block_logs = All_logs[block_number].split(",")
                for count, log in enumerate(block_logs):
                    log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                    if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                        if topics == log[1:-1]:
                            if transactionHash == "none":
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count)
                                # results.append((block_number,count2))
                                # break
                            elif transactionHash == log[-1]:
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count)
                                # results.append((block_number,count2))
                                # break
                    if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M2_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M2 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M2 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()

    alternating_topics = topics
    DTI_topics = []
    for i in range(len(alternating_topics)):
        DTI_topic = "0x"
        for topic in alternating_topics:
            DTI_topic += topic[2:]
        DTI_topics.append(DTI_topic)

        first_element = alternating_topics.pop(0)
        alternating_topics.append(first_element)


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0
    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = BloomFilter(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        topic_flag = 1
        for i in range(len(topics)):
            if bytes.fromhex(DTI_topics[i][2:]) not in DTI_bloom_filter:
                topic_flag = 0
                break

        if bytes.fromhex(address[2:]) in DTI_bloom_filter:
            if topic_flag:
                list_of_positive_bfs.append(block_number)
                num_of_blocks_checked += 1
                block_logs = All_logs[block_number].split(",")
                for count, log in enumerate(block_logs):
                    log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                    if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                        if topics == log[1:-1]:
                            if transactionHash == "none":
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count)
                                # results.append((block_number,count2))
                                # break
                            elif transactionHash == log[-1]:
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count)
                                # results.append((block_number,count2))
                                # break
                    if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M3_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M3 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M3 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()

    address_plus_topics = address

    for topic in topics:
        address_plus_topics += topic[2:]


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0
    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = BloomFilter(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        topic_flag = 1
        for i in range(len(topics)):
            if bytes.fromhex(topics[i][2:]) not in DTI_bloom_filter:
                topic_flag = 0
                break

        if bytes.fromhex(address_plus_topics[2:]) in DTI_bloom_filter:
            if topic_flag:
                list_of_positive_bfs.append(block_number)
                num_of_blocks_checked += 1
                block_logs = All_logs[block_number].split(",")
                for count, log in enumerate(block_logs):
                    log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                    if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                        if topics == log[1:-1]:
                            if transactionHash == "none":
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count)
                                # results.append((block_number,count2))
                                # break
                            elif transactionHash == log[-1]:
                                blocks_of_found_element.append(block_number)
                                positions_of_found_element_in_block.append(count)
                                # results.append((block_number,count2))
                                # break
                    if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M4_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M4 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M4 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M4(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics]):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M5_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M5 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M5 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M5(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics]):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M6_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M6 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M6 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M6(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics]):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M7_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M7 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M7 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M7(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics]):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M8_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M8 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M8 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M8(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics]):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M9_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M9 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M9 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M9(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics]):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M10_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M10 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M10 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M10(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics]):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M11_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M11 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M11 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M11(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics], bytes.fromhex(transactionHash[2:])):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M12_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M12 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M12 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M12(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics], bytes.fromhex(transactionHash[2:])):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M13_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M13 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M13 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M13(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics], bytes.fromhex(transactionHash[2:])):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)


def Log_Retrieval_DTI_M14_bloom_filter(address: str, topics: list, Starting_block: int, Ending_block: int,  transactionHash:str="none") -> None:

    time1 = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M14 blockchain Dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_Group_BloomFilters = open(path2 + "DTI M14 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()
    File_group_bloom_filter = File_Group_BloomFilters.readlines()

    time2 = time.time()


    blocks_of_found_element = []
    positions_of_found_element_in_block = []
    list_of_positive_bfs = []
    num_of_bfs_checked = 0
    num_of_blocks_checked = 0


    for block_number in range(Ending_block - Starting_block):

        DTI_bloom_filter = Bloom_filter_DTI_M14(int(File_group_bloom_filter[block_number]))

        num_of_bfs_checked += 1

        if DTI_bloom_filter.check_log(bytes.fromhex(address[2:]), [bytes.fromhex(topic[2:]) for topic in topics], bytes.fromhex(transactionHash[2:])):

            list_of_positive_bfs.append(block_number)
            num_of_blocks_checked += 1
            block_logs = All_logs[block_number].split(",")
            for count, log in enumerate(block_logs):
                log = log.split(" ")  ##  log = [ address, topic1, topic2, topic3, topic4, transactionHash]
                if address == log[0]:  ##  the number of topics is 0,1,2,3 or 4
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count)
                            # results.append((block_number,count2))
                            # break
                if (transactionHash != "none") & (blocks_of_found_element != []): break
        if (transactionHash != "none") & (blocks_of_found_element != []): break


    time3 = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, time3 - time1, (num_of_blocks_checked, num_of_bfs_checked, list_of_positive_bfs)




##  ##  Bloom filters  ##  ##
class Bloom_filter_DTI_M4():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics):

        k = keccak.new(digest_bits=256)
        k.update(address)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]
        one_bits_list = pair_list

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]

        for topic in topics:
            flag = 0
            count = 0
            while flag == 0:
                self.a += 1
                k = keccak.new(digest_bits=256)
                k.update(topic)
                hash = k.hexdigest()

                pair1 = int(bytes(hash[count:count+4], 'utf-8'), 16) % 2048
                pair2 = int(bytes(hash[count+4:count+8], 'utf-8'), 16) % 2048
                pair3 = int(bytes(hash[count+8:count+12], 'utf-8'), 16) % 2048
                pair_list = [pair1, pair2, pair3]

                count += 12
                flag = 1
                for pair in pair_list:
                    if pair in one_bits_list:
                        flag = 0
            self.a -= 1
            for pair in pair_list:
                one_bits_list.append(pair)
                inv_pair = 2047 - pair
                self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]


    def check_log(self, address, topics):

        all_logs_one_bits = []

        k = keccak.new(digest_bits=256)
        k.update(address)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]
        one_bits_list = pair_list

        for pair in pair_list:
            inv_pair = 2047 - pair
            all_logs_one_bits.append(inv_pair)


        for topic in topics:
            flag = 0
            count = 0
            while flag == 0:
                k = keccak.new(digest_bits=256)
                k.update(topic)
                hash = k.hexdigest()

                pair1 = int(bytes(hash[count:count + 4], 'utf-8'), 16) % 2048
                pair2 = int(bytes(hash[count + 4:count + 8], 'utf-8'), 16) % 2048
                pair3 = int(bytes(hash[count + 8:count + 12], 'utf-8'), 16) % 2048
                pair_list = [pair1, pair2, pair3]

                count += 12
                flag = 1
                for pair in pair_list:
                    if pair in one_bits_list:
                        flag = 0

            for pair in pair_list:
                one_bits_list.append(pair)
                inv_pair = 2047 - pair
                all_logs_one_bits.append(inv_pair)

        flag = True
        for index in all_logs_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M5():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics):
        one_bits_list = []

        address_topics_list = topics + [address]

        for element in address_topics_list:
            flag = 0
            count = 0
            while flag == 0:
                self.a += 1
                k = keccak.new(digest_bits=256)
                k.update(element)
                hash = k.hexdigest()

                pair1 = int(bytes(hash[count:count+4], 'utf-8'), 16) % 2048
                pair2 = int(bytes(hash[count+4:count+8], 'utf-8'), 16) % 2048
                pair3 = int(bytes(hash[count+8:count+12], 'utf-8'), 16) % 2048
                pair_list = [pair1, pair2, pair3]

                count += 12
                flag = 1
                for pair in pair_list:
                    if pair in one_bits_list:
                        flag = 0
            self.a -= 1
            for pair in pair_list:
                one_bits_list.append(pair)
                inv_pair = 2047 - pair
                self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]



    def check_log(self, address, topics):

        all_logs_one_bits = []
        one_bits_list = []
        address_topics_list = topics + [address]

        for element in address_topics_list:
            flag = 0
            count = 0
            while flag == 0:
                k = keccak.new(digest_bits=256)
                k.update(element)
                hash = k.hexdigest()

                pair1 = int(bytes(hash[count:count + 4], 'utf-8'), 16) % 2048
                pair2 = int(bytes(hash[count + 4:count + 8], 'utf-8'), 16) % 2048
                pair3 = int(bytes(hash[count + 8:count + 12], 'utf-8'), 16) % 2048
                pair_list = [pair1, pair2, pair3]

                count += 12
                flag = 1
                for pair in pair_list:
                    if pair in one_bits_list:
                        flag = 0

            for pair in pair_list:
                one_bits_list.append(pair)
                inv_pair = 2047 - pair
                all_logs_one_bits.append(inv_pair)


        flag = True
        for index in all_logs_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M6():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics):

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]

        for topic in topics:
            k = keccak.new(digest_bits=256)
            k.update(topic)
            hash = k.hexdigest()

            pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
            # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
            pair_list = [pair1, pair2]

            for pair in pair_list:
                inv_pair = 2047 - pair
                self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]



    def check_log(self, address, topics):
        all_one_bits = []

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            all_one_bits.append(inv_pair)

        for topic in topics:
            k = keccak.new(digest_bits=256)
            k.update(topic)
            hash = k.hexdigest()

            pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
            # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
            pair_list = [pair1, pair2]

            for pair in pair_list:
                inv_pair = 2047 - pair
                all_one_bits.append(inv_pair)

        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M7():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics):

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]

        for topic in topics:
            k = keccak.new(digest_bits=256)
            k.update(topic)
            hash = k.hexdigest()

            pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
            # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
            pair_list = [pair1, pair2]

            for pair in pair_list:
                inv_pair = 2047 - pair
                self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]



    def check_log(self, address, topics):
        all_one_bits = []

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2]

        for pair in pair_list:
            inv_pair = 2047 - pair
            all_one_bits.append(inv_pair)

        for topic in topics:
            k = keccak.new(digest_bits=256)
            k.update(topic)
            hash = k.hexdigest()

            pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
            # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
            pair_list = [pair1, pair2]

            for pair in pair_list:
                inv_pair = 2047 - pair
                all_one_bits.append(inv_pair)

        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M8():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics):

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        # DTI_element_list.append(address)
        # print(DTI_element_list)
        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]


        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]




    def check_log(self, address, topics):
        all_one_bits = []

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        # DTI_element_list.append(address)
        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            all_one_bits.append(inv_pair)

        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M9():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics):

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        # DTI_element_list.append(address)
        # print(DTI_element_list)
        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3, pair4]


        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]


    def check_log(self, address, topics):
        all_one_bits = []

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        # DTI_element_list.append(address)
        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3, pair4]

        for pair in pair_list:
            inv_pair = 2047 - pair
            all_one_bits.append(inv_pair)

        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M10():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics):

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        # DTI_element_list.append(address)
        # print(DTI_element_list)
        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        for i in range(len(topics)-1):
            pair_list.append(int(bytes(hash[((i*4)+12):((i*4)+16)], 'utf-8'), 16) % 2048)


        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]




    def check_log(self, address, topics):
        all_one_bits = []

        address_plus_topics = address
        for topic in topics:
            address_plus_topics += topic

        # DTI_element_list.append(address)
        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        for i in range(len(topics)-1):
            pair_list.append(int(bytes(hash[((i*4)+12):((i*4)+16)], 'utf-8'), 16) % 2048)

        for pair in pair_list:
            inv_pair = 2047 - pair
            all_one_bits.append(inv_pair)

        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M11():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics, transactionHash):

        address_plus_topics = address
        for topic in topics + [transactionHash]:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]

        for topic in topics:
            k = keccak.new(digest_bits=256)
            k.update(topic)
            hash = k.hexdigest()

            pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
            # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
            pair_list = [pair1, pair2]

            for pair in pair_list:
                inv_pair = 2047 - pair
                self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]



    def check_log(self, address, topics, transactionHash):
        all_one_bits = []

        address_plus_topics = address
        for topic in topics + [transactionHash]:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            all_one_bits.append(inv_pair)

        for topic in topics:
            k = keccak.new(digest_bits=256)
            k.update(topic)
            hash = k.hexdigest()

            pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
            # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
            pair_list = [pair1, pair2]

            for pair in pair_list:
                inv_pair = 2047 - pair
                all_one_bits.append(inv_pair)

        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M12():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics, transactionHash):

        address_plus_topics = address
        for topic in topics + [transactionHash]:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]



    def check_log(self, address, topics, transactionHash):
        all_one_bits = []

        address_plus_topics = address
        for topic in topics + [transactionHash]:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            all_one_bits.append(inv_pair)


        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M13():
    def __init__(self, initialized_value:int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(2048)

        self.a = 0

    def add(self,element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = 2047 - pair
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics, transactionHash):

        address_plus_topics = address
        for topic in topics + [transactionHash]:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        if len(topics) > 2:
            k = keccak.new(digest_bits=256)
            k.update(topics[2])
            hash = k.hexdigest()

            pair4 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair5 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair_list.append(pair4)
            pair_list.append(pair5)

        for pair in pair_list:
            inv_pair = 2047 - pair
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]



    def check_log(self, address, topics, transactionHash):
        all_one_bits = []

        address_plus_topics = address
        for topic in topics + [transactionHash]:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % 2048
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % 2048
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % 2048
        pair_list = [pair1, pair2, pair3]

        if len(topics) > 2:
            k = keccak.new(digest_bits=256)
            k.update(topics[2])
            hash = k.hexdigest()

            pair4 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair5 = int(bytes(hash[0:4], 'utf-8'), 16) % 2048
            pair_list.append(pair4)
            pair_list.append(pair5)


        for pair in pair_list:
            inv_pair = 2047 - pair
            all_one_bits.append(inv_pair)


        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


class Bloom_filter_DTI_M14():
    def __init__(self, initialized_value:int = 0):
        self.m = 6000
        self.k = 1
        self.value = str(bin(initialized_value))[2:].zfill(self.m)

        self.a = 0

    def add(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % self.m
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % self.m

        pair_list = [pair1, pair2, pair3]

        for pair in pair_list:
            inv_pair = self.m - pair - 1
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        k = keccak.new(digest_bits=256)
        k.update(element)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
        pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % self.m
        pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % self.m

        pair_list = [pair1, pair2, pair3]

        flag = True
        for pair in pair_list:
            inv_pair = self.m - pair - 1
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self,address, topics, transactionHash):

        address_plus_topics = address
        for topic in topics + [transactionHash]:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        # k = self.k
        # if len(topics) > 2:
        #     k = 2

        pair_list = []
        for i in range(self.k):
            pair = int(bytes(hash[i*4:i*4 + 4], 'utf-8'), 16) % self.m
            pair_list.append(pair)

        # pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
        # pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % self.m
        # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % self.m
        # # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % self.m
        # pair_list = [pair1, pair2, pair3]


        for pair in pair_list:
            inv_pair = self.m - pair - 1
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair + 1:]



    def check_log(self, address, topics, transactionHash):
        all_one_bits = []

        address_plus_topics = address
        for topic in topics + [transactionHash]:
            address_plus_topics += topic

        k = keccak.new(digest_bits=256)
        k.update(address_plus_topics)
        hash = k.hexdigest()

        # k = self.k
        # if len(topics) > 2:
        #     k = 2

        pair_list = []
        for i in range(self.k):
            pair = int(bytes(hash[i*4:i*4 + 4], 'utf-8'), 16) % self.m
            pair_list.append(pair)

        # pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
        # pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % self.m
        # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % self.m
        # # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % self.m
        # pair_list = [pair1, pair2, pair3]


        for pair in pair_list:
            inv_pair = self.m - pair - 1
            all_one_bits.append(inv_pair)

        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag


    def compressed_form(self, one_prob):

        model = StaticModel({'0': 1 - one_prob, '1': one_prob})
        coder = AECompressor(model)

        compressed_form = coder.compress(self.value)

        compressed_value = ""
        for element in compressed_form:
            compressed_value += str(element)

        return compressed_value




##  ##  False Positive Analysis Tests  ##  ##
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


def False_positive_analysis_DTI_M1(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M1 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M1 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    DTI_topics = []


    for topic in topics:
        DTI_topics.append(address + topic[2:])

    given_log_elements = [address] + DTI_topics


    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                for given_element_num in range(len(given_log_elements)):
                    if element == given_log_elements[given_element_num]:
                        result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M2(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M2 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M2 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    DTI_topics = []


    alternating_topics = topics
    for i in range(len(topics)):
        DTI_topic = "0x"
        for topic in alternating_topics:
            DTI_topic += topic[2:]
        DTI_topics.append(DTI_topic)

        first_element = alternating_topics.pop(0)
        alternating_topics.append(first_element)


    given_log_elements = [address] + DTI_topics

    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                for given_element_num in range(len(given_log_elements)):
                    if element == given_log_elements[given_element_num]:
                        result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M3(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M3 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M3 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    DTI_topics = []

    address_plus_topics = address

    for topic in topics:
        address_plus_topics += topic[2:]


    given_log_elements = [address_plus_topics] + DTI_topics

    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                for given_element_num in range(len(given_log_elements)):
                    if element == given_log_elements[given_element_num]:
                        result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M4(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    return 0, 0


def False_positive_analysis_DTI_M5(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    return 0, 0


def False_positive_analysis_DTI_M6(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M6 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M6 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    DTI_topics = topics

    address_plus_topics = address

    for topic in topics:
        address_plus_topics += topic[2:]


    given_log_elements = [address_plus_topics] + DTI_topics

    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                for given_element_num in range(len(given_log_elements)):
                    if element == given_log_elements[given_element_num]:
                        result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M7(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M7 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M7 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()


    address_plus_topics = address
    for topic in topics:
        address_plus_topics += topic[2:]


    given_log_elements = [address_plus_topics] + topics


    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]
        i = 0
        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]
            i += 1
            for element in elements:
                for given_element_num in range(len(given_log_elements)):
                    if element == given_log_elements[given_element_num]:
                        result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M8(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M8 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M8 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()


    address_plus_topics = address
    for topic in topics:
        address_plus_topics += topic[2:]


    given_log_elements = address_plus_topics

    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result = 0

        for log in block_logs[:-1]:
            elements = log.split(" ")

            if given_log_elements == elements[0]:
                result = 1


        if result == 0:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M9(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M9 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M9 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()


    address_plus_topics = address
    for topic in topics:
        address_plus_topics += topic[2:]


    given_log_elements = address_plus_topics

    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result = 0
        for log in block_logs[:-1]:
            elements = log.split(" ")

            if given_log_elements == elements[0]:
                result = 1


        if result == 0:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M10(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M10 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M10 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()


    address_plus_topics = address
    for topic in topics:
        address_plus_topics += topic[2:]

    given_log_elements = [address_plus_topics] + topics


    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                for given_element_num in range(len(given_log_elements)):
                    if element == given_log_elements[given_element_num]:
                        result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M11(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M11 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M11 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    DTI_topics = topics

    address_plus_topics = address

    for topic in topics + [transactionHash]:
        address_plus_topics += topic[2:]


    given_log_elements = [address_plus_topics] + DTI_topics

    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                for given_element_num in range(len(given_log_elements)):
                    if element == given_log_elements[given_element_num]:
                        result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M12(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M12 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M12 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    DTI_topics = topics

    address_plus_topics = address

    for topic in topics + [transactionHash]:
        address_plus_topics += topic[2:]


    given_log_elements = [address_plus_topics]

    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                for given_element_num in range(len(given_log_elements)):
                    if element == given_log_elements[given_element_num]:
                        result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M13(address, topics, transactionHash, positive_bfs:list, dataset:tuple):

    Starting_block, Ending_block = dataset
    path1 = global_path + "DTI M13 blockchain Dataset/"


    File_Logs = open(path1 +"DTI M13 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()
    File_Logs.close()

    DTI_topics = topics

    address_plus_topics = address

    for topic in topics + [transactionHash]:
        address_plus_topics += topic[2:]


    given_log_elements = [address_plus_topics]

    justified_fp = 0
    compressed_fp = 0

    for block_num in positive_bfs[:-1]:
        block_logs = All_logs_pile[block_num].split(",")

        result_list = [0 for i in range(len(given_log_elements))]

        for log in block_logs[:-1]:
            elements = log.split(" ")[:-1]

            for element in elements:
                for given_element_num in range(len(given_log_elements)):
                    if element == given_log_elements[given_element_num]:
                        result_list[given_element_num] = 1

        if 0 in result_list:
            compressed_fp += 1
        else:
            justified_fp += 1

    return justified_fp, compressed_fp


def False_positive_analysis_DTI_M14(address, topics, transactionHash, positive_bfs:list, dataset:tuple):
    # The compressed dti method produces no justified false positives, so the false positive analysis in meaningless
    return 0, 0




##  ##  Log Retrieval Test  ##  ##
def Log_Retrieval_Random_TopicBased_Bloom_Brute_DTI_plot(Number_of_logs_to_check: int, Scrap_database: tuple, Method_number: int, print_fp_analysis = True, show_plot = False):
    # The first argument that is required is the number of logs to check.
    # The second argument is the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database.
    # The Method_number: This refers to the dti method to be tested
    # The available methods with their coding are: DTI Method 1.1 -> 1, DTI Method 1.2 -> 2, DTI Method 1.3 -> 3, DTI Method 1.4 -> 8
    #                                              DTI Method 2.1 -> 6, DTI Method 2.2 -> 7
    #                                              DTI Method 3.1 -> 11, DTI Method 3.2 -> 12, DTI Method 3.3 -> 13
    #                                              Compressed DTI -> 14
    # create_all_plots: if True, the plots that are created are blocks checked and false positive analysis
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
        DTI_Log_Retrieval = Log_Retrieval_DTI_M1_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M1
        Method_code = "DTI_M1.1"
    elif Method_number == 2:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M2_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M2
        Method_code = "DTI_M1.2"
    elif Method_number == 3:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M3_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M3
        Method_code = "DTI_M1.3"
    elif Method_number == 4:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M4_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M4
        print_fp_analysis = False
        Method_code = "DTI_Not in thesis_4" # Not in thesis
    elif Method_number == 5:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M5_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M5
        print_fp_analysis = False
        Method_code = "DTI_Not in thesis_5"
    elif Method_number == 6:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M6_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M6
        Method_code = "DTI_M2.1"
    elif Method_number == 7:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M7_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M7
        Method_code = "DTI_M2.2"
    elif Method_number == 8:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M8_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M8
        Method_code = "DTI_M1.4"
    elif Method_number == 9:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M9_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M9
        Method_code = "DTI_Not in thesis_9"
    elif Method_number == 10:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M10_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M10
        Method_code = "DTI_Not in thesis_10"
    elif Method_number == 11:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M11_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M11
        Method_code = "DTI_M3.1"
    elif Method_number == 12:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M12_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M12
        Method_code = "DTI_M3.2"
    elif Method_number == 13:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M13_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M13
        Method_code = "DTI_M3.3"
    elif Method_number == 14:
        DTI_Log_Retrieval = Log_Retrieval_DTI_M14_bloom_filter
        DTI_False_positive_analysis = False_positive_analysis_DTI_M14
        print_fp_analysis = False
        Method_code = "Compressed DTI"


    ##  ##  Data Selection  ##  ##
    ##  Existing log selection  ##

    # one_topic_logs,two_topic_logs, three_topic_logs are the 1,2,3 topic logs that are randomly selected to be queried
    one_topic_logs = []
    two_topic_logs = []
    three_topic_logs = []
    four_topic_logs = []

    random.seed(0)

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

    # The following variables refer to the the blocks checked plot
    one_topic_bloom_blocks_checked, two_topic_bloom_blocks_checked, three_topic_bloom_blocks_checked, four_topic_bloom_blocks_checked, total_bloom_blocks_checked = ([], 0), ([], 0), ([], 0), ([], 0), ([], 0)
    one_topic_brute_blocks_checked, two_topic_brute_blocks_checked, three_topic_brute_blocks_checked, four_topic_brute_blocks_checked, total_brute_blocks_checked = 0, 0, 0, 0, 0
    one_topic_DTI_blocks_checked, two_topic_DTI_blocks_checked, three_topic_DTI_blocks_checked, four_topic_DTI_blocks_checked, total_DTI_blocks_checked = (0, 0, []), (0, 0, []), (0, 0, []), (0, 0, []), (0, 0, [])

    # The following variables refer to the false positive analysis plot
    total_bloom_justified_fp = 0
    total_bloom_compressed_fp = 0
    total_DTI_justified_fp = 0
    total_DTI_compressed_fp = 0


    for log in one_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        justified_fp, compressed_fp = False_positive_analysis_bloom_filter(log[0], log[1:-2], bloom_blocks_checked[0], (Starting_block, Ending_block))
        total_bloom_justified_fp += justified_fp
        total_bloom_compressed_fp += compressed_fp

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,                                                    transactionHash=log[-2])

        block, position, dti_time, dti_blocks_checked = DTI_Log_Retrieval(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        justified_fp, compressed_fp = DTI_False_positive_analysis(log[0], log[1:-2], log[-1], dti_blocks_checked[2], (Starting_block, Ending_block))
        total_DTI_justified_fp += justified_fp
        total_DTI_compressed_fp += compressed_fp

        one_topic_bloom_blocks_checked = tuple([one_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(one_topic_bloom_blocks_checked))])
        one_topic_brute_blocks_checked = one_topic_brute_blocks_checked + block[0] + 1
        one_topic_DTI_blocks_checked = tuple([one_topic_DTI_blocks_checked[i] + dti_blocks_checked[i] for i in range(len(one_topic_DTI_blocks_checked))])


    for log in two_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        justified_fp, compressed_fp = False_positive_analysis_bloom_filter(log[0], log[1:-2], bloom_blocks_checked[0], (Starting_block, Ending_block))
        total_bloom_justified_fp += justified_fp
        total_bloom_compressed_fp += compressed_fp

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, dti_time, dti_blocks_checked = DTI_Log_Retrieval(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        justified_fp, compressed_fp = DTI_False_positive_analysis(log[0], log[1:-2], log[-1], dti_blocks_checked[2], (Starting_block, Ending_block))
        total_DTI_justified_fp += justified_fp
        total_DTI_compressed_fp += compressed_fp

        two_topic_bloom_blocks_checked = tuple([two_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(two_topic_bloom_blocks_checked))])
        two_topic_brute_blocks_checked = two_topic_brute_blocks_checked + block[0] + 1
        two_topic_DTI_blocks_checked = tuple([two_topic_DTI_blocks_checked[i] + dti_blocks_checked[i] for i in range(len(two_topic_DTI_blocks_checked))])


    for log in three_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        justified_fp, compressed_fp = False_positive_analysis_bloom_filter(log[0], log[1:-2], bloom_blocks_checked[0], (Starting_block, Ending_block))
        total_bloom_justified_fp += justified_fp
        total_bloom_compressed_fp += compressed_fp

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, dti_time, dti_blocks_checked = DTI_Log_Retrieval(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        justified_fp, compressed_fp = DTI_False_positive_analysis(log[0], log[1:-2], log[-1], dti_blocks_checked[2], (Starting_block, Ending_block))
        total_DTI_justified_fp += justified_fp
        total_DTI_compressed_fp += compressed_fp

        three_topic_bloom_blocks_checked = tuple([three_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(three_topic_bloom_blocks_checked))])
        three_topic_brute_blocks_checked = three_topic_brute_blocks_checked + block[0] + 1
        three_topic_DTI_blocks_checked = tuple([three_topic_DTI_blocks_checked[i] + dti_blocks_checked[i] for i in range(len(three_topic_DTI_blocks_checked))])


    for log in four_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        justified_fp, compressed_fp = False_positive_analysis_bloom_filter(log[0], log[1:-2], bloom_blocks_checked[0], (Starting_block, Ending_block))
        total_bloom_justified_fp += justified_fp
        total_bloom_compressed_fp += compressed_fp

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, dti_time, dti_blocks_checked = DTI_Log_Retrieval(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        justified_fp, compressed_fp = DTI_False_positive_analysis(log[0], log[1:-2], log[-1], dti_blocks_checked[2], (Starting_block, Ending_block))
        total_DTI_justified_fp += justified_fp
        total_DTI_compressed_fp += compressed_fp

        four_topic_bloom_blocks_checked = tuple([four_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(four_topic_bloom_blocks_checked))])
        four_topic_brute_blocks_checked = four_topic_brute_blocks_checked + block[0] + 1
        four_topic_DTI_blocks_checked = tuple([four_topic_DTI_blocks_checked[i] + dti_blocks_checked[i] for i in range(len(four_topic_DTI_blocks_checked))])


    total_bloom_blocks_checked = tuple([one_topic_bloom_blocks_checked[i] + two_topic_bloom_blocks_checked[i] + three_topic_bloom_blocks_checked[i] + four_topic_bloom_blocks_checked[i] for i in range(len(one_topic_bloom_blocks_checked))])
    total_brute_blocks_checked = one_topic_brute_blocks_checked + two_topic_brute_blocks_checked + three_topic_brute_blocks_checked + four_topic_brute_blocks_checked
    total_DTI_blocks_checked = tuple([one_topic_DTI_blocks_checked[i] + two_topic_DTI_blocks_checked[i] + three_topic_DTI_blocks_checked[i] + four_topic_DTI_blocks_checked[i] for i in range(len(one_topic_DTI_blocks_checked))])


    print("Blocks checked reduction Bloom filter-", Method_code," :", round((100 * (len(total_bloom_blocks_checked[0]) - total_DTI_blocks_checked[0])) / (len(total_bloom_blocks_checked[0])), 2), "%")
    end = time.time()
    print("Total execution time of Log retrieval Position based comparison is: ",time.strftime("%H:%M:%S", time.gmtime(end - start)))

    # ##  ##  Plot  ##  ##
    x = np.arange(5)

    bloom_blocks_checked_measurments = [len(one_topic_bloom_blocks_checked[0]), len(two_topic_bloom_blocks_checked[0]), len(three_topic_bloom_blocks_checked[0]), len(four_topic_bloom_blocks_checked[0]), len(total_bloom_blocks_checked[0])]
    brute_blocks_checked_measurments = [one_topic_brute_blocks_checked, two_topic_brute_blocks_checked, three_topic_brute_blocks_checked, four_topic_brute_blocks_checked, total_brute_blocks_checked]
    group16_blocks_checked_measurments = [one_topic_DTI_blocks_checked[0], two_topic_DTI_blocks_checked[0], three_topic_DTI_blocks_checked[0], four_topic_DTI_blocks_checked[0], total_DTI_blocks_checked[0]]

    width = 0.25
    plt.figure().set_size_inches(14,5)

    # plot data in grouped manner of bar type
    plt.bar(x - width, bloom_blocks_checked_measurments, width, color='darkgoldenrod')
    plt.bar(x , brute_blocks_checked_measurments, width, color='cadetblue')
    plt.bar(x + width, group16_blocks_checked_measurments, width, color='darkmagenta')

    plt.xticks(x, ['One topic logs','Two topic logs','Three topic logs','Four topic logs' ,'Total logs'])

    plt.ylabel("Number of blocks checked")
    bottom, top = plt.ylim()
    plt.ylim(bottom, 1.5*top)
    text = 'Total logs:   '+ str(Number_of_logs_to_check) + '\n1 topic logs: '+str(len(one_topic_logs))+'\n2 topic logs: '+str(len(two_topic_logs)) + '\n3 topic logs: '+str(len(three_topic_logs)) + '\n4 topic logs: '+str(len(four_topic_logs))
    plt.text(-1.5 * width, 1.5 * max([max(brute_blocks_checked_measurments), max(bloom_blocks_checked_measurments), max(group16_blocks_checked_measurments)]), text, ha='left', va='top', fontsize=10)
    plt.legend(["Bloom filter", "Brute force", Method_code],loc='upper right')
    plt.title('Blocks Checked based on number of topics ('+str(Starting_block)+" - "+str(Ending_block)+")")

    number_size = 9
    for i, v in enumerate(bloom_blocks_checked_measurments):
        plt.text( i - width, v + 0.02*top, v, ha="center", color='black', fontsize=number_size)

    for i, v in enumerate(brute_blocks_checked_measurments):
        plt.text( i , v + 0.02*top, v, ha="center", color='black', fontsize=number_size)

    for i, v in enumerate(group16_blocks_checked_measurments):
        plt.text( i + width, v + 0.02*top, v, ha="center", color='black', fontsize=number_size)

    plt.savefig(path + "DTI plots/Blocks Checked BlF-BrF-" + Method_code + "(" + str(Number_of_logs_to_check) + ", " + str(Starting_block) + ").jpg", bbox_inches= 'tight') # , dpi= 500, bbox_inches= 'tight'
    if show_plot:
        plt.show()
    else:
        plt.close()


    # False positive type plot
    if print_fp_analysis:
        justified_measurments = [total_bloom_justified_fp, total_DTI_justified_fp]
        compressed_measurments = [total_bloom_compressed_fp, total_DTI_compressed_fp]

        x = np.arange(2)

        width = 0.25

        # plot data in grouped manner of bar type
        plt.bar(x - width*0.5, justified_measurments, width, color='darkviolet')
        plt.bar(x + width*0.5, compressed_measurments, width, color='forestgreen')

        plt.xticks(x, ['Bloom filter', Method_code])
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

        plt.savefig(path + "DTI plots/TB False positive analysis BlF-BrF-" + Method_code + "(" + str(Number_of_logs_to_check) + ", " + str(Starting_block) + ").jpg")
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
    # print("AFL", address_freq_list)

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
    # ax.legend(title='Fruit color')

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

        # element = random.choice(log)
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
            # random_element = random.choice(log)
            random_element = log[0]

            if random_element_number != element[2] and (same_elements_same_block + diff_elements_same_block) < num_of_random_elements_to_be_compared:
                if random_element == element[0]:
                    same_elements_same_block += 1
                else:
                    diff_elements_same_block += 1

            if (same_elements_diff_block + diff_elements_diff_block) == num_of_random_elements_to_be_compared and (same_elements_same_block + diff_elements_same_block) == num_of_random_elements_to_be_compared:
                element_result_list.append((element, same_elements_same_block, same_elements_diff_block))
                flag = 1
        # print("Next element")

    # [print(i[1], "    ", i[2]) for i in element_result_list]

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
        # print("Next element")

    # [print(i[1], "    ", i[2]) for i in element_result_list]

    print("\nTopics blockchain frequency test for",num_of_elements, "elements (random compared elements:",num_of_random_elements_to_be_compared,") in dataset",dataset)
    print("Total same block hits:      ", total_same_block_hits)
    print("Total different block hits: ", total_diff_block_hits)


def False_positive_rate_test(Scrap_database: tuple):
    Starting_block, Ending_block = Scrap_database

    path1 = global_path + "Scrap Blockchain Database/"
    path6 = global_path + "DTI M1 blockchain Dataset/"
    path7 = global_path + "DTI M2 blockchain Dataset/"
    path8 = global_path + "DTI M3 blockchain Dataset/"
    path9 = global_path + "DTI M4 blockchain Dataset/"
    path10 = global_path + "DTI M5 blockchain Dataset/"
    path11 = global_path + "DTI M6 blockchain Dataset/"
    path12 = global_path + "DTI M7 blockchain Dataset/"
    path13 = global_path + "DTI M8 blockchain Dataset/"
    path14 = global_path + "DTI M9 blockchain Dataset/"
    path15 = global_path + "DTI M10 blockchain Dataset/"
    path16 = global_path + "DTI M11 blockchain Dataset/"
    path17 = global_path + "DTI M12 blockchain Dataset/"
    path18 = global_path + "DTI M13 blockchain Dataset/"
    path19 = global_path + "DTI M14 blockchain Dataset/"



    File_Trad_BloomFilters = open(path1 + "Bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M1_BloomFilters = open(path6 + "DTI M1 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M2_BloomFilters = open(path7 + "DTI M2 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M3_BloomFilters = open(path8 + "DTI M3 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M4_BloomFilters = open(path9 + "DTI M4 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M5_BloomFilters = open(path10 + "DTI M5 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M6_BloomFilters = open(path11 + "DTI M6 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M7_BloomFilters = open(path12 + "DTI M7 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M8_BloomFilters = open(path13 + "DTI M8 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M9_BloomFilters = open(path14 + "DTI M9 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M10_BloomFilters = open(path15 + "DTI M10 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M11_BloomFilters = open(path16 + "DTI M11 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M12_BloomFilters = open(path17 + "DTI M12 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M13_BloomFilters = open(path18 + "DTI M13 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    File_DTI_M14_BloomFilters = open(path19 + "DTI M14 bloom filters for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")


    Trad_bfs = File_Trad_BloomFilters.readlines()
    DTI_M1_bfs = File_DTI_M1_BloomFilters.readlines()
    DTI_M2_bfs = File_DTI_M2_BloomFilters.readlines()
    DTI_M3_bfs = File_DTI_M3_BloomFilters.readlines()
    DTI_M4_bfs = File_DTI_M4_BloomFilters.readlines()
    DTI_M5_bfs = File_DTI_M5_BloomFilters.readlines()
    DTI_M6_bfs = File_DTI_M6_BloomFilters.readlines()
    DTI_M7_bfs = File_DTI_M7_BloomFilters.readlines()
    DTI_M8_bfs = File_DTI_M8_BloomFilters.readlines()
    DTI_M9_bfs = File_DTI_M9_BloomFilters.readlines()
    DTI_M10_bfs = File_DTI_M10_BloomFilters.readlines()
    DTI_M11_bfs = File_DTI_M11_BloomFilters.readlines()
    DTI_M12_bfs = File_DTI_M12_BloomFilters.readlines()
    DTI_M13_bfs = File_DTI_M13_BloomFilters.readlines()
    DTI_M14_bfs = File_DTI_M14_BloomFilters.readlines()



    trad_bf_ones = 0
    DTI_M1_bf_ones = 0
    DTI_M2_bf_ones = 0
    DTI_M3_bf_ones = 0
    DTI_M4_bf_ones = 0
    DTI_M5_bf_ones = 0
    DTI_M6_bf_ones = 0
    DTI_M7_bf_ones = 0
    DTI_M8_bf_ones = 0
    DTI_M9_bf_ones = 0
    DTI_M10_bf_ones = 0
    DTI_M11_bf_ones = 0
    DTI_M12_bf_ones = 0
    DTI_M13_bf_ones = 0
    DTI_M14_bf_ones = 0




    for num in range(len(Trad_bfs)):
        trad_bloom_filter = BloomFilter(int(Trad_bfs[num]))
        for element in bin(trad_bloom_filter):
            if element == "1":
                trad_bf_ones += 1


    for bloom_filter in DTI_M1_bfs:
        DTI_M1_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M1_bloom_filter):
            if element == "1":
                DTI_M1_bf_ones += 1

    for bloom_filter in DTI_M2_bfs:
        DTI_M2_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M2_bloom_filter):
            if element == "1":
                DTI_M2_bf_ones += 1

    for bloom_filter in DTI_M3_bfs:
        DTI_M3_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M3_bloom_filter):
            if element == "1":
                DTI_M3_bf_ones += 1

    for bloom_filter in DTI_M4_bfs:
        DTI_M4_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M4_bloom_filter):
            if element == "1":
                DTI_M4_bf_ones += 1

    for bloom_filter in DTI_M5_bfs:
        DTI_M5_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M5_bloom_filter):
            if element == "1":
                DTI_M5_bf_ones += 1

    for bloom_filter in DTI_M6_bfs:
        DTI_M6_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M6_bloom_filter):
            if element == "1":
                DTI_M6_bf_ones += 1

    for bloom_filter in DTI_M7_bfs:
        DTI_M7_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M7_bloom_filter):
            if element == "1":
                DTI_M7_bf_ones += 1

    for bloom_filter in DTI_M8_bfs:
        DTI_M8_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M8_bloom_filter):
            if element == "1":
                DTI_M8_bf_ones += 1

    for bloom_filter in DTI_M9_bfs:
        DTI_M9_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M9_bloom_filter):
            if element == "1":
                DTI_M9_bf_ones += 1

    for bloom_filter in DTI_M10_bfs:
        DTI_M10_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M10_bloom_filter):
            if element == "1":
                DTI_M10_bf_ones += 1

    for bloom_filter in DTI_M11_bfs:
        DTI_M11_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M11_bloom_filter):
            if element == "1":
                DTI_M11_bf_ones += 1

    for bloom_filter in DTI_M12_bfs:
        DTI_M12_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M12_bloom_filter):
            if element == "1":
                DTI_M12_bf_ones += 1

    for bloom_filter in DTI_M13_bfs:
        DTI_M13_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M13_bloom_filter):
            if element == "1":
                DTI_M13_bf_ones += 1

    for bloom_filter in DTI_M14_bfs:
        DTI_M14_bloom_filter = BloomFilter(int(bloom_filter))
        for element in bin(DTI_M14_bloom_filter):
            if element == "1":
                DTI_M14_bf_ones += 1
    bf = Bloom_filter_DTI_M14()


    print("Traditional Bloom Filter one bits: ", trad_bf_ones, "  | ", "%.2f" % (trad_bf_ones/((Ending_block-Starting_block)*20.48)), "%")
    print("DTI M1 Bloom Filter one bits     : ", DTI_M1_bf_ones, "  | ", "%.2f" % (DTI_M1_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M2 Bloom Filter one bits     : ", DTI_M2_bf_ones, "  | ", "%.2f" % (DTI_M2_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M3 Bloom Filter one bits     : ", DTI_M3_bf_ones, "  | ", "%.2f" % (DTI_M3_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M4 Bloom Filter one bits     : ", DTI_M4_bf_ones, "  | ", "%.2f" % (DTI_M4_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M5 Bloom Filter one bits     : ", DTI_M5_bf_ones, "  | ", "%.2f" % (DTI_M5_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M6 Bloom Filter one bits     : ", DTI_M6_bf_ones, "  | ", "%.2f" % (DTI_M6_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M7 Bloom Filter one bits     : ", DTI_M7_bf_ones, "  | ", "%.2f" % (DTI_M7_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M8 Bloom Filter one bits     : ", DTI_M8_bf_ones, "  | ", "%.2f" % (DTI_M8_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M9 Bloom Filter one bits     : ", DTI_M9_bf_ones, "  | ", "%.2f" % (DTI_M9_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M10 Bloom Filter one bits     : ", DTI_M10_bf_ones, "  | ", "%.2f" % (DTI_M10_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M11 Bloom Filter one bits     : ", DTI_M11_bf_ones, "  | ", "%.2f" % (DTI_M11_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M12 Bloom Filter one bits     : ", DTI_M12_bf_ones, "  | ", "%.2f" % (DTI_M12_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M13 Bloom Filter one bits     : ", DTI_M13_bf_ones, "  | ", "%.2f" % (DTI_M13_bf_ones / ((Ending_block - Starting_block) * 20.48)), "%")
    print("DTI M14 Bloom Filter one bits     : ", DTI_M14_bf_ones, "  | ", "%.2f" % (DTI_M14_bf_ones / ((Ending_block - Starting_block) * (bf.m / 100))), "%")


    print("\nAll bits:                          ",(Ending_block-Starting_block)*2048)


def Log_Uniqueness_analysis(Starting_block: int, Ending_block: int) -> None:

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DTI M2 blockchain Dataset/"
    path3 = global_path + "DTI M3 blockchain Dataset/"


    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    DTI_M2_File_Logs = open(path2 +"DTI M2 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    DTI_M3_File_Logs = open(path3 +"DTI M3 logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    DTI_M2_all_logs_pile = DTI_M2_File_Logs.readlines()
    DTI_M3_all_logs_pile = DTI_M3_File_Logs.readlines()

    total_elements = 0
    total_addresses = 0

    trad_block_list = []
    sum_of_trad_unique_count = 0
    for block_number in range(len(All_logs_pile)):
        block_logs = All_logs_pile[block_number].split(",")
        for log in block_logs:
            elements = log.split(" ")

            total_addresses += 1

            for element in elements[:-1]:
                total_elements += 1
                trad_block_list.append(element)

        trad_block_unique_count = len(set(trad_block_list))
        sum_of_trad_unique_count += trad_block_unique_count
        trad_block_list = []


    DTIM2_block_list = []
    sum_of_DTIM2_unique_count = 0
    for block_number in range(len(DTI_M2_all_logs_pile)):
        block_logs = DTI_M2_all_logs_pile[block_number].split(",")
        for log in block_logs:
            elements = log.split(" ")

            for element in elements[:-1]:
                DTIM2_block_list.append(element)

        DTIM2_block_unique_count = len(set(DTIM2_block_list))
        sum_of_DTIM2_unique_count += DTIM2_block_unique_count
        DTIM2_block_list = []



    DTIM3_block_list = []
    DTIM3_address_list = []
    DTIM3_topic_list = []
    sum_of_DTIM3_unique_count = 0
    sum_of_DTIM3_address_unique_count = 0
    sum_of_DTIM3_topic_unique_count = 0
    for block_number in range(len(DTI_M3_all_logs_pile)):
        block_logs = DTI_M3_all_logs_pile[block_number].split(",")
        for log in block_logs:
            elements = log.split(" ")

            DTIM3_address_list.append(elements[0])
            for element in elements[:-1]:
                DTIM3_block_list.append(element)
            DTIM3_topic_list = DTIM3_block_list[1:]

        DTIM3_block_unique_count = len(set(DTIM3_block_list))
        DTIM3_address_unique_count = len(set(DTIM3_address_list))
        DTIM3_topic_unique_count = len(set(DTIM3_topic_list))

        sum_of_DTIM3_unique_count += DTIM3_block_unique_count
        sum_of_DTIM3_address_unique_count += DTIM3_address_unique_count
        sum_of_DTIM3_topic_unique_count += DTIM3_topic_unique_count

        DTIM3_block_list = []
        DTIM3_address_list = []
        DTIM3_topic_list = []




    print("Results refer to (",Starting_block, "-", Ending_block,") dataset")
    print("Sum of unique elements count for traditional BF is:     ", sum_of_trad_unique_count)
    print("Sum of unique elements count for DTI Method2 is:        ", sum_of_DTIM2_unique_count)
    print("Sum of unique elements count for DTI Method3 is:        ", sum_of_DTIM3_unique_count)
    print("Sum of unique addresses+topics count for DTI Method3 is:", sum_of_DTIM3_address_unique_count)
    print("Sum of unique topics count for DTI Method3 is:          ", sum_of_DTIM3_topic_unique_count)
    print("Total elements in the dataset:                          ", total_elements)
    print("Total addresses in the dataset:                         ", total_addresses)
    print("Mean addresses per block:                               ", total_addresses/(Ending_block-Starting_block))


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


def Compressibility_test(dataset:tuple, one_prob):
    Starting_block, Ending_block = dataset

    path1 = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()


    total_compressed_length = 0
    total_uncompressed_length = 0
    for block_number in range(len(All_logs_pile)):
        bf = Bloom_filter_DTI_M14()
        for log in All_logs_pile[block_number].split(",")[:-1]:
            elements = log.split(" ")

            bf.add_log(bytes.fromhex(elements[0][2:]), [bytes.fromhex(topic[2:]) for topic in elements[1:-1]],bytes.fromhex(elements[-1][2:]))

        comp_length = len(bf.compressed_form(one_prob))
        uncomp_length = bf.m

        total_compressed_length += comp_length
        total_uncompressed_length += uncomp_length

    print("Compresibility test for dataset(", dataset, ") One prob:", one_prob)
    print("Number of one bits uncompressed: ", int(total_uncompressed_length / len(All_logs_pile)))
    print("Number of one bits compressed:   ", total_compressed_length / len(All_logs_pile))


def N_log_analysis(dataset: tuple):
    Starting_block, Ending_block = dataset

    path1 = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path1 +"Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")
    All_logs_pile = File_Logs.readlines()

    n_list = []
    nun_list = []  # non unique n
    log_num_list = []
    for block_number in range(len(All_logs_pile)):

        log_num_list.append((block_number, len(All_logs_pile[block_number].split(",")[:-1])))

        element_list = []
        for log in All_logs_pile[block_number].split(","):
            for element in log.split(" ")[:-1]:
                element_list.append(element)

        n_list.append((block_number, len(set(element_list))))
        nun_list.append((block_number, len(element_list)))

    log_num_list.sort(key=lambda x: x[1])
    nun_list.sort(key=lambda x: x[1])
    n_list.sort(key=lambda x: x[1])

    log_order = [x[0] for x in log_num_list]
    nun_order = [x[0] for x in nun_list]
    n_order = [x[0] for x in n_list]

    return log_order, nun_order, n_order


def False_positive_N_log_analysis(false_positive_bfs:list, log_order: list, nun_order: list, n_order: list):

    log_stats = [0, 0, 0, 0]
    nun_stats = [0, 0, 0, 0]
    n_stats = [0, 0, 0, 0]

    dataset_length = len(log_order)

    for block_number in false_positive_bfs:

        log_category = int((4 * log_order.index(block_number)) / dataset_length)
        nun_category = int((4 * nun_order.index(block_number)) / dataset_length)
        n_category = int((4 * n_order.index(block_number)) / dataset_length)

        log_stats[log_category] += 1
        nun_stats[nun_category] += 1
        n_stats[n_category] += 1

    return log_stats, nun_stats, n_stats


