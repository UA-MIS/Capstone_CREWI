from flask import abort

class Transaction:
    def __init__(self, userId, storeId, itemId):
        try:
            self.userId = userId
            self.storeId = storeId
            self.itemId = itemId
        except:
            # print issue to terminal and return 500 to requester
            print("500 ERROR: Transaction formatting error")
            abort(500, "500 ERROR: Transaction formatting error")