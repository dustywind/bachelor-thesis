#!/usr/bin/python

__author__ = 'dust'

import codecs
import sys

from productinfo import Bluse
import irdb


__database_path = '../database'
__database_name = 'ir.db'

def main():
    tc = irdb.TableCreator(__database_path, __database_name)
    tc.create_tables()

    f = codecs.open('./DamenBlusen.txt', 'r', 'utf-8')
    f.readline() # skip first line
    for line in f:
        try:
            b = Bluse(line)
            handler = tc.get_clothing_handler()
            handler.add_clothing(b)
        except UnicodeEncodeError:
            print(line)
            print(sys.exc_info())
            pass
        except ValueError:
            print(line)
            print(sys.exc_info())
            pass
        except Exception:
            print(line)
            print(sys.exc_info())
            pass
        except Exception, e:
            pass
        pass
    pass

if __name__ == '__main__':
    main()
