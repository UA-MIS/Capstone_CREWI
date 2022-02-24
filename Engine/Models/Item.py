from flask import abort

import Status
import printFormatting

class Item:
    def __init__(self, id, name, imgUrl, score):
        try:
            self.id = id
            self.name = name
            self.imgUrl = imgUrl
            self.score = score
        except Exception as e:
            # if constructing item fails, print issue and update status
            printFormatting.printError(str(e))
            Status.addFail("ITEM_INIT_FAIL")
            raise e