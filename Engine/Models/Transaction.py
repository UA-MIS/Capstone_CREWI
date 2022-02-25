from flask import abort

import printFormatting
import globalStatus

class Transaction:
    def __init__(self, userId, storeId, itemId):
        try:
            self.userId = userId
            self.storeId = storeId
            self.itemId = itemId
            self.score = float(0)
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("TRANSACTION_INIT_FAIL")

    def __str__(self):
        return "User ID: " + str(self.userId) + "\tStore ID: " + str(self.storeId) + "\tItem ID: " + str(self.itemId) + "\tScore: " + str(self.score)