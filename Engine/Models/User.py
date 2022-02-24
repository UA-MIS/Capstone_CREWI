from flask import abort

import Status
import printFormatting

class User:
    def __init__(self, userId, username):
        try:
            self.userId = userId
            self.username = username
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            Status.addFail("USER_INIT_FAIL")