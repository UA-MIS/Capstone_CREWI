# module to handle global status; never add fails or issues directly, always use these methods to do it

import printFormatting

# this method should only be called at the beginning of recommendation; it makes the global status array
# this can't really be error-handled, if this fails I would be astonished
def init():
    global statusArray
    statusArray = []

# fails are things that require immediate exit of the process; this will make sure FAIL is in the array and then add the exact fail
def addFail(failure):
    # if this fails, raise an error since we must track fails and add a fail code for it
    try:
        if "FAIL" not in statusArray: statusArray.append("FAIL")
        if failure not in statusArray: statusArray.append(failure)
    except Exception as e:
        printFormatting.printError(str(e))
        if "FAIL" not in statusArray: statusArray.append("FAIL")
        if "ADD_FAIL_FAIL" not in statusArray: statusArray.append("ADD_FAIL_FAIL")
        raise e

# issues are non-breaking problems, like missing username, location, etc.; this will make sure ISSUE is in the array and then add the exact issue
def addIssue(issue):
    # if this fails, raise an error since we must track issues and add a fail code for it
    try:
        if "ISSUE" not in statusArray: statusArray.append("ISSUE")
        if issue not in statusArray: statusArray.append(issue)
    except Exception as e:
        printFormatting.printError(str(e))
        if "FAIL" not in statusArray: statusArray.append("FAIL")
        if "ADD_ISSUE_FAIL" not in statusArray: statusArray.append("ADD_ISSUE_FAIL")
        raise e