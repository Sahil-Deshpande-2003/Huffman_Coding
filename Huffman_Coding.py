
import heapq
import os 


class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # defining comparators less_than and equals

        # defining function to compare binary tree nodes
        def __lt__(self, other):
            return self.freq < other.freq
        
        # telling them ki ek node dusre se chota hai iska matlab ek ki frequency dusre se choti hai

        def __eq__(self, other):
            if(other == None):
                return False
            if(not isinstance(other, HeapNode)):
                return False
            return self.freq == other.freq
        
        # so now interpreter knows that minimum Node is the node with Min frequency and it should know the basis on which we are
        # comparing 2 nodes since we are bulding a Min heap and at each step we are going to ask for the 2 Min nodes so 
        # we need to tell that we are comparing on basis of frequency and so give us the 2 nodes with Min frequency at each step 

    # functions for compression:

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)


    def make_codes_helper(self, root, current_code):
        if(root == None):
            return

        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")


    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)


    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text
    
    # encoded_text me pure string ka code pada hua hai


    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text


    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]

            # padded_encoded_text is a string, so byte as of now is a string 

            b.append(int(byte, 2))
        return b


    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        # now I have to read the content present in this path location and I have to write the output in 
        # the output_path kyuki mujhe sample.bin me kuch to likhna padega na 

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:

            # tu har jagah jo text pass kar raha tha function me, vo text tujhe milega
            # kaha se, jo user ne oath diya hai, vaha hoga na vo text, so apan ne 
            # vahi se liya hai 

            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
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


    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2) # convert into decimal

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        # padded info is stored in 1st 8 bits and the padding is done at the end so you need to remove both

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
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

        # ye utna acche se nahi samjha hai!

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
    
    
path = "D:/new_file.txt"

h = HuffmanCoding(path)

output_path = h.compress()
print("Compressed file path: " + output_path)

decom_path = h.decompress(output_path)
print("Decompressed file path: " + decom_path)
