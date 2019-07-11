# This file is an example of how to use the hash functions
#
# Import sys to get access to arguments
import sys
# From sha224.py file import the hash function under the name of sha224
from sha import hash
import sha
# Main function / Entry point | Set args variable to given arguments, except for the first one because that is just the script name (main.py, in this case)
def main(args=sys.argv[1:]):
    # Print hash value of the first argument, interpret first argument as $mode
    print("sha160:\n" + str(hash.sha160(args[0], args[1])))
    print("sha224:\n" + str(hash.sha224(args[0], args[1])))
    print("sha256:\n" + str(hash.sha256(args[0], args[1])))
    print("sha384:\n" + str(hash.sha384(args[0], args[1])))
    print("sha512:\n" + str(hash.sha512(args[0], args[1])))
    print("sha512/224:\n" + str(hash.sha512_t(args[0], 224)))
    print("sha512/256:\n" + str(hash.sha512_t(args[0], 256)))
# Call the main function after every potential function is defined
main()