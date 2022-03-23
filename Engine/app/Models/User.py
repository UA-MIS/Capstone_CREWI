import globalStatus
import printFormatting

# USER.PY: Class for users from the database

class User:
    # constructor that takes in ID and username; users don't have much importance other than that in the recommendation processes
    def __init__(self, userId, username):
        try:
            self.userId = userId
            self.username = username
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("USER_INIT_FAIL")