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
            printFormatting.printError(str(e))
            # print issue to terminal and return 500 to requester
            printFormatting.printError("Item formatting error")
            abort(500, "500 ERROR: Item formatting error")