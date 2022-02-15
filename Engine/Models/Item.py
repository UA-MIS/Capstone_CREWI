from flask import abort

class Item:
    def __init__(self, id, name, imgUrl, score):
        try:
            self.id = id
            self.name = name
            self.imgUrl = imgUrl
            self.score = score
        except:
            # print issue to terminal and return 500 to requester
            print("500 ERROR: Item formatting error")
            abort(500, "500 ERROR: Item formatting error")