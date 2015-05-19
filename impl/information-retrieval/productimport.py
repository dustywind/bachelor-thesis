#!/usr/bin/python

__author__ = 'dust'

import codecs

from productinfo import Bluse


def main():
    f = codecs.open('./DamenBlusen.txt', 'r', 'utf-8')
    f.readline() #skip first line
    for line in f:
        try:
            b = Bluse(line)
            print b
        except ValueError:
            print "error"
        pass
        


if __name__ == '__main__':
    main()
