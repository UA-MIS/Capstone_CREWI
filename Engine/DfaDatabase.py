from dotenv import load_dotenv
from flask import abort
import os
import mysql.connector
import globalStatus
import printFormatting
from Models import Transaction


#this can be where the class ends up; I have some concerns about file structure though
class DfaDatabase:
    # takes username, returns user id or 0 if user not found
    def lookupUser(self, request):
        try:
            # loading environment data
            load_dotenv()

            # opening the connection; may want to look into using a connection string dictionary later
            myConnection = mysql.connector.connect(
                host = os.environ.get('DFA_Host'),
                username = os.environ.get('DFA_Username'),
                password = os.environ.get('DFA_Password'),
                database = os.environ.get('DFA_Database')
            )

            # executing the select statement
            myCursor = myConnection.cursor()
            # prepared SQL statement; selecting the user ID that has the given username
            myCursor.execute("""
                SELECT User_ID
                FROM DFA_User
                WHERE Username = %(username)s
            """, { 'username': request.username })

            # fetching scalar from database
            dbResult = myCursor.fetchone()

            # closing connection
            myConnection.close()

            # return query results if it wasn't NULL (None in Python means NULL in SQL)
            if dbResult is not None:
                # result is an array for whatever reason, need to pull the single element out
                return dbResult[0]

            # if result was NULL, return 0 to signal user not found; also add status indicating bad username
            printFormatting.printWarning("User was not found in the database")
            globalStatus.addIssue("BAD_USERNAME_ISSUE")
            return 0
        except Exception as e:
            # print error for debugging, add fail to status array
            printFormatting.printError(str(e))
            globalStatus.addFail("USER_LOOKUP_FAIL")
            raise e

    # takes username, returns user id or 0 if user not found
    def lookupStore(self, request):
        try:
            # loading environment data
            load_dotenv()

            # opening the connection; may want to look into using a connection string dictionary later
            myConnection = mysql.connector.connect(
                host = os.environ.get('DFA_Host'),
                username = os.environ.get('DFA_Username'),
                password = os.environ.get('DFA_Password'),
                database = os.environ.get('DFA_Database')
            )

            # executing the select statement
            myCursor = myConnection.cursor()
            # prepared SQL statement; selecting the store ID that has the given location (not to be confused with store name)
            myCursor.execute("""
                SELECT Store_ID
                FROM DFA_Store
                WHERE Store_Location = %(location)s
            """, { 'location': request.location })

            # fetching scalar from database
            dbResult = myCursor.fetchone()

            # closing connection
            myConnection.close()

            # return query results if it wasn't NULL (None in Python means NULL in SQL)
            if dbResult is not None:
                # result is an array for whatever reason, need to pull the single element out
                return dbResult[0]

            # if result was NULL, return 0 to signal store not found; also add status indicating bad location
            printFormatting.printWarning("Location does not match any store in the database")
            globalStatus.addIssue("BAD_LOCATION_ISSUE")
            return 0
        except Exception as e:
            # print error for debugging, add fail to status array
            printFormatting.printError(str(e))
            globalStatus.addFail("LOCATION_LOOKUP_FAIL")
            raise e

    # takes request, returns array of all the user's matching time slot transactions
    def loadUserTransactions(self, request):
        try:
            # loading environment data
            load_dotenv()

            # for morning and afternoon, time should be after start and before end
            # for night, time should be after start or before end (because night has the midnight cutoff)
            timeCondition = "and"

            # loading time slot cutoffs from env file and swapping condition for the night scenario
            if (request.timeSlot == "Morning"):
                startTime = os.environ.get('Morning_Time')
                endTime = os.environ.get('Afternoon_Time')
            elif (request.timeSlot == "Afternoon"):
                startTime = os.environ.get('Afternoon_Time')
                endTime = os.environ.get('Night_Time')
            else:
                startTime = os.environ.get('Night_Time')
                endTime = os.environ.get('Morning_Time')
                timeCondition = "or"

            # opening the connection; may want to look into using a connection string dictionary later
            myConnection = mysql.connector.connect(
                host = os.environ.get('DFA_Host'),
                username = os.environ.get('DFA_Username'),
                password = os.environ.get('DFA_Password'),
                database = os.environ.get('DFA_Database')
            )

            # executing the select statement
            myCursor = myConnection.cursor()
            # prepared SQL statement; selecting the most recent 50 transactions that are in the time slot from the user
            myCursor.execute("""
                SELECT User_ID, Store_ID, Item_ID
                FROM DFA_Transaction
                WHERE User_ID = %(userId)s
                    and (TIME(Transaction_Time) > %(startTime)s 
                    """ + timeCondition + """ TIME(Transaction_Time) <= %(endTime)s)
                ORDER BY Transaction_Time DESC
                LIMIT %(transactionCount)s
            """,
            {
                'userId': request.userId,
                'startTime': startTime,
                'endTime': endTime,
                'transactionCount': int(os.environ.get('Transaction_Count'))
            })

            # fetching scalar from database
            dbResults = myCursor.fetchall()

            # closing connection
            myConnection.close()

            transactionArray = []

            # adding items to the transaction array
            for transaction in dbResults:
                transactionArray.append(Transaction.Transaction(transaction[0], transaction[1], transaction[2]))

            # return the array; if no transactions match the user, it'll just return an empty array
            return transactionArray
        except Exception as e:
            # printing error and updating status
            printFormatting.printError(str(e))
            globalStatus.addFail("USER_TRANSACTION_FAIL")
            raise e

    # takes request, returns array of all the user's matching time slot transactions
    def loadOtherTransactions(self, request, remainder):
        try:
            # loading environment data
            load_dotenv()

            # for morning and afternoon, time should be after start and before end
            # for night, time should be after start or before end (because night has the midnight cutoff)
            timeCondition = "and"

            # loading time slot cutoffs from env file and swapping condition for the night scenario
            if (request.timeSlot == "Morning"):
                startTime = os.environ.get('Morning_Time')
                endTime = os.environ.get('Afternoon_Time')
            elif (request.timeSlot == "Afternoon"):
                startTime = os.environ.get('Afternoon_Time')
                endTime = os.environ.get('Night_Time')
            else:
                startTime = os.environ.get('Night_Time')
                endTime = os.environ.get('Morning_Time')
                timeCondition = "or"

            # opening the connection; may want to look into using a connection string dictionary later
            myConnection = mysql.connector.connect(
                host = os.environ.get('DFA_Host'),
                username = os.environ.get('DFA_Username'),
                password = os.environ.get('DFA_Password'),
                database = os.environ.get('DFA_Database')
            )

            # executing the select statement
            myCursor = myConnection.cursor()
            # prepared SQL statement; selecting the most recent remainder transactions from other users that are in the time slot
            myCursor.execute("""
                SELECT User_ID, Store_ID, Item_ID
                FROM DFA_Transaction
                WHERE User_ID != %(userId)s
                    and (TIME(Transaction_Time) > %(startTime)s 
                    """ + timeCondition + """ TIME(Transaction_Time) <= %(endTime)s)
                ORDER BY Transaction_Time DESC
                LIMIT %(remainder)s
            """,
            {
                'userId': request.userId,
                'startTime': startTime,
                'endTime': endTime,
                'remainder': remainder
            })

            # fetching scalar from database
            dbResults = myCursor.fetchall()

            # closing connection
            myConnection.close()

            transactionArray = []

            # adding items to the transaction array
            for transaction in dbResults:
                transactionArray.append(Transaction.Transaction(transaction[0], transaction[1], transaction[2]))

            # return the array; if somehow there are no transactions from other users in the day part, it'll just return an empty array
            return transactionArray
        except Exception as e:
            # printing error and updating status
            printFormatting.printError(str(e))
            globalStatus.addFail("OTHER_TRANSACTION_FAIL")
            raise e