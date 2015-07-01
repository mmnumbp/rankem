"""Usage: rankem.py -x ITEM...
       rankem.py [-i] (ITEM DESCRIPTION)...
       rankem.py [-x|-i] -f [-l DELIIM] (ITEMS_FILE | -)
       rankem.py -fj [-i] (JSON_FILE | -)

Rank a list of items from best to worst by repeatedly picking the best of two.
    
Options:
    -x        --noDesc              Indicate that there are no descriptions 
                                    specified in the input
    
    -i        --ignoreDesc          Indicate that there are descriptions 
                                    specified in the input, but that they
                                    should be ignored

    -f        --use-file            Load items from file
    
    -l DELIM  --delimiter DELIM     Set which sequence of characters delimits 
                                    items and descriptions. Defaults to double
                                    newline. Whitespace will be trimmed.
    
    -j        --json                Read items from a json file
    
    -h        --help                Display this help text

Examples:
    python rankem.py -x item1 item2 item3
    python rankem.py item1 "description 1" item2 "description 2"
    python rankem.py --file -x stuff.txt
      stuff.txt:
        item 1

        item 2
    python rankem.py --file -j stuff.json
      stuff.json:
          [{
            "name": "item 1",
            "description": "description 1"
          },
          {
            "name": "item 2",
            "description": "description 2"
          }]
    echo item 1 \~ description 1 \~ item 2 \~ description 2 | python rankem.py -f -l \~ -

"""

import textwrap

from rankem import Item, Rankem
from docopt import docopt
from lib import terminalsize

def rank(rankem):
    present(rankem.next())

def present(items):
    width = terminalsize.get_terminal_size()[0]
    columnWidth = int(width/2 - 1)
    columnCenter = ('{:^' + str(columnWidth) + '}').format
    item1Str = columnCenter("Option 1: " + items[0].name())
    item2Str = columnCenter("Option 2: " + items[1].name())

    print(item1Str + item2Str)


def massage(opts):
    items = None
    descriptions = None
    if opts['-f']:
        # Items/descriptions are in a file
        pass
    else:
        # Items/descriptions are arguments
        items = opts['ITEM']
        if opts['-x'] or opts['-i']:
            descriptions = ['' for i in opts['ITEM']]
        else:
            descriptions = opts['DESCRIPTION']
    return [Item(i, d) for i, d in zip(items, descriptions)]

if __name__ == '__main__':
    opts = docopt(__doc__)
    
    print(opts)
    rank(Rankem(massage(opts)))

    #fileStr = ''
    #with open(opts['ITEMS_FILE'], 'r') as iFile:
    #    fileStr = iFile.read()
    

