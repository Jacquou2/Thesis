from eth_bloom import BloomFilter
import random
import time
from numpy import transpose
import os
import csv




# This class is used for testing the performance of the Brute force and the Bloom filter element retrieval methods
class Loaded_Blockchain:
    def __init__(self,Number_of_blocks: int, Number_of_elements: int) -> None:

        ## The Number_of_blocks variable that is provided on the function call refers to the number of blocks that the
        # loaded blockchain must have. The Number_of_elements variable that is provided on the function call refers to
        # the number of elements that each block in the loaded blockchain must have
        self.Number_of_blocks = Number_of_blocks
        self.Number_of_elements = Number_of_elements

        ## The name of the file containing the elements of all the blocks is stored in the  Block_element_filename variable(string)
        ## The name of the file containing the Bloom filters is stored in the  Bloom_filter_filename variable(string)
        self.Block_element_filename = ""
        self.Bloom_filter_filename = ""

        ## The path variable is the variable containing the path in which the Blockchan database is stored in my computer
        self.path = "C:/Users/user/PycharmProjects/Bloom Filters/Blockchain Database"

        ## Variables for Check_bloom_filters_for_element function
        # When the Check_bloom_filters_for_element function is called, the numbers of the blocks that have a positive bloom filter response to the
        # queried element are stored in the Block_numbers_of_positive_BF list. The queried element is stored in the Element_checked_in_BF variable
        # The ExTime_check_Bloomfilters variable refers to the time required for the execution of the function
        self.Block_numbers_of_positive_BF = []
        self.Element_checked_in_BloomFIlters = None
        self.ExTime_check_Bloomfilters = None

        ## Variables for Retrieve_Element_BruteForce function
        # When the Retrieve_Element_BruteForce function is called, the the numbers of the blocks that contain the Element are stored in
        # the Block_numbers_retrieved_BruteForce list. The Brute Force method is used for the query.
        # The queried element is stored in the Element_retrieved_BruteForce variable
        # The ExTime_retrieve_BruteForce variable refers to the time required for the execution of the function
        self.Block_numbers_retrieved_BruteForce = []
        self.Element_retrieved_BruteForce = None
        self.ExTime_retrieve_BruteForce = None

        ## Variables for Retrieve_Element_BloomFIlter function
        # When the Retrieve_Element_BloomFIlter function is called, the the numbers of the blocks that contain the Element are stored in
        # the Block_numbers_retrieved_BloomFilter list. The Bloom filter method is used for the query.
        # The queried element is stored in the Element_retrieved_BruteForce variable
        # The ExTime_retrieve_BloomFilter variable refers to the time required for the execution of the function
        self.Block_numbers_retrieved_BloomFilter = []
        self.Element_retrieved_BloomFilter = None
        self.ExTime_retrieve_BloomFilter = None

        ## Variables for Retrieve_Element_BloomFIlter2 function
        # When the Retrieve_Element_BloomFIlter2 function is called, the the numbers of the blocks that contain the Element are stored in
        # the Block_numbers_retrieved_BloomFilter list. The Bloom filter method is used for the query.
        # The Retrieve_Element_BloomFIlter function is an optimization attempt of the Retrieve_Element_BloomFIlter function
        # The queried element is stored in the Element_retrieved_BruteForce variable
        # The ExTime_retrieve_BloomFilter variable refers to the time required for the execution of the function
        self.Block_numbers_retrieved_BloomFilter2 = []
        self.Element_retrieved_BloomFilter2 = None
        self.ExTime_retrieve_BloomFilter2 = None

        ## Identification of the file
        # Based on the Number_of_blocks and Number_of_elements variables, the corresponding blockchain is identified from
        # the Blockchain Database directory in my computer. When identified, the name of the file containing the
        # elements of all the blocks is stored in the  Block_element_filename variable(string), and the name
        # of the file containing the Bloom filters is stored in the  Bloom_filter_filename variable(string)
        List_of_directories =  os.listdir(self.path)
        for file in List_of_directories:
            if "(B=" + str(self.Number_of_blocks) + ", Ele=" + str(self.Number_of_elements) + ")" in file and "Block Elements" in file:
                self.Block_element_filename = file
            if "(B=" + str(self.Number_of_blocks) + ", Ele=" + str(self.Number_of_elements) + ")" in file and "Bloom FIlters" in file:
                self.Bloom_filter_filename = file
        # print(self.Bloom_filter_filename)


    def Check_bloom_filters_for_element(self,element):
        ## The element variable (bytes) is provided on call and refers to the element to be queried.
        # This function checks the bloom filter of every block in the Blockchain for the element.
        # When the bloom filter of a block has a positive response, the number of that block is appended on the Block_numbers_of_positive_BF list.

        start = time.time()
        Bloom_filter_file = open(self.path + "/" + self.Bloom_filter_filename,"r")
        for i in range(self.Number_of_blocks):
            Bloom_filter = BloomFilter(int(Bloom_filter_file.readline()))
            if element in Bloom_filter:
                self.Block_numbers_of_positive_BF.append(i)
                self.Element_checked_in_BF = element
        Bloom_filter_file.close()
        end = time.time()
        self.ExTime_check_Bloomfilters = (end - start)  # * (10**3)


    def Retrieve_Element_BruteForce(self, element):
        start = time.time()

        Block_Element_file = open(self.path + "/" + self.Block_element_filename, "r")
        # lines = csv.reader(Block_Element_file)
        lines = Block_Element_file.readlines()

        for i,line in enumerate(lines):
            line = list(line.split(","))
            line[-1] = line[-1][:-1]
            if str(element)[4:-1] in line:
                self.Block_numbers_retrieved_BruteForce.append(i)
                self.Element_retrieved_BruteForce = element


        Block_Element_file.close()
        end = time.time()
        self.ExTime_retrieve_BruteForce = (end - start) # * (10 ** 3)


    # def Retrieve_Element_BruteForce(self,element):
    #     ## The element variable (bytes) is provided on call and refers to the element to be queried.
    #     # This function checks every block in the blockchain for the element(variable) using the Brute force method.
    #     # Therefore, every element of every block is individually compared to the element(variable).
    #     # When the element(variable) is found in a block, the block number is appended in the Block_numbers_retrieved_BruteForce list
    #
    #     start = time.time()
    #     Block_Element_file = open(self.path + "/" + self.Block_element_filename, "r")
    #     for i in range(self.Number_of_blocks):
    #         if str(element) in Block_Element_file.readline():
    #             self.Block_numbers_retrieved_BruteForce.append(i)
    #             self.Element_retrieved_BruteForce = element
    #             # break
    #
    #         # Block_Element_file.readline()
    #         next(Block_Element_file)
    #         # Block_Element_file.seek(i+1)
    #
    #     Block_Element_file.close()
    #     end = time.time()
    #     self.ExTime_retrieve_BruteForce = (end - start) # * (10 ** 3)


    def Retrieve_Element_BloomFIlter(self,element):
        start = time.time()
        Bloom_filter_file = open(self.path + "/" + self.Bloom_filter_filename,"r")
        Block_element_file = open(self.path + "/" + self.Block_element_filename, "r")

        lines = csv.reader(Block_element_file)
        lines = Block_element_file.readlines()

        for i, line in enumerate(lines):
            Bloom_filter = BloomFilter(int(Bloom_filter_file.readline()))
            line = list(line.split(","))
            line[-1] = line[-1][:-1]
            if element in Bloom_filter:
                if str(element)[4:-1] in line:
                    self.Block_numbers_retrieved_BloomFilter.append(i)
                    self.Element_retrieved_BloomFilter = element
                #     # break

        Bloom_filter_file.close()
        Block_element_file.close()
        end = time.time()
        self.ExTime_retrieve_BloomFilter = (end - start)  # * (10**3)


    def Retrieve_Element_BloomFIlter2(self,element):
        start = time.time()
        self.Check_bloom_filters_for_element(element)
        Block_numbers_of_positive_BF = self.Block_numbers_of_positive_BF
        Block_element_file = open(self.path + "/" + self.Block_element_filename, "r")

        lines = csv.reader(Block_element_file)


        for i, line in enumerate(lines):
            if i in Block_numbers_of_positive_BF:
                if str(element)[4:-1] in line:
                    self.Block_numbers_retrieved_BloomFilter2.append(i)
                    self.Element_retrieved_BloomFilter2 = element
                    # break


        Block_element_file.close()
        end = time.time()
        self.ExTime_retrieve_BloomFilter2 = (end - start)  # * (10**3)



    # def Retrieve_Element_BloomFIlter2(self,element):
    #     ## The element variable (bytes) is provided on call and refers to the element to be queried.
    #     # This function checks only the blocks in the blockchain that have a positive bloom filter response for the element(variable).
    #     # Therefore, not every element of every block is compared to the element(variable).
    #     # When the element(variable) is found in a block, the block number is appended in the Block_numbers_retrieved_BruteForce list
    #
    #     start = time.time()
    #     self.Check_bloom_filters_for_element(element)
    #     Block_Element_file = open(self.path + "/" + self.Block_element_filename, "r")
    #
    #     for i,line in enumerate(Block_Element_file):
    #         if i/2 in self.Block_numbers_of_positive_BF:
    #             if str(element) in line:
    #                 self.Block_numbers_retrieved_BloomFilter2.append(int(i/2))
    #                 self.Element_retrieved_BloomFilter2 = element
    #                 # break
    #
    #     end = time.time()
    #     self.ExTime_retrieve_BloomFilter2 = (end - start) # * (10 ** 3)



        # for i in self.Block_numbers_of_positive_BF:
        #     line = lc.getline(self.path + "/" + self.Block_element_filename, 2*i+1)
        #     if str(element) in line:
        #         self.Block_numbers_retrieved_BloomFilter.append(i)
        #         self.Element_retrieved_BloomFilter = element


# This class is used only for the creation of the blockchain database in the Create_Blockchain_Data function
class Blockchain:
    def __init__(self, NumOfBlocks: int, NumOfElements: int) -> None:
        # When an object of the Blockchain class is created, the following variables are initialized
        # The NumOfBlocks and NumOfElements variables are provided when the object is created and refer to the number of
        # blocks in the blockchain object and the number of elements in each block
        self.NumOfBlocks = NumOfBlocks
        self.NumOfElements = NumOfElements
        # The Blocks list contains all the blocks in the blockchain. The blocks are objects of the Block class.
        self.Blocks = []
        for i in range(self.NumOfBlocks):
            self.Blocks.append(Block(self.NumOfElements,i))


    # The following functions inside the Blockchain class are not used.
    def Retrieve_Element(self,Element):
        start = time.time()
        Block_Numbers = []
        for count, block in enumerate(self.Blocks):
            if(block.Retrieve_Element(Element)):
                Block_Numbers.append(count)
        end = time.time()
        ExTime = (end - start)*(10**3)
        return Block_Numbers, ExTime

    def Retrieve_Element_BruteForce(self,Element):
        start = time.time()
        Block_Numbers = []
        for count, block in enumerate(self.Blocks):
            if (block.Retrieve_Element_BruteForce(Element)):
                Block_Numbers.append(count)
        end = time.time()
        ExTime = (end - start)*(10**3)
        return Block_Numbers, ExTime

    def Check_BFs_Element(self,Element):
        Block_Numbers = []
        for count, block in enumerate(self.Blocks):
            # Block_Numbers.append(block.Retrieve_Element(Element)[1])
            if(block.Check_BF_Element(Element)):
                Block_Numbers.append(count)
        return Block_Numbers

    def Retrieve_Element2(self,Element):
        start = time.time()
        BlockNumbers = []
        posBF = self.Check_BFs_Element(Element)
        for block in posBF:
            if(Element in self.Blocks[block].Bloom_Filter):
                BlockNumbers.append(block)
        end = time.time()
        ExTime = (end - start)*(10**3)
        return BlockNumbers, ExTime


# This class is used only for the creation of the blockchain database in the Create_Blockchain_Data function
class Block:
    def __init__(self, NumOfElements: int, seed: int) -> None:
        # When an object of the Block class is created, the following variables are initialized
        # The NumOfElements variable refers to the number of elements the block object will have.
        # The seed variable is the seed number for the creation of the random data
        # The Bloom_Filter is the bloom filter that is created for the elements of that object
        self.NumOfElements = NumOfElements
        self.Bloom_Filter = BloomFilter()

        # The Elements list contains all the elements in the block object.
        self.Elements = []
        random.seed(seed)

        # In this for loop the random elements are created and stored, in the form of bytes, in the ELements list.
        # The elements are also added in the bloom filter
        for x in range(self.NumOfElements):
            i = bytes(str(random.random()), 'utf-8')
            self.Bloom_Filter.add(i)
            self.Elements.append(i)

    # The following functions inside the Block class are not used.
    def Add_Element(self,element):
        self.Bloom_Filter.add(element)
        self.Elements.append(element)

    def Retrieve_Element(self,element):
        found = 0
        if(element in self.Bloom_Filter):
            for ele in self.Elements:
                if ele == element:
                    found = 1
                    break
        return found

    def Retrieve_Element_BruteForce(self,element):
        found = 0
        for ele in self.Elements:
            if ele == element:
                found = 1
        return found

    def Check_BF_Element(self,element):
        bloom_filter_response = 0
        if(element in self.Bloom_Filter):
            bloom_filter_response = 1
        return bloom_filter_response


# This function is not used, and can be ignored
def Compare_BF_BF(list_of_Elements: list, list_of_BFnumber:list, word:bytes):
    Temp_Res_array1 = []
    Temp_Res_array2 = []
    BloomFilter_Result = []
    BruteForce_Result = []

    start = time.time()

    for i in list_of_BFnumber:
        for j in list_of_Elements:
            time1 = Blockchain(j, i).Retrieve_Element2(word)[1]
            Temp_Res_array1.append(time1)
        BloomFilter_Result.append(Temp_Res_array1)
        Temp_Res_array1 = []

    med = time.time()

    for i in list_of_BFnumber:
        for j in list_of_Elements:
            time1 = Blockchain(j, i).Retrieve_Element_BruteForce(word)[1]
            Temp_Res_array1.append(time1)
        BruteForce_Result.append(Temp_Res_array1)
        Temp_Res_array1 = []

    end = time.time()

    # for i in list_of_BFnumber:
    #     for j in list_of_Elements:
    #         time1 = Blockchain(j, i).Retrieve_Element(word)[1]
    #         time2 = Blockchain(j,i).Retrieve_Element_BruteForce(word)[1]
    #         time3 = Blockchain(j,i).Retrieve_Element2(word)[1]
    #         Temp_Res_array1.append(time1)
    #         Temp_Res_array2.append(time2)
    #         Temp_Res_array3.append(time3)
    #     BloomFilter_Result.append(Temp_Res_array1)
    #     BruteForce_Result.append(Temp_Res_array2)
    #     BloomFilter2_Result.append(Temp_Res_array3)
    #     Temp_Res_array1 = []
    #     Temp_Res_array2 = []
    #     Temp_Res_array3 = []

    BloomFilter_Result = transpose(BloomFilter_Result)
    BruteForce_Result = transpose(BruteForce_Result)

    Ex1 = med - start
    Ex2 = end - med

    return BloomFilter_Result, BruteForce_Result, Ex1, Ex2



# This function is used only for the creation of the blockchain database
def Create_Blockchain_Data(Num_Of_Blocks: int,Num_Of_Elements: int) -> None:
    ## This function creates blockchain data and stores them locally.
    ## The number of blocks in the blockchain and the number of Elements in each block must be specified

    # The path variable defines the path in which the files will be stored
    path = "C:/Users/user/PycharmProjects/Bloom Filters/Blockchain Database/"

    # The data od the blockchain are created with the Blockchain class.
    # Therefore, the data is a blockchain object that contains block objects.
    # In each block there are elements and a bloom filter that represents the elements
    Data = Blockchain(Num_Of_Blocks, Num_Of_Elements).Blocks

    # The File_Blockchain_Elements variable is the file that is created that contains the elements of each block.
    # The File_Blockchain_BloomFilters variable is the file that is created that contains the bloom filter of each block.
    # Each file is named in the following way: "Blockchain (B=X, Ele=Y) Block Elements", where X is the number of blocks
    # in the blockchain and Y is the number of elements in each block. The naming of each file is important and is used
    # in the operations that access the files, so it must not be changed
    File_Blockchain_Elements = open(path + "Blockchain (B="+str(Num_Of_Blocks)+ ", Ele="+ str(Num_Of_Elements)+ ") Block Elements","w")
    File_Blockchain_BloomFilters = open(path + "Blockchain (B=" + str(Num_Of_Blocks)+ ", Ele="+ str(Num_Of_Elements)+ ") Bloom FIlters", "w")

    # In this for loop the data are written in the files in the following way. The File_Blockchain_Elements contains
    # the elements of each block seperated by comma. Each block is separeted from the next by "\n\n".
    # The File_Blockchain_BloomFilters contains the bloom filters of each block in their integer form. Each bloom filter
    # is separeted from the next by "\n\n". The block elements of the File_Blockchain_Elements correspond with the
    # bloom filters in the File_Blockchain_BloomFilters file, so the 1st line of elements belongs to the 1st block and
    # the 1st bloom filter also belongs to the 1st block
    i = 0
    for block in Data:
        num_of_elements = len(block.Elements)
        for count, element in enumerate(block.Elements):
            if count < num_of_elements-1:
                File_Blockchain_Elements.write(str(element)[4:-1] + ",")
            elif count == num_of_elements-1:
                File_Blockchain_Elements.write(str(element)[4:-1])
        File_Blockchain_Elements.write('\n')
        File_Blockchain_BloomFilters.write(str(int(block.Bloom_Filter))+'\n')
        i += 1

    File_Blockchain_Elements.close()
    File_Blockchain_BloomFilters.close()



# This function is used for testing the performance of the Brute force and the Bloom filter element retrieval methods
def Test_Loaded_Blockchain_Time_performance(list_of_number_of_Blocks:list, list_of_number_of_Elements: list, element:bytes):
    # This function returns the execution time of the Retrieve_Element_BruteForce and the Retrieve_Element_BloomFIlter function
    # of the Loaded_Blockchain class for a number of Loaded_Blockchain objects. Each object deffers in the number of blocks and
    # the number of elements. The function's input are two lists, one containing the number of blocks and one containing the
    # number of elements in each block. The execution time is measured for every possible combination of the two lists so totaly
    # n*m combinations, where n,m: the lenght of each list. This process is executed for the Retrieve_Element_BruteForce and
    # the Retrieve_Element_BloomFIlter function separately.
    # Another input is the element to be queried.
    # The function also returns the total execution time of all the combinations for the Retrieve_Element_BruteForce and the
    # Retrieve_Element_BloomFIlter functions individually.


    # The Temp_REBruteForce_array and Temp_REBloomFilter_array lists are used as temporary storage, while the final result
    # is stored in the REBruteForce_result_array and the REBloomFilter_result_array lists
    Temp_REBruteForce_array =[]
    Temp_REBloomFilter_array = []

    REBruteForce_result_array = []
    REBloomFilter_result_array = []

    # The start, med and end variables store the time and are used to return the total execution time of all the
    # combinations for the Retrieve_Element_BruteForce and the Retrieve_Element_BloomFIlter functions.
    start = time.time()

    # For the measurments of the execution time, a Loaded_Blockchain object is created, named Tested_Blockchain. Then,
    # the Retrieve_Element_BruteForce function is executed and the result(time) is appended in the result list.
    # This process is repeated for all the combinations on the list_of_number_of_Blocks and list_of_number_of_Elements
    # given as variables
    for number_of_Blocks in list_of_number_of_Blocks:
        for number_of_Elements in list_of_number_of_Elements:
            Tested_Blockchain = Loaded_Blockchain(number_of_Blocks,number_of_Elements)
            Tested_Blockchain.Retrieve_Element_BruteForce(element)
            Temp_REBruteForce_array.append(Tested_Blockchain.ExTime_retrieve_BruteForce)

        REBruteForce_result_array.append(Temp_REBruteForce_array)
        Temp_REBruteForce_array = []

    med = time.time()

    # The same process is executed here for the Retrieve_Element_BloomFIlter function.
    for number_of_Blocks in list_of_number_of_Blocks:
        for number_of_Elements in list_of_number_of_Elements:
            Tested_Blockchain = Loaded_Blockchain(number_of_Blocks, number_of_Elements)
            Tested_Blockchain.Retrieve_Element_BloomFIlter(element)
            Temp_REBloomFilter_array.append(Tested_Blockchain.ExTime_retrieve_BloomFilter)

        REBloomFilter_result_array.append(Temp_REBloomFilter_array)
        Temp_REBloomFilter_array = []

    end = time.time()

    # The Ex_Time_BruteForce_Performance refers to the execution time of all the combinations for theRetrieve_Element_BruteForce function,
    # while the Ex_Time_BloomFilter_Performance refers to the Retrieve_Element_BloomFIlter function
    Ex_Time_BruteForce_Performance = med - start
    Ex_Time_BloomFilter_Performance = end - med


    return REBruteForce_result_array, REBloomFilter_result_array, Ex_Time_BruteForce_Performance, Ex_Time_BloomFilter_Performance

