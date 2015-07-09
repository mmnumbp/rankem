"""Usage: rankem.py -x ITEM...
       rankem.py [-i] (ITEM DESCRIPTION)...
       rankem.py [-x|-i] -f [-l DELIIM] (ITEMS_FILE | -)
       rankem.py -fj [-i] (JSON_FILE | -)

Rank a list of items from best to worst by repeatedly picking the best of two.
Loading a list from a file isn't working yet.
    
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
import itertools
import sys

from rankem import Item, Rankem
from docopt import docopt
from lib import terminalsize

if sys.version_info < (3, 0):
    input = raw_input

def rank(rankem):
    choices = rankem.next()
    while(choices is not None):
        print("")
        present(choices)
        print("")
        print("(a)/(b)/(q)uit/(s)kip: ")
        a = set(['a', '1', 'left', 'l'])
        b = set(['b', '2', 'right', 'r'])
        q = set(['q', 'quit', 'exit', 'save'])
        s = set(['s', 'skip'])
        
        choice = ''
        while choice not in (a | b | q | s):
            choice = input().lower()
        
        if choice in a:
            rankem.choose(choices[0])
        elif choice in b:
            rankem.choose(choices[1])
        elif choice in q:
            die()

        # else is when choice is in (s)kip
        choices = rankem.next()
    return rankem.ranking()


def present(items):
    width = terminalsize.get_terminal_size()[0]
    columnWidth = int(width/2 - 1)
    # Center item names and print
    columnCenter = ('{:^' + str(columnWidth) + '}').format
    item1Str = columnCenter("Option A: " + items[0].name())
    item2Str = columnCenter("Option B: " + items[1].name())
    print(item1Str + item2Str)

    ### Prepare description formatting
    desc1wrap = textwrap.wrap(items[0].description(), columnWidth)
    desc2wrap = textwrap.wrap(items[1].description(), columnWidth)
        
    ## Make both description line lists the same length 
    if len(desc1wrap) < len(desc2wrap):
        while len(desc1wrap) < len(desc2wrap):
            desc1wrap.append('')
    elif len(desc2wrap) <  len(desc1wrap):
        while len(desc2wrap) < len(desc1wrap):
            desc2wrap.append('')
    else:
        # Descriptions take the same number of lines to print, do nothing
        pass

    ## Formatting to print side-by-side
    addWhitespaceToColumnWidth = lambda s: s+' '*(columnWidth-len(s)+1)
    desc1wrap = list(map(addWhitespaceToColumnWidth, desc1wrap))
    desc2wrap = list([line+'\n' for line in desc2wrap])

    # Intersperse lines, like so:
    # [desc1[0], desc2[0], desc1[1], desc2[1]...]
    finalOutputList = list(
        itertools.chain.from_iterable(zip(desc1wrap, desc2wrap)) )
    print(''.join(finalOutputList))

def displayFinalRanking(ranking):
    print("")
    print("Final ranking:")
    for item in ranking:
        print(item.name())

def massage(opts):
    items = None
    descriptions = None
    if opts['-f']:
        # Items/descriptions are in a file
        pass # STUB!
    else:
        # Items/descriptions are arguments
        items = opts['ITEM']
        if opts['-x'] or opts['-i']:
            descriptions = ['' for i in opts['ITEM']]
        else:
            descriptions = opts['DESCRIPTION']
    return [Item(i, d) for i, d in zip(items, descriptions)]

def die():
    exit(0)

if __name__ == '__main__':
    opts = docopt(__doc__)
    displayFinalRanking(rank(Rankem(massage(opts))))

    #fileStr = ''
    #with open(opts['ITEMS_FILE'], 'r') as iFile:
    #    fileStr = iFile.read()
    

