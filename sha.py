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
    def MIX_sha160(t, init_words, w=32):
        if t >= 16:
            return sched.ROTL(init_words[t-3] ^ init_words[t-8] ^ init_words[t-14] ^ init_words[t-16], 1)
        return init_words[t]
    @staticmethod
    def MIX_sha224(t, init_words, w=32):
        if t >= 16:
            return int((sched.sigma1(init_words[t-2]) + init_words[t-7] + sched.sigma0(init_words[t-15]) + init_words[t-16])   % 2 ** 32)
        return init_words[t]

    # FIPS-180-4 6.1.2
    # Create message schedule for block i
    @staticmethod
    def create_schedule_sha160(inital_words):
        W = []
        for t in range(0, 16):
            W.append(sched.MIX_sha160(t, inital_words))
        for t in range(16, 80):
            W.append(sched.MIX_sha160(t, W))
        return W
    @staticmethod
    def create_schedule_sha224(inital_words):
        W = []
        for t in range(0, 16):
            W.append(sched.MIX_sha224(t, inital_words))
        for t in range(16, 64):
            W.append(sched.MIX_sha224(t, W))
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
    K_sha160 = []
    # FIPS-180-4 5.3.1
    # Constant inital hash values
    H_sha160 = [int('67452301', 16),
        int('efcdab89', 16),
        int('98badcfe', 16),
        int('10325476', 16),
        int('c3d2e1f0', 16)]

    K_sha224 = [int('428a2f98', 16),
        int('71374491', 16),
        int('b5c0fbcf', 16),
        int('e9b5dba5', 16),
        int('3956c25b', 16),
        int('59f111f1', 16),
        int('923f82a4', 16),
        int('ab1c5ed5', 16),
        int('d807aa98', 16),
        int('12835b01', 16),
        int('243185be', 16),
        int('550c7dc3', 16),
        int('72be5d74', 16),
        int('80deb1fe', 16),
        int('9bdc06a7', 16),
        int('c19bf174', 16),
        int('e49b69c1', 16),
        int('efbe4786', 16),
        int('0fc19dc6', 16),
        int('240ca1cc', 16),
        int('2de92c6f', 16),
        int('4a7484aa', 16),
        int('5cb0a9dc', 16),
        int('76f988da', 16),
        int('983e5152', 16),
        int('a831c66d', 16),
        int('b00327c8', 16),
        int('bf597fc7', 16),
        int('c6e00bf3', 16),
        int('d5a79147', 16),
        int('06ca6351', 16),
        int('14292967', 16),
        int('27b70a85', 16),
        int('2e1b2138', 16),
        int('4d2c6dfc', 16),
        int('53380d13', 16),
        int('650a7354', 16),
        int('766a0abb', 16),
        int('81c2c92e', 16),
        int('92722c85', 16),
        int('a2bfe8a1', 16),
        int('a81a664b', 16),
        int('c24b8b70', 16),
        int('c76c51a3', 16),
        int('d192e819', 16),
        int('d6990624', 16),
        int('f40e3585', 16),
        int('106aa070', 16),
        int('19a4c116', 16),
        int('1e376c08', 16),
        int('2748774c', 16),
        int('34b0bcb5', 16),
        int('391c0cb3', 16),
        int('4ed8aa4a', 16),
        int('5b9cca4f', 16),
        int('682e6ff3', 16),
        int('748f82ee', 16),
        int('78a5636f', 16),
        int('84c87814', 16),
        int('8cc70208', 16),
        int('90befffa', 16),
        int('a4506ceb', 16),
        int('bef9a3f7', 16),
        int('c67178f2', 16)
        ]
    # FIPS-180-4 5.3.2
    # Constant inital hash values
    H_sha224 = [int('c1059ed8', 16),
        int('367cd507', 16),
        int('3070dd17', 16),
        int('f70e5939', 16),
        int('ffc00b31', 16),
        int('68581511', 16),
        int('64f98fa7', 16),
        int('befa4fa4', 16)]

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
            schedule = sched.create_schedule_sha160(preproccessed_message[i-1])
            message_hashed = hash.hash_sha160(schedule, H_sha160, i)
            H_sha160.append(message_hashed)
        # Create msg variable (This will be final result)
        msg = ''
        # Foreach word in the last entry of H_sha160
        for w in H_sha160[-1]:
            # Add word in hex to $msg string variable
            msg += hex(w)[2:].zfill(8)
        return msg
    @staticmethod
    def sha224(message, message_format=0):
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
        # Set H variable with inital hash value
        H = [hash.get_H_sha224()]
        # FIPS-180-4 6.2.2
        # Foreach parsed block, create message schedule and hash, then append hash values to $H
        for i in range(1, len(preproccessed_message) + 1):
            schedule = sched.create_schedule_sha224(preproccessed_message[i-1])
            message_hashed = hash.hash_sha224(schedule, H, i)
            H.append(message_hashed)
        # Create msg variable (This will be final result)
        msg = ''
        # Foreach word in the last entry of H
        for w in H[-1][:7]:
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
    def f_sha160(x, y, z, t):
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
    @staticmethod
    def get_H_sha224():
        return hash.H_sha224
    
    # FIPS-180-4 6.2.2
    @staticmethod
    def hash_sha160(W, H_sha160, i):
        # Set inital hash values from previous (final) hash values
        a = H_sha160[i-1][0]
        b = H_sha160[i-1][1]
        c = H_sha160[i-1][2]
        d = H_sha160[i-1][3]
        e = H_sha160[i-1][4]
        # Iterate 80 times
        for t in range(80):
            if 0 <= t <= 19:
                hash.K_sha160.append(int('5A827999', 16))
            elif 20 <= t <= 39:
                hash.K_sha160.append(int('6ED9EBA1', 16))
            elif 40 <= t <= 59:
                hash.K_sha160.append(int('8F1BBCDC', 16))
            elif 60 <= t <= 79:
                hash.K_sha160.append(int('CA62C1D6', 16))
            # Calculate temporary value
            T = int((hash.ROTL(a, 5) + hash.f_sha160(b, c, d, t) + e + hash.K_sha160[t] + W[t]) % 2 ** 32)
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
    @staticmethod
    def hash_sha224(W, H, i):
        # Set inital hash values from previous (final) hash values
        a = H[i-1][0]
        b = H[i-1][1]
        c = H[i-1][2]
        d = H[i-1][3]
        e = H[i-1][4]
        f = H[i-1][5]
        g = H[i-1][6]
        h = H[i-1][7]
        # Iterate 64 times
        for t in range(0, 64):
            # Calculate temporary value 1
            T1 = int((h + hash.SIGMA1(e) + hash.Ch(e, f, g) + hash.K_sha224[t] + W[t]) % 2 ** 32)
            # Calculate temporary value 2
            T2 = int((hash.SIGMA0(a) + hash.Maj(a, b, c)) % 2 ** 32)
            h = g
            g = f
            f = e
            e = int((d + T1)  % 2 ** 32)
            d = c
            c = b
            b = a
            a = (T1 + T2) % 2 ** 32
        # Calculate final hash values
        H0 = (H[i-1][0] + a) % 2 ** 32
        H1 = (H[i-1][1] + b) % 2 ** 32
        H2 = (H[i-1][2] + c) % 2 ** 32
        H3 = (H[i-1][3] + d) % 2 ** 32
        H4 = (H[i-1][4] + e) % 2 ** 32
        H5 = (H[i-1][5] + f) % 2 ** 32
        H6 = (H[i-1][6] + g) % 2 ** 32
        H7 = (H[i-1][7] + h) % 2 ** 32
        # Return final hash values
        return [H0, H1, H2, H3, H4, H5, H6, H7]
