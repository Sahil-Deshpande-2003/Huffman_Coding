
import heapq
import os 


class HuffmanCoding:
    def __init__(self, path):
        self.path = path # path of the file to be compressed
        self.heap = [] # Min heap using an array
        self.codes = {} # maps the characters to codes
        self.reverse_mapping = {} # maps the codes to characters

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # defining comparators less_than and equals

        # defining function to compare binary tree nodes
        # if 1 node is smaller than the other it means that the freq_dict of the 1st one is less than other one
        
        def __lt__(self, other):
            return self.freq < other.freq


        '''The isinstance function in Python is used to check if an object
belongs to a particular class or a tuple of classes.
In my code, it is used to determine
if the other object is an instance of the HeapNode class.'''


        def __eq__(self, other):
            if(other == None):
                return False
            if(not isinstance(other, HeapNode)):
                return False
            
            return self.freq == other.freq
        
        # so now interpreter knows that minimum Node is the node with Min freq_dict and it should know the basis on which we are
        # comparing 2 nodes since we are bulding a Min heap and at each step we are going to ask for the 2 Min nodes so 
        # we need to tell that we are comparing on basis of freq_dict and so give us the 2 nodes with Min freq_dict at each step 

    # functions for compression:

    def make_freq_dict_dict(self, text):
        freq_dict = {}
        for character in text:
            if not character in freq_dict:
                freq_dict[character] = 0
            freq_dict[character] += 1
        return freq_dict

    def make_heap(self, freq_dict):
        for key in freq_dict:
            node = self.HeapNode(key, freq_dict[key]) # create a node with the key and its value
            heapq.heappush(self.heap, node)
            '''
            Heap data structure is mainly used to represent a priority queue.
            In Python, it is available using the “heapq” module.
            '''

    def merge_nodes(self):
        while(len(self.heap)>1):

            # POP the 2 nodes with min freq

            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)


    def make_codes_helper(self, root, current_code):

        # once the binary tree is formed, build the codes for each character

        if(root == None):
            return

        if(root.char != None):

            # base case -> Leaf Node
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")


    def make_codes(self):

        # now to access the root, here, each time we are picking up 2 nodes, adding their frequencies and creating a node with key = None
        #  and frequency = f1 + f2, hence as we keep going upwards in the tree, the frequency keeps on increasing 
        # hence the lower nodes i.e. the nodes with lesser freq are towards the front of the heap 

        # here root is the node with min freq
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)


    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character] # encode the text by using the binary codes for each character
        return encoded_text
    
    # encoded_text me pure string ka code pada hua hai


    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8 # it should be a multiple of 8
        for i in range(extra_padding):
            encoded_text += "0" # Padding done at the end

        padded_info = "{0:08b}".format(extra_padding) # means extra padding = 0 and ":08" specifies that the field should be 8 characters wide, and "b" indicates that the value should be formatted as a binary number.

        encoded_text = padded_info + encoded_text # padded information is stored in the 1st 8 bits  
        return encoded_text

    # read acche se!!!!

    def get_byte_array(self, padded_encoded_text):


        # Convert the bits into bytes

        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray() # creates an empty bytearray object named b.

        #A bytearray in Python is a mutable sequence of bytes.
        # It is similar to a regular bytes object (immutable), 
        # but bytearray allows you to modify the bytes it contains after creation.


        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]

            # padded_encoded_text is a string, so byte as of now is a string 

            b.append(int(byte, 2))
        return b


    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        # now I have to read the content present in this path location and I have to write the output in 
        # the output_path (sample.bin in this case)

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:

            # The wb indicates that the file is opened for writing in binary mode.



            # ('r+'): This method opens the file for both reading and writing.

            # Text is accessed using the path provided by the user

            text = file.read() # access the file using the path 
            text = text.rstrip()
            '''
            In Python, trailing characters refer to characters that appear at the end of a string, list, or any sequence data structure. These characters come after the main content of the sequence and are often used to represent additional or optional information.

            For example, in a string, trailing characters are the characters that appear after the last non-whitespace character. In a list, trailing elements are the elements that appear after the last non-empty element. Trailing characters or elements can include spaces, tabs, newline characters

            The rstrip() method removes any trailing characters (characters at the end a string), space is the default trailing character to remove.

            '''

            freq_dict = self.make_freq_dict_dict(text)
            self.make_heap(freq_dict)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))

        print("Compressed")
        return output_path


    """ functions for decompression: """
    '''
    Steps for decompression:

    1. Implement decompress function
    2. Implement remove padding function
    3. Implement decode text function
    
    
    '''
    # start YAHA SE

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8] # padded_info is stored in the 1st 8 bits
        extra_padding = int(padded_info, 2) # number if 0's added at the end

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        # padded info is stored in 1st 8 bits and the padding is done at the end so you need to remove both

        # Eg 10100010 10100000 -> if extra padding = 5 means that last 5 0's are padded at the end, so to remove them,
        # use -1*extra_padding so that indexing begins from the end 

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                # self.reverse_mapping contains the mapping of codes with characters

                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text


    def decompress(self, input_path):

        '''
        Converts .bin file back to .txt file 
        '''
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"
        # sample.bin file split on the basis of '.', so filename is sample and extension is .bin
        # and output path will be sample_decompressed.txt

        # since we are reading content from bin file (sample.bin) so we need to use
        # 'rb' mode

        # converting bytes back to bits

      

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1) # here I have read 1st byte
            while(len(byte) > 0):
                byte = ord(byte) # using ord you can find the integer corresponding to that value
                bits = bin(byte)[2:].rjust(8, '0') # for bin(5) you'll get bin as b'101 hence start from the 2nd index
                # and rjust so that you get a 8 bit number hence 00000101
                bit_string += bits
                byte = file.read(1) # here again you are reading byte

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("Decompressed")
        return output_path
    
    
path = "D:/Huffman_Coding_Text_File.txt"


h = HuffmanCoding(path)

output_path = h.compress()
print("Compressed file path: " + output_path)

decom_path = h.decompress(output_path)
print("Decompressed file path: " + decom_path)
