from Models import Transaction
from Models import Item
from Models import Store

import os
import mysql.connector
import globalStatus
import printFormatting

# DATABASE.PY: Class that handles accessing the database; alter the environment variables to target another MySQL DB

class Database:
    # this is the constructor; the database object holds the database credentials
    def __init__(self):
        try:
            # reading credentials from the environment file
            self.host = os.environ.get('Database_Host')
            self.username = os.environ.get('Database_Username')
            self.password = os.environ.get('Database_Password')
            self.database = os.environ.get('Database_Database')
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("DATABASE_INIT_FAIL")
            raise e

    # this will connect to the database, returns a MySQLConnection object
    def establishConnection(self):
        try:
            return mysql.connector.connect(
                host = self.host,
                username = self.username,
                password = self.password,
                database = self.database
            )
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("DATABASE_CONNECTION_FAIL")
            raise e

    # loads stores, returns an array of stores for distance calculations
    def loadStores(self):
        try:
            # opening the connection
            myConnection = Database.establishConnection(self)

            # making a cursor
            myCursor = myConnection.cursor()
            # selecting all the relevant data from the store table
            myCursor.execute("""
                SELECT Store_ID, Store_Location, Latitude, Longitude
                FROM DFA_Store
            """)

            # loading all results into a results object
            dbResults = myCursor.fetchall()

            # closing connection
            myConnection.close()

            # initializing empty store array
            storeArray = []

            # adding stores to the store array
            for store in dbResults:
                storeArray.append(Store.Store(store[0], store[1], store[2], store[3]))

            printFormatting.printSuccess("Loaded stores")
            return storeArray
        except Exception as e:
            # print error for debugging, add fail to status array
            printFormatting.printError(str(e))
            globalStatus.addFail("STORE_LOADING_FAIL")
            raise e            

    # takes request, returns user id or 0 if user not found
    def lookupUser(self, request):
        try:
            # opening the connection
            myConnection = Database.establishConnection(self)

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
                printFormatting.printSuccess("User found in the database")
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

    # takes request, returns the user's most recent store ID
    def lookupRecentStore(self, request):
        try:
            # opening the connection
            myConnection = Database.establishConnection(self)

            # making cursor object
            myCursor = myConnection.cursor()
            # prepared SQL statement; selecting the store ID from the user's most recent transaction
            myCursor.execute("""
                SELECT Store_ID
                FROM DFA_Transaction
                WHERE User_ID = %(userId)s
                ORDER BY Transaction_Time DESC
                LIMIT 1                
            """, { 'userId': request.userId })

            # fetching scalar from database
            dbResult = myCursor.fetchone()

            # closing connection
            myConnection.close()

            # return query results if it wasn't NULL (None in Python means NULL in SQL)
            if dbResult is not None:
                printFormatting.printSuccess("Found user's most recent location")
                # result is an array for whatever reason, need to pull the single element out
                return dbResult[0]

            # return 0 to indicate store not found, meaning the user doesn't exist or has no transactions
            printFormatting.printWarning("Could not find user's most recent location")
            globalStatus.addIssue("RECENT_LOCATION_ISSUE")
            return 0
        except Exception as e:
            # print error for debugging, add fail to status array
            printFormatting.printError(str(e))
            globalStatus.addFail("LOCATION_LOOKUP_FAIL")
            raise e

    # takes request, returns the address of the given store ID
    def lookupStoreId(self, storeId):
        try:
            # opening the connection
            myConnection = Database.establishConnection(self)

            # making cursor object
            myCursor = myConnection.cursor()
            # prepared SQL statement; selecting the address from the given store ID
            myCursor.execute("""
                SELECT Store_Location
                FROM DFA_Store
                WHERE Store_ID = %(storeId)s                
            """, { 'storeId': storeId })

            # fetching scalar from database
            dbResult = myCursor.fetchone()

            # closing connection
            myConnection.close()

            # return query results if it wasn't NULL (None in Python means NULL in SQL)
            if dbResult is not None:
                printFormatting.printSuccess("Looked up store address")
                # result is an array for whatever reason, need to pull the single element out
                return dbResult[0]

            # return blank to indicate store not found, meaning the user doesn't exist or has no transactions
            printFormatting.printWarning("Could not find user's most recent location")
            globalStatus.addIssue("RECENT_LOCATION_ISSUE")
            return ""
        except Exception as e:
            # print error for debugging, add fail to status array
            printFormatting.printError(str(e))
            globalStatus.addFail("LOCATION_LOOKUP_FAIL")
            raise e

    # takes request, returns array of all the user's matching time slot transactions
    def loadUserTransactions(self, request):
        try:
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

            # opening the connection
            myConnection = Database.establishConnection(self)

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

            printFormatting.printSuccess("Loaded user transactions")
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

            # opening the connection
            myConnection = Database.establishConnection(self)

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

            printFormatting.printSuccess("Loaded non-user transactions")
            # return the array; if somehow there are no transactions from other users in the day part, it'll just return an empty array
            return transactionArray
        except Exception as e:
            # printing error and updating status
            printFormatting.printError(str(e))
            globalStatus.addFail("OTHER_TRANSACTION_FAIL")
            raise e

    # takes items, modifies them with info directly so no return is needed
    # adds URL and name to list of items using the database
    def lookupItems(self, items):
        try:
            # items need to be sorted by ID because they can't be retrieved from the database ordered by score (since score varies)
            items.sort(key=lambda x: x.id)

            # returns tuple of item IDs (for instance, (1, 2, 3)) and converts it to a string so it can be concatenated into the query
            itemIds = str(Item.getIdTuple(items))

            # opening the connection
            myConnection = Database.establishConnection(self)

            # executing the select statement
            myCursor = myConnection.cursor()
            # prepared SQL statement; selecting the ID, name, and URL for items in the ID array
            myCursor.execute("""
                SELECT Item_ID, Item_Name, Menu_Pic
                FROM DFA_Menu
                WHERE Item_ID IN """ + itemIds + """
                ORDER BY Item_ID""")

            # fetching results from database
            dbResult = myCursor.fetchall()

            # closing connection
            myConnection.close()

            # looping through results and assigning names and URLs
            for index, result in enumerate(dbResult):
                # because items is sorted by ID and the results are queryed by ID, they already line up
                # however, just to be safe, this is double-checked with the if statement
                # if there's a misalignment issue, no data will be assigned to that item
                if items[index].id == int(result[0]):
                    items[index].name = str(result[1])
                    items[index].imgUrl = str(result[2])


            # sorting items by score again so they'll be returned in the right order
            items.sort(key=lambda x: -1*x.score)

            printFormatting.printSuccess("Looked up recommendation items in database")
            # if no items are found, the engine won't return useful info to the front end, so it's considered a full failure
            if dbResult is None:
                raise e
        except Exception as e:
            # print error for debugging, add fail to status array
            printFormatting.printError(str(e))
            globalStatus.addFail("ITEMS_LOOKUP_FAIL")
            raise e    