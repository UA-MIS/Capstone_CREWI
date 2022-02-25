# module to print things more descriptively

# the error handling here won't raise an exception since printing isn't worth stopping the recommendation over
# it also won't raise an issue because console printing is irrelevant to the widget
# however, it will print an error for back-end debugging purposes

# colors for printing
successColor = '\033[92m' # green
warningColor = '\033[93m' # yellow
errorColor = '\033[91m' # red
resetColor = '\033[0m' # reset, use after any color printing

# print message in green for success
# if printing success fails, print the error and print success manually
def printSuccess(message):
    try:
        print(successColor + "SUCCESS: " + message + resetColor)
    except Exception as e:
        printError(str(e))
        print(successColor + "SUCCESS: Generic success message" + resetColor)

# print message in red for error
# if error printing fails, manually print a generic message
def printError(message):
    try:
        print(errorColor + "ERROR: " + message + resetColor)
    except Exception as e:
        print(errorColor + "ERROR: " + str(e) + resetColor)
        print(errorColor + "ERROR: Generic error message" + resetColor)

# print message in yellow for issue
# if printing warning fails, an error will be printed
def printWarning(message):
    try:
        print(warningColor + "WARNING: " + message + resetColor)
    except Exception as e:
        printError(str(e))
        print(warningColor + "WARNING: Generic warning message" + resetColor)

# print all the fails and issues; this happens when a global fail has occurred
# if this somehow fails, it'll print the error and an explanation
def printFinalStatus(statuses):
    try:
        print(errorColor + "BREAKING FAILURES AND ISSUES:")
        for status in statuses:
            print("\t" + status)
        print(resetColor)
    except Exception as e:
        printError(str(e))
        printError("Unable to display failures and issues")