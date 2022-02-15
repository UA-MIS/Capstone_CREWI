from flask import abort

class User:
    def __init__(self, userId, username):
        try:
            self.userId = userId
            self.username = username
        except:
            # print issue to terminal and return 500 to requester
            print("500 ERROR: User formatting error")
            abort(500, "500 ERROR: User formatting error")