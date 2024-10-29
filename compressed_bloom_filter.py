from Crypto.Hash import keccak
from eth_bloom import BloomFilter
from arithmetic_compressor import AECompressor
from arithmetic_compressor.models import StaticModel
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from real_Ethereum_data_functions import Log_Retrieval_bloom_filter_Offline, Log_Retrieval_brute_force_Offline
from arithmetic_compressor.models import BinaryPPM, MultiBinaryPPM
from arithmetic_compressor.models import BaseFrequencyTable, SimpleAdaptiveModel, ContextMix_Linear, ContextMix_Logistic
import statistics


##  Parameters  ##
global_path = your_path


##  ##  Dataset Creation functions  ##  ##
def Create_dynamic_compressed_bf_dataset(dataset:tuple):
    start = time.time()
    starting_block, ending_block = dataset

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DCBF dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(starting_block) + " to " + str(ending_block), "r")
    Bloom_filters = open(path1 + "Bloom filters for blocks " + str(starting_block) + " to " + str(ending_block), "r")
    File_Bloom_Filters_Write = open(path2 + "DCBFs for blocks " + str(starting_block) + " to " + str(ending_block), "w")

    All_logs_pile = File_Logs.readlines()
    Bloom_filters = Bloom_filters.readlines()

    for block_number in range(len(All_logs_pile)):
        print("block number: ", block_number)

        m, k, one_prob, (trad_bf_tfpr, cbf_tfpr) = Optimize_DCBF_fixed_z_k(dataset, block_number + starting_block)

        if cbf_tfpr < trad_bf_tfpr:
            bloom_filter = Universal_bloom_filter(m,k)

            for log in All_logs_pile[block_number].split(",")[:-1]:
                for element in log.split(" ")[:-1]:
                    bloom_filter.add(bytes.fromhex(element[2:]))

            overhead_bits = "11"
            overhead_bits += bin(m)[2:].zfill(15)
            overhead_bits += bin(k)[2:].zfill(2)
            overhead_bits += bin(int(round(one_prob*100, 0)))[2:].zfill(7)


            cbf_value = bloom_filter.compressed_AC_form(one_prob)

            bloom_filter_value = overhead_bits + cbf_value

        else:
            bloom_filter = BloomFilter(int(Bloom_filters[block_number]))

            bloom_filter_value = "10" + bin(bloom_filter)[2:]

        File_Bloom_Filters_Write.write(str(int(bloom_filter_value, 2)) + "\n")

    end = time.time()

    print("Execution time for the creation of dcbf dataset is: ", time.strftime("%H:%M:%S", time.gmtime(end - start)))


def Create_compressed_bf_dataset_M1(dataset):
    starting_block, ending_block = dataset

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Compressed M1 dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(starting_block) + " to " + str(ending_block), "r")
    File_Bloom_Filters_Write = open(path2 + "Compressed bfs for blocks " + str(starting_block) + " to " + str(ending_block), "w")

    All_logs_pile = File_Logs.readlines()


    for block_number in range(len(All_logs_pile)):
        print("block number:",block_number)
        bf = compessed_bloom_filter_M1()
        for log in All_logs_pile[block_number].split(",")[:-1]:
            for element in log.split(" ")[:-1]:
                bf.add(bytes.fromhex(element[2:]))
        File_Bloom_Filters_Write.write(str(bf.int_form()) + "\n")


def Optimize_DCBF_fixed_z_k(dataset:tuple, block:int):
    starting_block, ending_block = dataset

    path1 = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path1 +"Logs for blocks " + str(starting_block) + " to " + str(ending_block), "r")

    All_logs_pile = File_Logs.readlines()

    Block_logs = All_logs_pile[block-starting_block]

    k = 2
    m = 3000
    step = 50
    flag = 0
    iter = 0
    n = 0
    prev_direction = 3
    while flag == 0:
        iter += 1
        cbf = Universal_bloom_filter(m, k)


        block_elements_list = []
        for log in Block_logs.split(",")[:-1]:
            for element in log.split(" ")[:-1]:
                block_elements_list.append(element)
                cbf.add(bytes.fromhex(element[2:]))

        n = len(set(block_elements_list))

        cbf_ones = 0
        for element in cbf.value:
            if element == "1":
                cbf_ones += 1

        prob_of_ones = max(round((cbf_ones / m), 2), 0.01)

        z = len(cbf.compressed_BFT_form(prob_of_ones))

        if z > 2000:
            m = m - step
            future_direction = 0
        elif z < 1900:
            m = m + step
            future_direction = 1
        else:
            flag = 1
            break

        if prob_of_ones == 0.01:
            print("Minimum prob_of_ones at block: ", block - starting_block)
            flag = 1
            break

        if iter > 100:
            print("Over 100 at block: ", block - starting_block)
            flag = 1
            break

        if m > 32767 - step:
            print("Maximum bits for m reached at block: ", block - starting_block)
            flag = 1
            break

        if future_direction - prev_direction != 0 and iter != 1:
            step = max(5, int(step/2))

        prev_direction = future_direction


        # if iter % 10 == 9 and step >= 20:
        #     step -= 5

    theoretical_tradbf_fpr = (1-(1-(1/2048))**(3*n))**3
    theoretical_cbf_fpr = (1-(1-(1/m))**(k*n))**k

    #
    # print("Num of iterations:", iter)
    # print("m:", m)
    # print("z:", z)
    # print("Unique elements:", n)
    # print("One probability:", prob_of_ones)
    # print("Theoretical traditional bf false positive probability is: ", "%.2f" % (100*theoretical_tradbf_fpr), "%")
    # print("Theoretical compressed bf false positive probability is:  ", "%.2f" % (100*theoretical_cbf_fpr), "%")

    return m, k, prob_of_ones, (round((100*theoretical_tradbf_fpr), 2), round((100*theoretical_cbf_fpr), 2))




##  ##  Bloom filters  ##  ##
class Universal_bloom_filter():
    def __init__(self, m: int, k: int,  initialized_value: int = 0):
        self.value = str(bin(initialized_value))[2:].zfill(m)
        self.m = m
        self.k = k


    def add(self, element):
        kh = keccak.new(digest_bits=512)
        kh.update(element)
        hash = kh.hexdigest()

        pair_list = []
        for i in range(self.k):
            pair = int(bytes(hash[i*4:i*4+4], 'utf-8'), 16) % self.m

            pair_list.append(pair)


        for pair in pair_list:
            inv_pair = self.m - pair - 1
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        kh = keccak.new(digest_bits=512)
        kh.update(element)
        hash = kh.hexdigest()

        pair_list = []
        for i in range(self.k):
            pair = int(bytes(hash[i * 4:i * 4 + 4], 'utf-8'), 16) % self.m

            pair_list.append(pair)

        flag = True
        for pair in pair_list:
            inv_pair = self.m - pair - 1
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def add_log(self, address, topics, transactionHash):

        address_topics_trHash = address
        for topic in topics + [transactionHash]:
            address_topics_trHash += topic

        k = keccak.new(digest_bits=256)
        k.update(address_topics_trHash)
        hash = k.hexdigest()

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
        # pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % self.m
        # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % self.m
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % self.m
        pair_list = [pair1]

        if len(topics) > 2:
            pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % self.m
            pair_list.append(pair2)
            # k = keccak.new(digest_bits=256)
            # k.update(topics[2])
            # hash = k.hexdigest()
            #
            # pair4 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
            # # pair5 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
            # pair_list.append(pair4)
            # pair_list.append(pair5)

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

        pair1 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
        # pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % self.m
        # pair3 = int(bytes(hash[8:12], 'utf-8'), 16) % self.m
        # pair4 = int(bytes(hash[12:16], 'utf-8'), 16) % self.m
        pair_list = [pair1]

        if len(topics) > 2:
            pair2 = int(bytes(hash[4:8], 'utf-8'), 16) % self.m
            pair_list.append(pair2)
            # k = keccak.new(digest_bits=256)
            # k.update(topics[2])
            # hash = k.hexdigest()
            #
            # pair4 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
            # # pair5 = int(bytes(hash[0:4], 'utf-8'), 16) % self.m
            # pair_list.append(pair4)
            # pair_list.append(pair5)


        for pair in pair_list:
            inv_pair = self.m - pair - 1
            all_one_bits.append(inv_pair)


        flag = True
        for index in all_one_bits:
            if self.value[index] == "0":
                flag = False

        return flag



    def compressed_AC_form(self, one_prob):

        model = StaticModel({'0': 1 - one_prob, '1': one_prob})
        coder = AECompressor(model)

        compressed_form = coder.compress(self.value)

        compressed_value = ""
        for element in compressed_form:
            compressed_value += str(element)

        return compressed_value


    def compressed_BPPM_form(self, context_size):

        model = BinaryPPM(k = context_size)
        coder = AECompressor(model)

        compressed_form = coder.compress([int(i) for i in self.value])

        compressed_value = ""
        for element in compressed_form:
            compressed_value += str(element)

        return compressed_value


    def compressed_SAM_form(self, one_prob):

        model = SimpleAdaptiveModel({'0': 1 - one_prob, '1': one_prob})
        coder = AECompressor(model)

        compressed_form = coder.compress(self.value)

        compressed_value = ""
        for element in compressed_form:
            compressed_value += str(element)

        return compressed_value


    def compressed_BFT_form(self, one_prob):

        model = BaseFrequencyTable({'0': 1 - one_prob, '1': one_prob})
        coder = AECompressor(model)

        compressed_form = coder.compress(self.value)

        compressed_value = ""
        for element in compressed_form:
            compressed_value += str(element)

        return compressed_value


    def compressed_LinM_form(self, one_prob):

        model = ContextMix_Linear()
        # model = ContextMix_Linear([SimpleAdaptiveModel({0: 1 - one_prob, 1: one_prob}), BaseFrequencyTable({0: 1 - one_prob, 1: one_prob})])
        coder = AECompressor(model)

        compressed_form = coder.compress([int(i) for i in self.value])

        compressed_value = ""
        for element in compressed_form:
            compressed_value += str(element)

        return compressed_value


    def compressed_LogM_form(self):

        model = ContextMix_Logistic()
        coder = AECompressor(model)

        compressed_form = coder.compress([int(i) for i in self.value])

        compressed_value = ""
        for element in compressed_form:
            compressed_value += str(element)

        return compressed_value


class compessed_bloom_filter_M1():
    def __init__(self, initialized_value:int = 0):
        self.m = 5000
        self.k = 1
        self.value = str(bin(initialized_value))[2:].zfill(self.m)

    def add(self,element):
        kh = keccak.new(digest_bits=256)
        kh.update(element)
        hash = kh.hexdigest()

        pair_list = []
        for i in range(self.k):
            pair = int(bytes(hash[i*4:i*4+4], 'utf-8'), 16) % self.m

            pair_list.append(pair)


        for pair in pair_list:
            inv_pair = self.m - pair - 1
            self.value = self.value[:inv_pair] + "1" + self.value[inv_pair+1:]


    def check(self, element):
        kh = keccak.new(digest_bits=256)
        kh.update(element)
        hash = kh.hexdigest()

        pair_list = []
        for i in range(self.k):
            pair = int(bytes(hash[i * 4:i * 4 + 4], 'utf-8'), 16) % self.m

            pair_list.append(pair)

        flag = True
        for pair in pair_list:
            inv_pair = self.m - pair - 1
            if self.value[inv_pair] == "0":
                flag = False
        return flag


    def int_form(self):
        return int(self.value, 2)


    def compressed_form(self, one_prob):

        model = StaticModel({'0':1 - one_prob , '1': one_prob})
        coder = AECompressor(model)

        compressed_form = coder.compress(self.value)

        return compressed_form




##  ##  Log Retrieval  ##  ##
def Log_Retrieval_DCBF(address: str, topics: list, starting_block: int, ending_block: int,  transactionHash:str="none"):
    start = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "DCBF dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(starting_block) + " to " + str(ending_block), "r")
    DC_Bloom_filters = open(path2 + "DCBFs for blocks " + str(starting_block) + " to " + str(ending_block), "r")

    All_logs_pile = File_Logs.readlines()
    DC_Bloom_filters = DC_Bloom_filters.readlines()

    blocks_of_found_element = []
    positions_of_found_element_in_block = []

    blocks_checked_list = []
    num_of_bfs_checked = 0
    for block_number in range(len(All_logs_pile)):

        dcbf_line = bin(int(DC_Bloom_filters[block_number]))[2:]

        element_in_bf = True

        if dcbf_line[1] == "0":
            bloom_filter = BloomFilter(int(dcbf_line[2:], 2))
            if bytes.fromhex(address[2:]) not in bloom_filter:
                element_in_bf = False
            for topic in topics:
                if bytes.fromhex(topic[2:]) not in bloom_filter:
                    element_in_bf = False

        elif dcbf_line[1] == "1":
            m = int(dcbf_line[2:17], 2)
            k = int(dcbf_line[17:19], 2)
            one_prob = int(dcbf_line[19:26], 2) / 100

            model = StaticModel({'0': 1 - one_prob, '1': one_prob})
            coder = AECompressor(model)
            decompressed_bf_value = coder.decompress([int(i) for i in dcbf_line[26:]], m)

            decompressed_bf_value_string = ""
            for ele in decompressed_bf_value:
                decompressed_bf_value_string += str(ele)


            bloom_filter = Universal_bloom_filter(m, k, int(decompressed_bf_value_string, 2))
            if bloom_filter.check(bytes.fromhex(address[2:])) == False:
                element_in_bf = False
            for topic in topics:
                if bloom_filter.check(bytes.fromhex(topic[2:])) == False:
                    element_in_bf = False

        num_of_bfs_checked += 1

        if element_in_bf:
            block_logs = All_logs_pile[block_number].split(",")[:-1]
            blocks_checked_list.append(block_number)
            for count2, log in enumerate(block_logs):
                log = log.split(" ")
                if address == log[0]:
                    if topics == log[1:-1]:
                        if transactionHash == "none":
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count2)
                            # break
                        elif transactionHash == log[-1]:
                            blocks_of_found_element.append(block_number)
                            positions_of_found_element_in_block.append(count2)
                            # break
        if (transactionHash != "none") & (blocks_of_found_element != []): break
    end = time.time()

    return blocks_of_found_element, positions_of_found_element_in_block, end-start, (blocks_checked_list,num_of_bfs_checked)


def Log_Retrieval_Compressed_M1(address: str, topics: list, starting_block: int, ending_block: int,  transactionHash:str="none"):
    start = time.time()

    path1 = global_path + "Scrap Blockchain Database/"
    path2 = global_path + "Compressed M1 dataset/"

    File_Logs = open(path1 + "Logs for blocks " + str(starting_block) + " to " + str(ending_block), "r")
    Comp_Bloom_filters = open(path2 + "Compressed bfs for blocks " + str(starting_block) + " to " + str(ending_block), "r")

    All_logs_pile = File_Logs.readlines()
    Comp_Bloom_filters = Comp_Bloom_filters.readlines()

    blocks_of_found_element = []
    positions_of_found_element_in_block = []

    blocks_checked_list = []
    num_of_bfs_checked = 0

    for block_number in range(len(All_logs_pile)):
        # The block_logs list contains all the logs of one block
        block_logs = All_logs_pile[block_number].split(",")[:-1]

        bloom_filter = compessed_bloom_filter_M1(int(Comp_Bloom_filters[block_number]))

        num_of_bfs_checked += 1
        topic_flag = 1
        for topic in topics:
            if bloom_filter.check(bytes.fromhex(topic[2:])) == False:
                topic_flag = 0
                break

        if bloom_filter.check(bytes.fromhex(address[2:])):
            if topic_flag:
                blocks_checked_list.append(block_number)
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
    end = time.time()
    # print("|||")

    return blocks_of_found_element, positions_of_found_element_in_block, end-start, (blocks_checked_list,num_of_bfs_checked)





##  ##  Log Retrieval Tests  ##  ##
def Log_Retrieval_Random_TopicBased_Bloom_Brute_DCBF_plot(Number_of_logs_to_check: int, Scrap_database: tuple, show_plot = False):
    # The first argument that is required is the number of logs to check.
    # The second argument is the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database
    # show_plot: if True, the plot that is created is shown, If False no plot is shown
    # The database is the stored locally in the computer memory and it is retrieved from the database when
    # the Scrap_database variable is given
    start = time.time()
    print("Starting Time:", time.strftime("%H:%M:%S", time.gmtime(start)))
    Starting_block, Ending_block = Scrap_database
    path = global_path

    File_Logs = open(global_path + "Scrap Blockchain Database/Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()

    File_Logs.close()

    ##  ##  Data Selection  ##  ##

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
    one_topic_Comp_blocks_checked, two_topic_Comp_blocks_checked, three_topic_Comp_blocks_checked, four_topic_DTIM2_blocks_checked, total_Comp_blocks_checked = ([], 0), ([], 0), ([], 0), ([], 0), ([], 0)


    for log in one_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,                                                    transactionHash=log[-2])

        block, position, Comp_time, Comp_blocks_checked = Log_Retrieval_DCBF(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        one_topic_bloom_blocks_checked = tuple([one_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(one_topic_bloom_blocks_checked))])
        one_topic_brute_blocks_checked = one_topic_brute_blocks_checked + block[0] + 1
        one_topic_Comp_blocks_checked = tuple([one_topic_Comp_blocks_checked[i] + Comp_blocks_checked[i] for i in range(len(one_topic_Comp_blocks_checked))])


    # The bloom filter retrieval time for all the logs in the middle_logs list
    for log in two_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, Comp_time, Comp_blocks_checked = Log_Retrieval_DCBF(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        two_topic_bloom_blocks_checked = tuple([two_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(two_topic_bloom_blocks_checked))])
        two_topic_brute_blocks_checked = two_topic_brute_blocks_checked + block[0] + 1
        two_topic_Comp_blocks_checked = tuple([two_topic_Comp_blocks_checked[i] + Comp_blocks_checked[i] for i in range(len(two_topic_Comp_blocks_checked))])


    for log in three_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, Comp_time, Comp_blocks_checked = Log_Retrieval_DCBF(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        three_topic_bloom_blocks_checked = tuple([three_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(three_topic_bloom_blocks_checked))])
        three_topic_brute_blocks_checked = three_topic_brute_blocks_checked + block[0] + 1
        three_topic_Comp_blocks_checked = tuple([three_topic_Comp_blocks_checked[i] + Comp_blocks_checked[i] for i in range(len(three_topic_Comp_blocks_checked))])


    for log in four_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, Comp_time, Comp_blocks_checked = Log_Retrieval_DCBF(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        four_topic_bloom_blocks_checked = tuple([four_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(four_topic_bloom_blocks_checked))])
        four_topic_brute_blocks_checked = four_topic_brute_blocks_checked + block[0] + 1
        four_topic_DTIM2_blocks_checked = tuple([four_topic_DTIM2_blocks_checked[i] + Comp_blocks_checked[i] for i in range(len(four_topic_DTIM2_blocks_checked))])


    total_bloom_blocks_checked = tuple([one_topic_bloom_blocks_checked[i] + two_topic_bloom_blocks_checked[i] + three_topic_bloom_blocks_checked[i] + four_topic_bloom_blocks_checked[i] for i in range(len(one_topic_bloom_blocks_checked))])
    total_brute_blocks_checked = one_topic_brute_blocks_checked + two_topic_brute_blocks_checked + three_topic_brute_blocks_checked + four_topic_brute_blocks_checked
    total_Comp_blocks_checked = tuple([one_topic_Comp_blocks_checked[i] + two_topic_Comp_blocks_checked[i] + three_topic_Comp_blocks_checked[i] + four_topic_DTIM2_blocks_checked[i] for i in range(len(one_topic_Comp_blocks_checked))])


    print("Blocks checked reduction Bloom filter-DCBF :", round((100 * (len(total_bloom_blocks_checked[0]) - len(total_Comp_blocks_checked[0]))) / (len(total_bloom_blocks_checked[0])), 2), "%")
    end = time.time()
    print("Total execution time of Log retrieval Position based comparison is: ",time.strftime("%H:%M:%S", time.gmtime(end - start)))


    # ##  ##  Plot  ##  ##
    x = np.arange(5)

    bloom_blocks_checked_measurments = [len(one_topic_bloom_blocks_checked[0]), len(two_topic_bloom_blocks_checked[0]), len(three_topic_bloom_blocks_checked[0]), len(four_topic_bloom_blocks_checked[0]), len(total_bloom_blocks_checked[0])]
    brute_blocks_checked_measurments = [one_topic_brute_blocks_checked, two_topic_brute_blocks_checked, three_topic_brute_blocks_checked, four_topic_brute_blocks_checked, total_brute_blocks_checked]
    Comp_blocks_checked_measurments = [len(one_topic_Comp_blocks_checked[0]), len(two_topic_Comp_blocks_checked[0]), len(three_topic_Comp_blocks_checked[0]), len(four_topic_DTIM2_blocks_checked[0]), len(total_Comp_blocks_checked[0])]

    width = 0.2

    # plot data in grouped manner of bar type
    plt.bar(x - width, bloom_blocks_checked_measurments, width, color='darkgoldenrod')
    plt.bar(x , brute_blocks_checked_measurments, width, color='cadetblue')
    plt.bar(x + width, Comp_blocks_checked_measurments, width, color='darkmagenta')

    plt.xticks(x, ['One topic logs','Two topic logs','Three topic logs','Four topic logs' ,'Total logs'])

    plt.ylabel("Number of blocks checked")
    bottom, top = plt.ylim()
    plt.ylim(bottom, 1.5*top)
    text = 'Total logs:   '+ str(Number_of_logs_to_check) + '\n1 topic logs: '+str(len(one_topic_logs))+'\n2 topic logs: '+str(len(two_topic_logs)) + '\n3 topic logs: '+str(len(three_topic_logs)) + '\n4 topic logs: '+str(len(four_topic_logs))
    plt.text(-1.5 * width, 1.5 * max([max(brute_blocks_checked_measurments), max(bloom_blocks_checked_measurments), max(Comp_blocks_checked_measurments)]), text, ha='left', va='top', fontsize=10)
    plt.legend(["Bloom filter", "Brute force", "DCBF"],loc='upper right')
    plt.title('Blocks Checked based on number of topics ('+str(Starting_block)+" - "+str(Ending_block)+")")

    for i, v in enumerate(bloom_blocks_checked_measurments):
        plt.text( i - width, v + 0.02*top, v, ha="center", color='black')

    for i, v in enumerate(brute_blocks_checked_measurments):
        plt.text( i , v + 0.02*top, v, ha="center", color='black')

    for i, v in enumerate(Comp_blocks_checked_measurments):
        plt.text( i + width, v + 0.02*top, v, ha="center", color='black')


    plt.savefig(path + "CBF plots/Blocks Checked BlF-BrF-DCBF (" + str(Number_of_logs_to_check) + ", " + str(Starting_block) + ").jpg", bbox_inches= 'tight') # , dpi= 500, bbox_inches= 'tight'
    if show_plot:
        plt.show()
    else:
        plt.close()


def Log_Retrieval_Random_TopicBased_Bloom_Brute_CompBF_plot(Number_of_logs_to_check: int, Scrap_database: tuple, show_plot = False):
    # The first argument that is required is the number of logs to check.
    # The second argument is the Scrap database. This is given in the form of a tuple where the 1st position is the
    # starting block of the database and the 2nd position is the ending block of the database
    # show_plot: if True, the plot that is created is shown, If False no plot is shown
    # The database is the stored locally in the computer memory and it is retrieved from the database when
    # the Scrap_database variable is given
    start = time.time()
    print("Starting Time:", time.strftime("%H:%M:%S", time.gmtime(start)))
    Starting_block, Ending_block = Scrap_database
    path = global_path

    File_Logs = open(global_path + "Scrap Blockchain Database/Logs for blocks " + str(Starting_block) + " to " + str(Ending_block), "r")

    All_logs = File_Logs.readlines()

    File_Logs.close()

    ##  ##  Data Selection  ##  ##

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
    one_topic_Comp_blocks_checked, two_topic_Comp_blocks_checked, three_topic_Comp_blocks_checked, four_topic_DTIM2_blocks_checked, total_Comp_blocks_checked = ([], 0), ([], 0), ([], 0), ([], 0), ([], 0)


    for log in one_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,                                                    transactionHash=log[-2])

        block, position, Comp_time, Comp_blocks_checked = Log_Retrieval_Compressed_M1(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        one_topic_bloom_blocks_checked = tuple([one_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(one_topic_bloom_blocks_checked))])
        one_topic_brute_blocks_checked = one_topic_brute_blocks_checked + block[0] + 1
        one_topic_Comp_blocks_checked = tuple([one_topic_Comp_blocks_checked[i] + Comp_blocks_checked[i] for i in range(len(one_topic_Comp_blocks_checked))])


    # The bloom filter retrieval time for all the logs in the middle_logs list
    for log in two_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, Comp_time, Comp_blocks_checked = Log_Retrieval_Compressed_M1(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        two_topic_bloom_blocks_checked = tuple([two_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(two_topic_bloom_blocks_checked))])
        two_topic_brute_blocks_checked = two_topic_brute_blocks_checked + block[0] + 1
        two_topic_Comp_blocks_checked = tuple([two_topic_Comp_blocks_checked[i] + Comp_blocks_checked[i] for i in range(len(two_topic_Comp_blocks_checked))])


    for log in three_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, Comp_time, Comp_blocks_checked = Log_Retrieval_Compressed_M1(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        three_topic_bloom_blocks_checked = tuple([three_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(three_topic_bloom_blocks_checked))])
        three_topic_brute_blocks_checked = three_topic_brute_blocks_checked + block[0] + 1
        three_topic_Comp_blocks_checked = tuple([three_topic_Comp_blocks_checked[i] + Comp_blocks_checked[i] for i in range(len(three_topic_Comp_blocks_checked))])


    for log in four_topic_logs:
        block, position, bloom_time, bloom_blocks_checked = Log_Retrieval_bloom_filter_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, brute_time = Log_Retrieval_brute_force_Offline(log[0], log[1:-2], Starting_block, Ending_block,transactionHash=log[-2])

        block, position, Comp_time, Comp_blocks_checked = Log_Retrieval_Compressed_M1(log[0], log[1:-2], Starting_block, Ending_block, transactionHash=log[-2])

        four_topic_bloom_blocks_checked = tuple([four_topic_bloom_blocks_checked[i] + bloom_blocks_checked[i] for i in range(len(four_topic_bloom_blocks_checked))])
        four_topic_brute_blocks_checked = four_topic_brute_blocks_checked + block[0] + 1
        four_topic_DTIM2_blocks_checked = tuple([four_topic_DTIM2_blocks_checked[i] + Comp_blocks_checked[i] for i in range(len(four_topic_DTIM2_blocks_checked))])


    total_bloom_blocks_checked = tuple([one_topic_bloom_blocks_checked[i] + two_topic_bloom_blocks_checked[i] + three_topic_bloom_blocks_checked[i] + four_topic_bloom_blocks_checked[i] for i in range(len(one_topic_bloom_blocks_checked))])
    total_brute_blocks_checked = one_topic_brute_blocks_checked + two_topic_brute_blocks_checked + three_topic_brute_blocks_checked + four_topic_brute_blocks_checked
    total_Comp_blocks_checked = tuple([one_topic_Comp_blocks_checked[i] + two_topic_Comp_blocks_checked[i] + three_topic_Comp_blocks_checked[i] + four_topic_DTIM2_blocks_checked[i] for i in range(len(one_topic_Comp_blocks_checked))])


    print("Blocks checked reduction Bloom filter-CompBF :", round((100 * (len(total_bloom_blocks_checked[0]) - len(total_Comp_blocks_checked[0]))) / (len(total_bloom_blocks_checked[0])), 2), "%")
    end = time.time()
    print("Total execution time of Log retrieval Position based comparison is: ",time.strftime("%H:%M:%S", time.gmtime(end - start)))


    # ##  ##  Plot  ##  ##
    x = np.arange(5)

    bloom_blocks_checked_measurments = [len(one_topic_bloom_blocks_checked[0]), len(two_topic_bloom_blocks_checked[0]), len(three_topic_bloom_blocks_checked[0]), len(four_topic_bloom_blocks_checked[0]), len(total_bloom_blocks_checked[0])]
    brute_blocks_checked_measurments = [one_topic_brute_blocks_checked, two_topic_brute_blocks_checked, three_topic_brute_blocks_checked, four_topic_brute_blocks_checked, total_brute_blocks_checked]
    Comp_blocks_checked_measurments = [len(one_topic_Comp_blocks_checked[0]), len(two_topic_Comp_blocks_checked[0]), len(three_topic_Comp_blocks_checked[0]), len(four_topic_DTIM2_blocks_checked[0]), len(total_Comp_blocks_checked[0])]

    width = 0.2

    # plot data in grouped manner of bar type
    plt.bar(x - width, bloom_blocks_checked_measurments, width, color='darkgoldenrod')
    plt.bar(x , brute_blocks_checked_measurments, width, color='cadetblue')
    plt.bar(x + width, Comp_blocks_checked_measurments, width, color='darkmagenta')

    plt.xticks(x, ['One topic logs', 'Two topic logs', 'Three topic logs', 'Four topic logs', 'Total logs'])

    plt.ylabel("Number of blocks checked")
    bottom, top = plt.ylim()
    plt.ylim(bottom, 1.5*top)
    text = 'Total logs:   '+ str(Number_of_logs_to_check) + '\n1 topic logs: '+str(len(one_topic_logs))+'\n2 topic logs: '+str(len(two_topic_logs)) + '\n3 topic logs: '+str(len(three_topic_logs)) + '\n4 topic logs: '+str(len(four_topic_logs))
    plt.text(-1.5 * width, 1.5 * max([max(brute_blocks_checked_measurments), max(bloom_blocks_checked_measurments), max(Comp_blocks_checked_measurments)]), text, ha='left', va='top', fontsize=10)
    plt.legend(["Bloom filter", "Brute force", "Compressed BF"],loc='upper right')
    plt.title('Blocks Checked based on number of topics ('+str(Starting_block)+" - "+str(Ending_block)+")")

    for i, v in enumerate(bloom_blocks_checked_measurments):
        plt.text( i - width, v + 0.02*top, v, ha="center", color='black')

    for i, v in enumerate(brute_blocks_checked_measurments):
        plt.text( i , v + 0.02*top, v, ha="center", color='black')

    for i, v in enumerate(Comp_blocks_checked_measurments):
        plt.text( i + width, v + 0.02*top, v, ha="center", color='black')


    plt.savefig(path + "CBF plots/Blocks Checked BlF-BrF-CompBF (" + str(Number_of_logs_to_check) + ", " + str(Starting_block) + ").jpg", bbox_inches= 'tight') # , dpi= 500, bbox_inches= 'tight'
    if show_plot:
        plt.show()
    else:
        plt.close()






##  ##  Other Tests  ##  ##
def Space_statistics_CBF(dataset: tuple, m:int, k:int, Coding_Method="AC", context_size=None, prob_of_ones=None):
    start = time.time()
    starting_block, ending_block = dataset

    path1 = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path1 +"Logs for blocks " + str(starting_block) + " to " + str(ending_block), "r")
    Bloom_filters = open(path1 +"Bloom filters for blocks " + str(starting_block) + " to " + str(ending_block), "r")

    All_logs_pile = File_Logs.readlines()
    Bloom_filters = Bloom_filters.readlines()


    trad_bf_ones = 0
    comp_bf_ones = 0
    comp_bf_size = 0
    if Coding_Method == "All":
        AC_comp_bf_size, BPPM_comp_bf_size, SAM_comp_bf_size, BFT_comp_bf_size, LinM_comp_bf_size, LogM_comp_bf_size = 0, 0, 0, 0, 0, 0
        AC_comp_bf_size_list, SAM_comp_bf_size_list, BFT_comp_bf_size_list = [], [], []

    for block_num in range(len(All_logs_pile)):
        trad_bf = BloomFilter(int(Bloom_filters[block_num]))
        for element in bin(trad_bf):
            if element == "1":
                trad_bf_ones += 1

        comp_bf = Universal_bloom_filter(m, k)
        for log in All_logs_pile[block_num].split(",")[:-1]:
            for element in log.split(" ")[:-1]:
                comp_bf.add(bytes.fromhex(element[2:]))


        for element in comp_bf.value:
            if element == "1":
                comp_bf_ones += 1

        if Coding_Method == "AC":
            comp_bf_size += len(comp_bf.compressed_AC_form(prob_of_ones))
        elif Coding_Method == "BPPM":
            comp_bf_size += len(comp_bf.compressed_BPPM_form(context_size=context_size))
        elif Coding_Method == "SAM":
            comp_bf_size += len(comp_bf.compressed_SAM_form(prob_of_ones))
        elif Coding_Method == "BFT":
            comp_bf_size += len(comp_bf.compressed_BFT_form(prob_of_ones))
        elif Coding_Method == "LinM":
            comp_bf_size += len(comp_bf.compressed_LinM_form())
        elif Coding_Method == "LogM":
            comp_bf_size += len(comp_bf.compressed_LogM_form())
        elif Coding_Method == "All":
            AC_comp_bf_size += len(comp_bf.compressed_AC_form(prob_of_ones))
            AC_comp_bf_size_list.append(len(comp_bf.compressed_AC_form(prob_of_ones)))
            # BPPM_comp_bf_size += len(comp_bf.compressed_BPPM_form(context_size=context_size))
            SAM_comp_bf_size += len(comp_bf.compressed_SAM_form(prob_of_ones))
            SAM_comp_bf_size_list.append(len(comp_bf.compressed_SAM_form(prob_of_ones)))
            BFT_comp_bf_size += len(comp_bf.compressed_BFT_form(prob_of_ones))
            BFT_comp_bf_size_list.append(len(comp_bf.compressed_BFT_form(prob_of_ones)))
            # LinM_comp_bf_size += len(comp_bf.compressed_LinM_form(prob_of_ones))
            # LogM_comp_bf_size += len(comp_bf.compressed_LogM_form())




    sum_of_unique_elements = 0
    for block_number in range(len(All_logs_pile)):
        block_logs = All_logs_pile[block_number].split(",")
        block_elements_list = []
        for log in block_logs:
            elements = log.split(" ")

            for element in elements[:-1]:
                block_elements_list.append(element)

        block_unique_element_count = len(set(block_elements_list))
        sum_of_unique_elements += block_unique_element_count

    # Computation of theretical false positive rate #
    n = sum_of_unique_elements / len(All_logs_pile)

    theoretical_comp_fpr = (1-(1-(1/m))**(k*n))**k

    theoretical_trad_fpr = (1-(1-(1/2048))**(3*n))**3

    end = time.time()
    if Coding_Method != "All":
        print("Space Statistics for dataset", dataset, "|| m=", m, "|| k=", k, "|| one_prob=", prob_of_ones, "|| context_size=", context_size, "||")
        print("Coding Method: ", Coding_Method)
        print("Traditional bloom filter ones:", trad_bf_ones, "| Percentage: ", "%.2f" % ((100*trad_bf_ones)/(2048*len(All_logs_pile))), "%")
        print("Compressed bloom filter ones: ", comp_bf_ones, "| Percentage: ", "%.2f" % ((100*comp_bf_ones)/(m*len(All_logs_pile))), "%")
        print("Traditional bloom filter total size: ", 2048*len(All_logs_pile))
        print("Compressed bloom filter total size:  ", comp_bf_size)
        print("Change in size :  ", "%.2f" % (((2048*len(All_logs_pile)) - comp_bf_size)/(20.48*len(All_logs_pile))), "%")
        print("\nMean unique elements in the dataset are: ", n)

        print("Theoretical traditional bf false positive probability is: ", "%.2f" % (100*theoretical_trad_fpr), "%")
        print("Theoretical compressed bf false positive probability is:  ", "%.2f" % (100*theoretical_comp_fpr), "%")
        print("Execution time:", time.strftime("%H:%M:%S", time.gmtime(end - start)))
    else:
        print("Space Statistics for dataset", dataset, "|| m=", m, "|| k=", k, "|| one_prob=", prob_of_ones) # , "|| context_size=", context_size, "||")
        # print("Traditional bloom filter ones:", trad_bf_ones, "| Percentage: ", "%.2f" % ((100 * trad_bf_ones) / (2048 * len(All_logs_pile))), "%")
        # print("Compressed bloom filter ones: ", comp_bf_ones, "| Percentage: ", "%.2f" % ((100 * comp_bf_ones) / (m * len(All_logs_pile))), "%")
        print("Traditional bloom filter total size: ", 2048 * len(All_logs_pile))
        print("Arithmetic Coding Compressed bloom filter total size:            ", AC_comp_bf_size)
        print("Arithmetic Coding Compressed bloom filter standard deviation:    ", "%.2f" % statistics.pstdev(AC_comp_bf_size_list))
        # print("PPM Compressed bloom filter total size:                    ", BPPM_comp_bf_size)
        print("Simple Adaptive Model Compressed bloom filter total size:        ", SAM_comp_bf_size)
        print("Simple Adaptive Model Compressed bloom filter standard deviation:", "%.2f" % statistics.pstdev(SAM_comp_bf_size_list))
        print("Base Frequency Model Compressed bloom filter total size:         ", BFT_comp_bf_size)
        print("Base Frequency Model Compressed bloom filter standard deviation: ", "%.2f" % statistics.pstdev(BFT_comp_bf_size_list))
        # print("Lineal Mixing Compressed bloom filter total size:          ", LinM_comp_bf_size)
        # print("Logistic Mixing Compressed bloom filter total size:        ", LogM_comp_bf_size)
        print("\nMean unique elements in the dataset are: ", n)

        print("Theoretical traditional bf false positive probability is: ", "%.2f" % (100 * theoretical_trad_fpr), "%")
        print("Theoretical compressed bf false positive probability is:  ", "%.2f" % (100 * theoretical_comp_fpr), "%")
        print("Execution time:", time.strftime("%H:%M:%S", time.gmtime(end - start)))


def DCBF_Optimization_statistics(dataset:tuple):
    starting_block, ending_block = dataset

    path1 = global_path + "Scrap Blockchain Database/"
    File_Logs = open(path1 +"Logs for blocks " + str(starting_block) + " to " + str(ending_block), "r")

    All_logs_pile = File_Logs.readlines()

    better_cbf_fpr_occurances = 0
    sum_of_fpr_for_better_cbf_fpr = 0
    for block_nuber in range(len(All_logs_pile)):
        print(block_nuber)

        m, k, one_prob, (trad_bf_fpr, cbf_fpr) = Optimize_DCBF_fixed_z_k(dataset, starting_block + block_nuber)

        if cbf_fpr < trad_bf_fpr:
            better_cbf_fpr_occurances += 1
            sum_of_fpr_for_better_cbf_fpr += trad_bf_fpr - cbf_fpr


    print("Number of occurances where compression was better:", better_cbf_fpr_occurances)
    print("Mean improval of fpr with compression:            ", round(sum_of_fpr_for_better_cbf_fpr / better_cbf_fpr_occurances, 3))


def Space_statistics_dcbf(dataset: tuple):
    starting_block, ending_block = dataset

    path = global_path + "DCBF dataset/"

    File_DC_Bloom_Filters = open(path + "DCBFs for blocks " + str(starting_block) + " to " + str(ending_block), "r")
    DC_Bloom_filters = File_DC_Bloom_Filters.readlines()

    dcbf_total_space = 0
    for block_number in range(len(DC_Bloom_filters)):

        dcbf_total_space += len(bin(int(DC_Bloom_filters[block_number]))[2:])

    tradbf_total_space = (ending_block - starting_block) * 2048

    print("Space statistics for dataset",dataset)
    print("Total space occupied by Traditional bfs:",tradbf_total_space, "bits")
    print("Total space occupied by DCBFs:          ",dcbf_total_space, "bits")
    print("The DCBF method occupies ",round((100 * (tradbf_total_space-dcbf_total_space))/tradbf_total_space, 1), "% less bits" )

