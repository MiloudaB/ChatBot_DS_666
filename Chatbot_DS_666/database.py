#dependencies
import sqlite3


class DataBaseInitiator:
    ## initialize the database connection 
    def __init__(self, database_name="Tracking.sqlite"):
        self.database_name = database_name
        try :
            self.connector = sqlite3.connect(database_name, check_same_thread=False)
        except Exception as exception:
            print(exception)
    ##setup the database by creating the necessery tables and its columns
    def setup(self):
        query = "CREATE TABLE IF NOT EXISTS Tracking (id PRIMARY KEY, tracked_code INTEGER UNIQUE)"
        self.connector.execute(query)
        self.connector.commit()
    ##check if the giving code is already in the database
    def check(self, tracked_code):
        cursor = self.connector.cursor()
        cursor.execute("SELECT COUNT(1) FROM Tracking WHERE tracked_code=:tracked_code",{'tracked_code':tracked_code})
        result = cursor.fetchone()
        return result


if __name__ == 'main':
    print("This file is not useful on its own !!")