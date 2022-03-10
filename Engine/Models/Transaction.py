import printFormatting
import globalStatus

# TRANSACTION.PY: Class for holding a transaction from the database

class Transaction:
    # constructor takes all the fields except score, which is initialized to 0
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

    # allows transactions to be printed to the terminal, useful for debugging
    def __str__(self):
        return "User ID: " + str(self.userId) + "\tStore ID: " + str(self.storeId) + "\tItem ID: " + str(self.itemId) + "\tScore: " + str(self.score)