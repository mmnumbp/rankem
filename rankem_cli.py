"""Usage: rankit.py [-i DELIM] [-x | -d DELIM] ITEMS_FILE

Rank a list of items from best to worst by repeatedly picking the best of two
    
Options:
    -h        --help                Display this help text
    -i DELIM, --itemDelim DELIM     Delimiter between items [default: ~]
    -d DELIM, --descDelim DELIM     Delimiter between descriptions [default: ~]
    -x        --noDesc              Disable descriptions

Examples:

python rankit.py -i '#' -d '-' items.txt
items.txt:
#   item 1 - description 1 
#   item 2 - description 2
#   item 3 - description 3

python rankit.py items2.txt
items2.txt:
item 1
~
description 1
~
item 2
~
description 2
    
"""

from docopt import docopt

if __name__ == '__main__':
    opts = docopt(__doc__)
    fileStr = ''
    with open(opts['ITEMS_FILE'], 'r') as iFile:
        fileStr = iFile.read()
    