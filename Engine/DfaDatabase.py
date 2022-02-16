from dotenv import load_dotenv
from flask import abort
import os
import mysql.connector

#this can be where the class ends up; I have some concerns about file structure though
class DfaDatabase:
    def loadItems():
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
            myCursor.execute("SELECT * FROM DFA_Menu")

            # loading and print the results
            dbResults = myCursor.fetchall()
            for x in dbResults:
                print(x)

            # closing the connection
            myConnection.close()
        except:
            # print issue to terminal and return 500 to requester
            print("500 ERROR: Failed to load transactions")
            abort(500, "500 ERROR: Failed to load transactions")