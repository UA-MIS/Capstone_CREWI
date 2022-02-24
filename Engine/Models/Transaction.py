from flask import abort

import printFormatting
import Status

class Transaction:
    def __init__(self, userId, storeId, itemId):
        try:
            self.userId = userId
            self.storeId = storeId
            self.itemId = itemId
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            Status.addFail("TRANSACTION_INIT_FAIL")

    def __str__(self):
        return "User ID: " + str(self.userId) + "\tStore ID: " + str(self.storeId) + "\tItem ID: " + str(self.itemId)