# this method should only be called at the beginning of recommendation; it makes the global status array
def init():
    global statusArray
    statusArray = []

# fails are things that require immediate exit of the process; this will make sure FAIL is in the array and then add the exact fail
def addFail(failure):
    if "FAIL" not in statusArray: statusArray.append("FAIL")
    statusArray.append(failure)

# issues are non-breaking problems, like missing username, location, etc.; this will make sure ISSUE is in the array and then add the exact issue
def addIssue(issue):
    if "ISSUE" not in statusArray: statusArray.append("ISSUE")
    statusArray.append(issue)