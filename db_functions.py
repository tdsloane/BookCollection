"""
    These functions act as the add, delete, and edit functions to the database.
    They are called by the menus in monitor_modes.
"""
import pyodbc
import pandas as pd
from monitor_modes import MainMenu, Chooser
from screen_tools import Tools
# from main import LibStart


class DBcontrol:

    # Connection string components
    DRIVER = '{ODBC Driver 17 for SQL Server}'
    SERVER_NAME = 'HQ-GIIOKUS\SQLEXPRESS'
    DATABASE_NAME = 'PersonalLibrary'

    # Define connection string
    CONNECTION_STRING = """
    Driver={driver}; 
    Server={server};
    Database={database}; 
    Trusted_Connection=yes;
    """.format(
        driver = DRIVER,
        server = SERVER_NAME,
        database = DATABASE_NAME
    )

    def sendQuery(query):
        # Contact the db and make the query
        with pyodbc.connect(DBcontrol.CONNECTION_STRING) as conx:
            cursor = conx.cursor()
            cursor.execute(query)
            # fetch data 
            records = cursor.fetchall()

            # Define column names
            columns = [column[0] for column in cursor.description]

            # Dump the data into a dataframe
            dump = pd.DataFrame.from_records(
                data=records,
                columns=columns
            )

            # Print the head
            print(dump.head())

            # cursor.commit()
        

    def viewBookControl():
        """
            Controls the sql query requierd to view the entire library.
        """
        query = "SELECT Title, Author, Genre, Read FROM PersonalLibrary" # Query must be redefined before runtime.

        DBcontrol.sendQuery(query)

        # Allow the user to continue.
        print("Would you like to continue further?")
        user_input = input()
        if user_input in Chooser.sayYay:
            MainMenu.startMenu()
        elif user_input in Chooser.sayNay:
            LibStart.running = False

    def unreadBookControl():
        """
            Controls the sql query requierd to view all unread books in the db.
        """
        query = "SELECT Title, Author, Genre, Read FROM PersonalLibrary" # Query must be redefined before runtime.

        DBcontrol.sendQuery(query)

        # Allow the user to continue.
        print("Would you like to continue further?")
        user_input = input()
        if user_input in Chooser.sayYay:
            MainMenu.startMenu()
        elif user_input in Chooser.sayNay:
            LibStart.running = False

    def readBookControl():
        """
            Controls the sql query requierd to view a list of all books read.
        """
        query = "SELECT Title, Author, Genre, Read FROM PersonalLibrary" # Query must be redefined before runtime.

        DBcontrol.sendQuery(query)

        # Allow the user to continue.
        print("Would you like to continue further?")
        user_input = input()
        if user_input in Chooser.sayYay:
            MainMenu.startMenu()
        elif user_input in Chooser.sayNay:
            LibStart.running = False


    def addBookInfo():
        """
            This function controls the text for the addBook function for readability.
        """
        Tools.screen_clear()
        print('*' * 20)
        print('Adding a Book')
        print('*' * 20)
        print("Would you like to continue further?")
        print("I will need to ask you a series of questions to continue.")
        print()
        user_input = input()

        if user_input in Chooser.sayYay:
            Tools.screen_clear()
            print('*' * 20)
            print('What is the ISBN?')
            print('*' * 20)
            print()
            isbn = input()
            print()

            print('*' * 20)
            print('What is the title?')
            print('*' * 20)
            print()
            title = input()
            print()

            print('*' * 20)
            print('Who is the Author?')
            print('*' * 20)
            print()
            author = input()
            print()

            # print('*' * 20)
            # print('What country are they from?')
            # print('*' * 20)
            # print()
            # author_loc = input()
            # print()

            print('*' * 20)
            print('How many pages is the book?')
            print('*' * 20)
            print()
            pages = input()
            print()

            print('*' * 20)
            print('What is the genre?')
            print('*' * 20)
            print()
            genre = input()
            print()

            print('*' * 20)
            print('Who is the Publisher?')
            print('*' * 20)
            print()
            pub = input()
            print()

            print('*' * 20)
            print('What year was it published?')
            print('*' * 20)
            print()
            pub_year = input()
            print()

            print('*' * 20)
            print('What language is the book in?')
            print('*' * 20)
            print()
            lang = input()
            print()

            print('*' * 20)
            print('Is it part of a collection?')
            print('*' * 20)
            print()
            user_input = input()
            if user_input in Chooser.sayYay:
                print()
                print('*' * 20)
                print('Which collection?')
                print('*' * 20)
                print()
                collection = input()
            elif user_input in Chooser.sayNay:
                collection = ''

            print()
            print('*' * 20)
            print('Have you read this book yet?')
            print('*' * 20)
            print()
            user_input = input()
            if user_input in Chooser.sayYay:
                read_yet = 1
            elif user_input in Chooser.sayNay:
                read_yet = 0

            sleep(2)
            Tools.screen_clear()
            print()
            print('*' * 20)
            print('Here is what you have registered.\nIs this correct? ')
            print('*' * 20)
            print()
            
            print(f"ISBN: {isbn}\nTitle: {title}\nAuthor: {author}\nPages: {pages}\nGenre: {genre}\nPublisher: {pub}\nCollection: {collection}\nRead: {read_yet}\nLanguage: {lang}\nYear Published: {pub_year}")
            print()

            user_input = input("Is this information correct?\nPlease say yes or no.")
            if user_input in Chooser.sayYay:
                # Send it out!
                return isbn, title, author, pages, genre, pub, collection, read_yet, lang, pub_year
            # Send them back if not correct.
            elif user_input in Chooser.sayNay:
                DBcontrol.addBookInfo()

        elif user_input in Chooser.sayNay:
            MainMenu.startMenu()


    def addBook(isbn, title, author, pages, genre, pub, collection, read_yet, lang, pub_year, author_loc):
        """
            Adds a book to the db using user input.
        """

        # Query must be redefined before runtime.
        # Mutliple queries might need to be run.
        query = f"""
        INSERT INTO PersonalLibrary (ISBN, Title, Author, Pages, Genre, Publisher, Collection, Read, Language, Pub_Year)
        VALUES({isbn}, {title}, {author}, {pages}, {genre}, {pub}, {collection}, {read_yet}, {lang}, {pub_year})"""

        DBcontrol.sendQuery(query)

        # Allow the user to continue.
        print("Would you like to continue further?")
        user_input = input()
        if user_input in Chooser.sayYay:
            MainMenu.startMenu()
        # elif user_input in Chooser.sayNay:
        #     LibStart.running = False


    def markBook():
        """
            This function will mark a book as read.
        """
        Tools.screen_clear()
        print('*' * 20)
        print('Another book bites the dust!\nLets mark it down!')
        print('*' * 20)
        print("Would you like to continue further?")
        print()
        user_input = input()
        if user_input in Chooser.sayYay:
            Tools.screen_clear()
            print('*' * 40)
            print('What is the isbn of the book you would like to mark as read?')
            print('*' * 40)
            print()
            isbn = input()
            print(f"The ISBN you entered was:\n{isbn}")
            print("Was this correct?")
            if user_input in Chooser.sayYay:
                # Query must be redefined before runtime.
                # Mutliple queries might need to be run.
                query = f"UPDATE WHERE {isbn} INTO PersonalLibrary" 

                DBcontrol.sendQuery(query)

                # Second query will display the books information.
                query = "SELECT * FROM Database"

                DBcontrol.sendQuery(query)

            elif user_input in Chooser.sayNay:
                DBcontrol.markBook()
        elif user_input in Chooser.sayNay:
            MainMenu.queryMenu()

    def deleteBook():
        """
            This function will remove a book from the db.
        """
        Tools.screen_clear()
        print('*' * 20)
        print('Removing a Book')
        print('*' * 20)
        print("Would you like to continue further?")
        print()
        user_input = input()
        if user_input in Chooser.sayYay:
            Tools.screen_clear()
            print('*' * 40)
            print('What is the isbn of the book you would like to remove?')
            print('*' * 40)
            print()
            isbn = input()
            print(f"The ISBN you entered was:\n{isbn}")
            print("Was this correct?")
            if user_input in Chooser.sayYay:
                # Query must be redefined before runtime.
                # Mutliple queries might need to be run.
                query = f"DELETE WHERE {isbn} INTO PersonalLibrary" 

                DBcontrol.sendQuery(query)

                # Second query will display the books information.
                query = "SELECT * FROM Database"

                DBcontrol.sendQuery(query)

            elif user_input in Chooser.sayNay:
                DBcontrol.markBook()
        elif user_input in Chooser.sayNay:
            MainMenu.queryMenu()