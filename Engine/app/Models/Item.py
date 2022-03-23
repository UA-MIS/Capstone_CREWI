import globalStatus
import printFormatting

# ITEM.PY: Class for menu items; this is used in the item recommendation process

class Item:
    # item constructor sets the arguments to item's fields
    def __init__(self, id, name, imgUrl, score):
        try:
            self.id = id
            self.name = name
            self.imgUrl = imgUrl
            self.score = score
        except Exception as e:
            # if constructing item fails, print issue and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("ITEM_INIT_FAIL")
            raise e

    # allows items to be printed to the terminal, useful for debugging
    def __str__(self):
        return "ID: " + str(self.id) + "\tName: " + self.name + "\tImage URL: " + self.imgUrl + "\tScore: " + str(self.score)

# not technically part of the class but it's essentially an item utility function so it was placed in the class file
# this takes a list/array of items and returns a tuple of their IDs (e.g. (1, 2, 3, etc.))
def getIdTuple(items):
    # making empty tuple
    idTuple = ()
    
    # adding each ID to it
    for item in items:
        idTuple += (item.id,)

    # returning it; this is used for looking up all the items during the item rec process
    return idTuple