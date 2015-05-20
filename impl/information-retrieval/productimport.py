#!/usr/bin/python

__author__ = 'dust'

import codecs
import pdb

from productinfo import Bluse
import irdb 



__database_path = '../database'
__database_name = 'ir.db'

def main():
    tc = irdb.TableCreator(__database_path, __database_name)
    tc.create_tables()

    f = codecs.open('./DamenBlusen.txt', 'r', 'utf-8')
    f.readline() #skip first line
    for line in f:
        try:
            b = Bluse(line)
            handler = tc.get_clothing_handler()

            pdb.set_trace()


            handler.add_clothing(b)
        except UnicodeEncodeError, e:
            #print e
            pass
        except ValueError, e:
            #print e
            pass
        except Exception, e:
            pass
        pass

if __name__ == '__main__':
    main()
