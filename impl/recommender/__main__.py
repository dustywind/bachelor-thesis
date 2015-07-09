
import sys

import recommender.webapi

if __name__ == '__main__':
    database = sys.argv[1]
    host = sys.argv[2]
    port = sys.argv[3]
    recommender.webapi.run(database, host, port)



