# This file is an example of how to use the hash functions
#
# Import sys to get access to arguments
import sys
# From sha224.py file import the hash function under the name of sha224
from sha import hash
# Main function / Entry point | Set args variable to given arguments, except for the first one because that is just the script name (main.py, in this case)
def main(args=sys.argv[1:]):
    # Print hash value of the first argument, interpret first argument as $mode
    print(hash.sha160(args[0], int(args[1])))
# Call the main function after every potential function is defined
main()