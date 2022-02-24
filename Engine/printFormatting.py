# module to print things more descriptively

successColor = '\033[92m' # green
warningColor = '\033[93m' # yellow
errorColor = '\033[91m' # red
resetColor = '\033[0m' # reset, use after any color printing

def printSuccess(message):
    print(successColor + "SUCCESS: " + message + resetColor)

def printError(message):
    print(errorColor + "ERROR: " + message + resetColor)

def printWarning(message):
    print(warningColor + "WARNING: " + message + resetColor)

def printFinalStatus(statuses):
    print(errorColor + "BREAKING FAILURES AND ISSUES:")
    for status in statuses:
        print("\t" + status)
    print(resetColor)