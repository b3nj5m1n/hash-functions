import sys
import math


class sched:

    # FIPS-180-4 2.2.2
    # Rotate bits to the right
    @staticmethod
    def ROTR(x, n, w=32):
        return ((x >> n) | (x << w - n)) & ((1 << w) - 1)

    # FIPS-180-4 3.2
    # Rotate bits to the right
    @staticmethod
    def ROTL(x, n, w=32):
        return sched.ROTR(x, w-n)

    # FIPS-180-4 4.1.2
    @staticmethod
    def sigma0(x):
        return sched.ROTR(x, 7) ^ sched.ROTR(x, 18) ^ (x >> 3)

    # FIPS-180-4 4.1.2
    @staticmethod
    def sigma1(x):
        return sched.ROTR(x, 17) ^ sched.ROTR(x, 19) ^ (x >> 10)

    # FIPS-180-4 6.1.2
    # (New word function for message schedule)
    @staticmethod
    def MIX(t, init_words, w=32):
        if t >= 16:
            return sched.ROTL(init_words[t-3] ^ init_words[t-8] ^ init_words[t-14] ^ init_words[t-16], 1)
        return init_words[t]

    # FIPS-180-4 6.1.2
    # Create message schedule for block i
    @staticmethod
    def create_schedule(inital_words):
        W = []
        for t in range(0, 16):
            W.append(sched.MIX(t, inital_words))
        for t in range(16, 80):
            W.append(sched.MIX(t, W))
        return W

class ppp:
    # Convert ASCII to ASCII
    def from_str(message):
        return message
    # Convert integer to ASCII
    def from_int(message):
            return str(chr(int(message, 10)))
    # Convert hexadecimal to ASCII
    def from_hex(message):
        return str(chr(int(message, 16)))
    # Convert binary to ASCII
    def from_bin(message):
        return str(chr(int(message, 2)))
    # Convert octal to ASCII
    def from_oct(message):
        return str(chr(int(message, 8)))
    # Convert file to ASCII
    def from_file(filename):
        # Open file and store its content in $content
        with open(filename, 'rb') as f:
            content = f.read()
        # Create result variable
        rs = ''
        # Convert content to ASCII
        for c in content:
            rs += str(chr(c))
        return rs

class prep:
    # FIPS-180-4 5.1.1
    # This converts from an ASCII string to a binary string, it's lenght being a multiple of the block_size
    def padd(message, block_size=512, lenght_block_size=64):
        # Convert message to array of integers
        ints = []
        for c in message:
            ints.append(ord(c))
        # Convert array of integers to array of strings (Binary representation of the integers)
        message = []
        for i in ints:
            message.append(bin(i)[2:].zfill(8))
        # Convert string array (Message in bytes) to string (Message in bits)
        message = ''.join(message)
        # Get current lenght of message (in bits)
        l = len(message)
        # Get the lenght of the message in bits (In bits. I'm confused too)
        l_bits = bin(l)[2:].zfill(8)
        # Add bit (With value of 1) to the end of the message (In bits)
        message += '1'
        # Padd message with 0's
        k = (((block_size - lenght_block_size) % (block_size)) - (1 + l))
        while k < 0:
            k += block_size
        for i in range(0, k):
            message += '0'
        # Add lenght of message (In bits) to the end of the message, padd with zeroes to size of lenght_block_size
        message += l_bits.zfill(lenght_block_size)
        return message

    # # FIPS-180-4 5.2.1
    # Parse message (In bits) into blocks of the size of block_size, thoose are parsed into 16 words of the lenght of w bits
    # Returns array of arrays, words are now integers
    def parse(message, block_size=512, w=32):
        # Create empty list of blocks
        M = []
        # How many blocks will be created
        n = int(len(message) / block_size)
        # Iterate over that number
        for n in range(0, n):
            # Create new block of the size of block_size
            m = (message[n*block_size:(n*block_size)+block_size])
            # Create empty word list
            W = []
            # Iterate over how many words are in a block (16)
            for i in range(0, 16):
                # Append the word to W, now as integer
                W.append(int(m[i * w:(i * w) + w],2))
            # Add the list of words (Containing the information of the block) to the list of blocks
            M.append(W)
        return M

    # FIPS-180-4 6.2.1
    # Pre-proccess a message
    # Profiles:
    # 0 - sha160
    def prep(message, profile=0):
        block_size = 512
        lenght_block_size = 64
        w = 32
        if profile == 0:
            block_size = 512
            lenght_block_size = 64
            w = 32
        message = prep.padd(message, block_size, lenght_block_size)
        message = prep.parse(message, block_size, w)
        return message

class hash:

    # FIPS-180-4 4.2.2
    # Constant values
    K = []
    # FIPS-180-4 5.3.1
    # Constant inital hash values
    H_sha160 = [int('67452301', 16),
        int('efcdab89', 16),
        int('98badcfe', 16),
        int('10325476', 16),
        int('c3d2e1f0', 16)]

    # Main function, return sha160 hash of input
    # Message_format's:
    # 0 = ASCII
    # 1 = Integer (Base 10)
    # 2 = Hexadecimal (Base 16)
    # 3 = Binary (Base 2)
    # 4 = Octal (Base 8)
    # 5 = From file
    @staticmethod
    def sha160(message, message_format=0):
        # Set inital message
        inital_message = ppp.from_str(message)
        # Convert message if neccessary
        if message_format == 0:
            inital_message = ppp.from_str(message)
        elif message_format == 1:
            inital_message = ppp.from_int(message)
        elif message_format == 2:
            inital_message = ppp.from_hex(message)
        elif message_format == 3:
            inital_message = ppp.from_bin(message)
        elif message_format == 4:
            inital_message = ppp.from_oct(message)
        elif message_format == 5:
            inital_message = ppp.from_file(message)
        # Preproccess (converted) message (Padding & Parsing)
        preproccessed_message = prep.prep(inital_message)
        # Set H_sha160 variable with inital hash value
        H_sha160 = [hash.get_H_sha160()]
        # FIPS-180-4 6.2.2
        # Foreach parsed block, create message schedule and hash, then append hash values to $H_sha160
        for i in range(1, len(preproccessed_message) + 1):
            schedule = sched.create_schedule(preproccessed_message[i-1])
            message_hashed = hash.hash(schedule, H_sha160, i)
            H_sha160.append(message_hashed)
        # Create msg variable (This will be final result)
        msg = ''
        # Foreach word in the last entry of H_sha160
        for w in H_sha160[-1]:
            # Add word in hex to $msg string variable
            msg += hex(w)[2:].zfill(8)
        return msg

    # FIPS-180-4 2.2.2
    # Rotate bits to the right
    @staticmethod
    def ROTR(x, n, w=32):
        return ((x >> n) | (x << w - n)) & ((1 << w) - 1)

    # FIPS-180-4 3.2
    # Rotate bits to the right
    @staticmethod
    def ROTL(x, n, w=32):
        return sched.ROTR(x, w-n)

    # FIPS-180-4 4.1.2
    @staticmethod
    def SIGMA0(x):
        return hash.ROTR(x, 2) ^ hash.ROTR(x, 13) ^ hash.ROTR(x, 22)

    # FIPS-180-4 4.1.2
    @staticmethod
    def SIGMA1(x):
        return hash.ROTR(x, 6) ^ hash.ROTR(x, 11) ^ hash.ROTR(x, 25)

    # FIPS-180-4 4.1.1
    @staticmethod
    def Ch(x, y, z):
        return (x & y) ^ (~x & z)

    # FIPS-180-4 4.1.1
    @staticmethod
    def Maj(x, y, z):
        return (x & y) ^ (x & z) ^ (y & z)

    # FIPS-180-4 4.1.1
    @staticmethod
    def Parity(x, y, z):
        return x ^ y ^ z

    # FIPS-180-4 4.1.1
    @staticmethod
    def f(x, y, z, t):
        if 0 <= t and t <= 19:
            return hash.Ch(x, y, z)
        if 20 <= t and t <= 39:
            return hash.Parity(x, y, z)
        if 40 <= t and t <= 59:
            return hash.Maj(x, y, z)
        if 60 <= t and t <= 79:
            return hash.Parity(x, y, z)

    # FIPS-180-4 5.3.2
    # Get the (constant) inital hash values
    @staticmethod
    def get_H_sha160():
        return hash.H_sha160
    
    # FIPS-180-4 6.2.2
    @staticmethod
    def hash(W, H_sha160, i):
        # Set inital hash values from previous (final) hash values
        a = H_sha160[i-1][0]
        b = H_sha160[i-1][1]
        c = H_sha160[i-1][2]
        d = H_sha160[i-1][3]
        e = H_sha160[i-1][4]
        # Iterate 80 times
        for t in range(80):
            if 0 <= t <= 19:
                hash.K.append(int('5A827999', 16))
            elif 20 <= t <= 39:
                hash.K.append(int('6ED9EBA1', 16))
            elif 40 <= t <= 59:
                hash.K.append(int('8F1BBCDC', 16))
            elif 60 <= t <= 79:
                hash.K.append(int('CA62C1D6', 16))
            # Calculate temporary value
            T = int((hash.ROTL(a, 5) + hash.f(b, c, d, t) + e + hash.K[t] + W[t]) % 2 ** 32)
            e = d
            d = c
            c = hash.ROTL(b, 30)
            b = a
            a = T
        # Calculate final hash values
        H0 = (H_sha160[i-1][0] + a) % 2 ** 32
        H1 = (H_sha160[i-1][1] + b) % 2 ** 32
        H2 = (H_sha160[i-1][2] + c) % 2 ** 32
        H3 = (H_sha160[i-1][3] + d) % 2 ** 32
        H4 = (H_sha160[i-1][4] + e) % 2 ** 32
        # Return final hash values
        return [H0, H1, H2, H3, H4]

