import sys
from projectmaker import make_directory, make_basicfile

if "-createnew" in sys.argv:
    i = sys.argv.index("-createnew")
    path = sys.argv[i + 1]
    make_directory(path)
    make_basicfile(path)
    
