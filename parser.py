#!python

import re
import sys


class Parser:

    def __init__(self, inpt=None):
        if input is None:
            pass
        self.data = inpt
        self.count = 0 
        self.pre_star_count = 0
        self.pre_dot_count = 0
        self.cur_star_count = 0
        self.cur_dot_count = 0
        self.index = []
        self.output = []

    # Create for debugging purpose.
    def printInputData(self):
        print (self.data)

    # main parser method to process input data.
    def parseData(self):
        for line in self.data:
            line = line.strip()
            if line not in '\xc2\xa0\n' and line != '':
                starpat = re.compile(r'^(\*+)(.*)$')  # Pattern match for * in the string
                dotpat = re.compile(r'^(\.+)(.*)$')  # Pattern match for . in the string

                if starpat.match(line) is not None:  # Parse lines with *'s
                    # get the count of * in the string
                    self.cur_star_count = len(starpat.match(line).group(1))

                    # Collect the data from the string
                    data = starpat.match(line).group(2)

                    if self.cur_star_count == 1:
                        self.count += 1
                        self.appendOutput(str(self.count) + ' ' + data)
                        self.pre_star_count = self.cur_star_count
                        self.index = []
                    elif self.cur_star_count > 1:
                        if self.pre_star_count == 0 and self.count == 0:
                            self.count = 1
                        indx = [self.count]
                        # check if previously index was set
                        # if yes, use it to increment to next value
                        if len(self.index) > 0:
                            if self.pre_star_count >= self.cur_star_count:
                                for i in range(1, self.cur_star_count):
                                    indx.append(self.index[i])
                                # Increment last digit in subsequence ex: 3.2.1 to 3.2.2
                                # Also 3.1 to 3.2
                                val = 1 + indx[-1]
                                indx[-1] = val
                                self.index = indx
                            elif self.pre_star_count < self.cur_star_count:
                                for i in range(1, self.cur_star_count):
                                    # check if previous count data in index
                                    # If current * count is greater then append 1
                                    if i >= len(self.index):
                                        indx.append(1)
                                    else:
                                        indx.append(self.index[i])
                                self.index = indx
                        else:
                            for i in range(1, self.cur_star_count):
                                indx.append(1)
                            self.index = indx

                        # Generate value as 3.1.1 etc
                        value = ".".join(map(str, self.index))

                        # Set prev counter to current counter value
                        self.pre_star_count = self.cur_star_count

                        # Append output to the list
                        self.appendOutput(str(value) + ' ' + data)
                elif dotpat.match(line) is not None:  # Parse lines with . and ..n
                    # get the count of . in the string
                    self.cur_dot_count = len(dotpat.match(line).group(1))

                    # get the data from the string.
                    data = dotpat.match(line).group(2)

                    if self.cur_dot_count > self.pre_dot_count:
                        data = '- ' + data

                        # If current dot count is greater then previous should
                        # have + instead of - so replace it with +
                        # Modify output list directly i.e last value
                        pre_data = self.output[-1]
                        pre_data = pre_data.replace("-", "+")
                        self.output[-1] = pre_data
                    elif self.cur_dot_count <= self.pre_dot_count:
                        data = '- ' + data

                    # Add leading spaces to the data
                    data = data.rjust(len(data) + self.cur_dot_count)

                    # Set the prev dot count to current dot count.
                    self.pre_dot_count = self.cur_dot_count

                    # Append final output to list
                    self.appendOutput(data)
                elif self.pre_dot_count > 0 and \
                        self.pre_star_count == self.cur_star_count:

                    # Span multiple lines case
                    pre_data = self.output[-1]

                    # Add leading spaces to the data text.
                    line = line.rjust(len(line) + self.pre_dot_count + 3)
                    data = pre_data + "\n" + line

                    # Directly modify the output list for previous/last value.
                    self.output[-1] = data

    # Append data to the output list
    def appendOutput(self, data):
        self.output.append(data)

    # Write output to the file.
    def generateOutput(self):
        fh = open("output.txt", "w")
        fh.write("\n".join(self.output))
        fh.close()

    # For debugging purpose.
    def printOutputData(self):
        print ("\n".join(self.output))


if __name__ == "__main__":
    data = sys.stdin.readlines()
    Obj = Parser(data)
    Obj.parseData()
    Obj.printOutputData()
    # Obj.generateOutput()
