import math
import sys
import datetime

print("----------------------------------------------------------------")
print("-                                                              -")
print("-                        TXT to Huffman                        -")
print("-                                                              -")
print("----------------------------------------------------------------")


# Part 1
# Character statistics
print("                      Software Instruction")
print("----------------------------------------------------------------")
print("-  Please input name of the file                               -")
print("-  If this file is in the same folder as the application       -")
print("-  You may just need to type its name. e.g. GameOfThrones.txt  -")
print("-  Otherwise, you may need to input the full path of the file  -")
print("-  e.g. E:\Repository\GameOfThrones.txt                        -")
print("----------------------------------------------------------------")

fileName = input("\nFile Name: ")
try:
    file = open(fileName, "r", errors='ignore')  # open file
except Exception as Error:
    print("{}".format(Error))
    print("Program Terminated.")
    print("\nPress Enter to exit.")
    a = input()  # Hold
    sys.exit()

print(datetime.datetime.now().strftime('%X'), " Read the file successfully...\n")
print(datetime.datetime.now().strftime('%X'), " Start statistics on characters...")
charCount = {}  # dictionary to hold char counts
charProbability = {}  # dictionary to hold char probabilities
validchars = "abcdefghijklmnopqrstuvwxyz"  # only these counted

for i in range(97, 123):  # lowercase range
    c = (chr(i))  # the chars a-z
    charCount[c] = charProbability[c] = 0  # initialize count
blank = " "
charCount[blank] = charProbability[blank] = 0

print(datetime.datetime.now().strftime('%X')," Counting...")
for lines in file:
    for word in lines:
        chars = list(word)  # convert word into a char list
        for c in chars:  # process chars
            if c.isalpha():  # only alpha allowed
                if c.isupper():
                    c = c.lower()  # if char is upper convert to lower
                if c in validchars:  # if in valid char set
                    charCount[c] += 1  # increment count
            if c == " ":
                charCount[blank] += 1

totalCharNum = 0
entropy = 0
# Calculating total characters
for value in charCount.values():
    totalCharNum += value
# Calculating probabilities and write it to charProbability dictionary
print(datetime.datetime.now().strftime('%X'), " Calculating probabilities and entropy...")
for key in charCount.keys():
    charProbability[key] = charCount[key] / totalCharNum
    entropy += -charProbability[key] * math.log(charProbability[key], 2)

file.close()
print(datetime.datetime.now().strftime('%X'), " Done.\n")


# Part 2
# Huffman Coding
print(datetime.datetime.now().strftime('%X'), " Generate Huffman Coding...")


# Creating tree nodes
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


# Main function for huffman coding
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

# Sort nodes.
sort = sorted(charProbability.items(), key=lambda e: e[1], reverse=True)
nodes = sort

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))

    # Sort nodes.
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

# Export Huffman Tree to HuffmanCode tuple
huffmanCode = huffman_code_tree(nodes[0][0])

# Statistics on coding efficiency of Huffman coding.
HuffmanAverageLen = 0
HuffmanCodewordVariance = 0
for (char, frequency) in sort:
    HuffmanAverageLen += len(huffmanCode[char]) * frequency

HuffmanCodingEfficiency = entropy / HuffmanAverageLen
for (char, frequency) in sort:
    HuffmanCodewordVariance += ((len(huffmanCode[char]) - HuffmanAverageLen) ** 2) * frequency

print(datetime.datetime.now().strftime('%X'), " Done.\n")


# Part 3
# ASCII Code
print(datetime.datetime.now().strftime('%X'), " Read ASCII Code...")
ASCIICode = {}  # dictionary to hold value of ASCII code
for (char, frequency) in sort:
    ASCIICode[char] = str(bin(ord(char)).replace('0b','')).zfill(7)

# Statistics on coding efficiency of ASCII code.
ASCIIAverageLen = 7 # Standard ASCII codeword length
ASCIICodingEfficiency = entropy / ASCIIAverageLen
print(datetime.datetime.now().strftime('%X'), " Done.\n")


print("                Result Table")
print(' Char | Frequency | ASCII Code | Huffman Code ')
print('---------------------------------------------- ')
for (char, frequency) in sort:
    print(' %-4r | %9.5f | %10s | %12s ' % (char, frequency, ASCIICode[char], huffmanCode[char]))
print("\nEntropy:                             %.3f" % (entropy))
print("Average ASCII Codeword Length:       %.3f" % (ASCIIAverageLen))
print("ASCII Coding Efficiency:             %.3f %%" % (ASCIICodingEfficiency * 100))
print("Average Huffman Codeword Length:     %.3f" % (HuffmanAverageLen))
print("Huffman Codeword Variance:           %.3f" % (HuffmanCodewordVariance))
print("Huffman Coding Efficiency:           %.3f %%" % (HuffmanCodingEfficiency * 100))


print("\nPress Enter to exit.")
b = input()  # Hold
