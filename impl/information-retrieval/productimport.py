#!/usr/bin/python

__author__ = 'dust'

import codecs

from productinfo import Bluse


def main():
    f = codecs.open('./DamenBlusen.txt', 'r', 'utf-8')
    f.readline() #skip first line
    s = f.readline()
    print s
    b = Bluse(s)
    print b
    pass


if __name__ == '__main__':
    main()
