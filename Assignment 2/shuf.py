#!/usr/bin/python

import argparse, random, sys


class shuf:
    def __init__(self, lines):
        self.lines = lines

    def shuf(self, n=""):
        length = len(self.lines)
        parser = argparse.ArgumentParser()

        # Shuffle the lines
        random.shuffle(self.lines)

        # Structural pattern matching
        match n:

            # If no head count, print every shuffled line
            case "":
                for i in range(length):
                    print(self.lines[i])

            # If there is a head count, make sure it's valid and then print out the correct amount of lines
            case non_empty:
                try:
                    count = int(n)
                    assert (count >= 0)
                    if count > length:
                        n = str(length)
                except:
                    parser.error("Head count is invalid")

                for i in range(int(n)):
                    print(self.lines[i])

    def repeat(self, n=""):
        length = len(self.lines)
        parser = argparse.ArgumentParser

        # Structural pattern matching
        match n:

            # If no head count, run forever
            case "":
                while True:
                    print(random.choice(self.lines))

            # If there's a head count, make sure it's valid and then print out the correct amount of lines
            case non_empty:
                try:
                    count = int(n)
                    assert (count >= 0)
                except:
                    parser.error("Head count is invalid")

                for i in range(int(n)):
                    print(random.choice(self.lines))


def main():
    usage_msg = """shuf [OPTION]... FILE
or:  shuf -e [OPTION]... [ARG]...
or:  shuf -i LO-HI [OPTION]...
Write a random permutation of the input lines to standard output."""

    parser = argparse.ArgumentParser(usage=usage_msg)

    # Positional Argument
    parser.add_argument("file", nargs="*")

    # Head Count
    parser.add_argument("-n", "--head-count", action="store", dest="head_count", default="",
                        help="output at most COUNT lines")

    # Input Range
    parser.add_argument("-i", "--input-range", action="store", dest="input_range",
                        help="treat each number LO through HI as an input line")

    # Echo
    parser.add_argument("-e", "--echo", action="store_true", dest="echo", help="treat each ARG as an input line")

    # Repeat
    parser.add_argument("-r", "--repeat", action="store_true", dest="repeat", help="output lines can be repeated")

    args = parser.parse_args()

    output = []


    # If the input range flag is set
    if args.input_range:
        try:
            # Get the range and make sure its valid
            ir = args.input_range.split('-')
            assert (len(ir) == 2)
            LO = int(ir[0])
            HI = int(ir[1])
            assert (HI >= LO)
            assert (LO >= 0 and HI >= 0)
            output = list(range(LO, HI + 1))
        except:
            parser.error("Input range is invalid")

        try:
            assert (not args.echo)
        except:
            parser.error("Cannot combine -e and -i")

        try:
            assert (not args.file)
        except:
            parser.error("Extra operand")
    
    # If the echo flag is set, the output is just what is inputted
    elif args.echo:
        output = args.file

    # If there is a positional argument
    elif args.file:

        # Check there is only one file specified
        if len(args.file) == 1:
            try:

                # If that file is '-', just read from input
                if (args.file[0] == '-'):
                    for line in sys.stdin:
                        output.append(line.rstrip('\n'))

                # Otherwise, open the file and read the lines as the input
                else:
                    with open(args.file[0]) as input:
                        for line in input.readlines():
                            output.append(line.rstrip('\n'))
            except:
                parser.error("File could not be opened")
                return
        else:
            parser.error("Too many arguments")



    # Otherwise, there are no arguments so just read from input
    else:
        for line in sys.stdin:
            output.append(line.rstrip('\n'))

    shuffle = shuf(output)

    # If the repeat flag is set
    if args.repeat:
        shuffle.repeat(args.head_count)

    # Otherwise just shuffle the output normally
    else:
        shuffle.shuf(args.head_count)


if __name__ == "__main__":
    main()
