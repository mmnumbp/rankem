class item(object):
    name = ""
    description = ""
    rank = 0

class rankit(object):
    itemList = []

    def __init__(self, itemList):
        self.itemList = itemList
