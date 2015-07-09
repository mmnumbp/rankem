import random
from collections import defaultdict
from functools import partial
from operator import itemgetter

"""
Simple data object for storing item information. You may wish to use the rank
argument if you have a partially predetermined order. A higher rank is a better
score.
"""
class Item(object):
    def __init__(self, name, description, rank=1):
        self._name = name.strip(' \t\n\r')
        self._description = description.strip(' \t\n\r')
        self._rank = rank
    def name(self):
        return self._name
    def description(self):
        return self._description
    def __repr__(self):
        return "(" + str(self._rank) + ") " + self.name() + ": " + self.description()
    def __str__(self):
        return self.name()

"""
A Rankem object manages a single list of items to be ranked.
itemSet must be iterable and contain Item objects.
"""
class Rankem(object):
    def __init__(self, itemSet):
        self.byRank = defaultdict(set)
        self.rand = random.Random()
        self.currentOptions = None

        for item in itemSet:
            self.byRank[item._rank].add(item)

        self.rand.seed()

    def next(self):
        ranksWithDupes = list(filter(lambda r: len(self.byRank[r]) > 1, self.byRank))

        # Return a tuple of different random items of the same rank
        # If there are no items of the same rank, return None
        if len(ranksWithDupes) == 0:
            return None
        else:
            randIdx = self.rand.randint(0, len(ranksWithDupes)-1)
            randRank = ranksWithDupes[randIdx]
            rankItemList = list(self.byRank[randRank])
            
            # Find two random different items of the same rank
            randItemFunc = partial(self.rand.randint, 0, len(rankItemList)-1)
            item1idx = item2idx = randItemFunc()
            while(item1idx == item2idx):
                item2idx = randItemFunc()
            
            options = (rankItemList[item1idx], rankItemList[item2idx])
            self.currentOptions = options
            return options

    def choose(self, choice):
        if choice not in self.currentOptions:
            raise ValueError("Item chosen was not one that was presented")
        else:
            self.byRank[choice._rank].remove(choice)
            choice._rank += 1
            self.byRank[choice._rank].add(choice)

    def ranking(self):
        byRankItemsList = list(self.byRank.items())
        # Sort dict items list by rank
        byRankItemsList.sort(key=itemgetter(0))
        # Remove rank keys, leaving only values (single-element sets)
        sortedRankSetList = [rankSet for rank, rankSet in byRankItemsList]
        # Unpack single-element sets
        return list(map(set.pop, sortedRankSetList))[::-1]


if __name__ == '__main__':
    # Try test data
    testItemSet = set([Item('A', ''),
                       Item('B', ''),
                       Item('C', ''),
                       Item('D', '')])
    rankem = Rankem(testItemSet)
    nextChoice = rankem.next()
    while(nextChoice != None):
        print(nextChoice)
        rankem.choose(nextChoice[0])
        nextChoice = rankem.next()
    print(rankem.ranking())