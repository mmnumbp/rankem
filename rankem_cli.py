"""Usage: rankem.py -x ITEM...
       rankem.py [-i] (ITEM DESCRIPTION)...
       rankem.py -f [-x|-i] [-l DELIIM] (ITEMS_FILE | -)
       rankem.py -fj [-i] JSON_FILE

Rank a list of items from best to worst by repeatedly picking the best of two.
    
Options:
    -x        --noDesc              Parse as though there are no descriptions
    -i        --ignoreDesc          Parse with descriptions, but ignore them
    -f        --use-file            Load items from file
    -l DELIM  --delimiter DELIM     Set which sequence of characters delimits 
                                    items and descriptions. Defaults to double
                                    newline. Whitespace will be trimmed.
    -j        --json                Read items from a json file
    -h        --help                Display this help text

Examples:
    python rankem.py -x item1 item2 item3
    python rankem.py item1 "description 1" item2 "description 2"
    python rankem.py file stuff.txt
      stuff.txt:
        item 1

          description 1

          item 2

          description 2
    python rankem.py file -j stuff.json
      stuff.json:
          [{
            "name": "item 1",
            "description": "description 1"
          },
          {
            "name": "item 2",
            "description": "description 2"
          }]

"""

from docopt import docopt

if __name__ == '__main__':
    opts = docopt(__doc__)
    print(opts)
    #fileStr = ''
    #with open(opts['ITEMS_FILE'], 'r') as iFile:
    #    fileStr = iFile.read()
    