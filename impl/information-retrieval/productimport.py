#!/usr/bin/python

__author__ = 'dust'

import codecs

from productinfo import Bluse
import irdb 


__database_path = '../database'
__database_name = 'ir.db'

def main():
    db_test()
    return

def db_test():
    tc = irdb.TableCreator(__database_path, __database_name)
    tc.create_tables()
    pass

def bluse_test():
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
