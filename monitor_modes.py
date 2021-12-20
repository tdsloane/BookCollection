"""
    The classes and functions herein are for the express purpose
    of creating and displaying menus while also connecting menus to eachother.
"""
import pyodbc
import pandas as pd
from time import sleep
from screen_tools import ScreenTools


class MainMenu:

    def startMenu(): 
        """
            This function displays the main menu.
        """
        ScreenTools.screen_clear()
        print()
        print('*' * 20)
        print('Welcome to the\nSloane Book System!')
        print('*' * 20)
        sleep(5)
        ScreenTools.screen_clear()

        print('*' * 20)
        print('What would you like to do?')
        print('*' * 20)
        print()
        print('* To Query the library:\n* Press 1')
        print()
        print('* To Add a book:\n* Press 2')
        print()
        print('* To Mark a book as read:\n* Press 3')
        print()
        print('* To Remove a book from the system:\n* Press 4')
        print()
        print('* To Quit:\n* Press 5')
        print()
        user_input = int(input())
        try:
            if user_input > 5:
                print("Please enter a number 1-5")
                sleep(5)
                MainMenu.startMenu()
        except ValueError as e:
            print(f"{e} Please enter a number 1-5.")
            sleep(5)
            MainMenu.startMenu()
        print("Int Check")
        Chooser.mainChooser(user_input) 


    def queryMenu():
        """
            This function displays the query menu.
        """
        ScreenTools.screen_clear()
        print('*' * 20)
        print('What would you like to query?')
        print('*' * 20)
        print()
        print('* To view unread books:\n* Press 1')
        print()
        print('* To view all read books:\n* Press 2')
        print()
        print('* To view all books or print a count:\n* Press 3') # Two Branches
        print()
        print('* To create a custom query:\n* Press 4')
        print()
        user_input = int(input())
        Chooser.queryChooser(user_input)

    def addBook():
        """
            This function uses an insert statement to add a book to the db.
        """
        ScreenTools.screen_clear()
        print('*' * 20)
        print("So, you want to add a book to the list?")
        print("Say yes or no.")
        print('*' * 20)
        print()
        user_input = input()
        if user_input in Chooser.sayNay:
            MainMenu.queryMenu()
        elif user_input in Chooser.sayYay:
            DBcontrol.askBookInfo()


    def markBook():
        """
            This function uses an update statement to update a books read status.
        """
        ScreenTools.screen_clear()
        print('*' * 20)
        print("So, you want to mark a book as read?")
        print("Say yes or no.")
        print('*' * 20)
        print()
        user_input = input()
        if user_input in Chooser.sayNay:
            MainMenu.queryMenu()
        elif user_input in Chooser.sayYay:
            ScreenTools.screen_clear()
            print('*' * 20)
            print("Congradulations!!")
            print("Please enter the ISBN of the book you read.")
            print('*' * 20)
            print()
            user_input = int(input())
            DBcontrol.sendMarkQuery(user_input)


    def deleteBook():
        """
            This function uses an delete statement to remove a book from the db.
        """
        ScreenTools.screen_clear()
        print('*' * 20)
        print("So, you want to remove a book?")
        print("Say yes or no.")
        print('*' * 20)
        print()
        user_input = input()
        if user_input in Chooser.sayNay:
            MainMenu.queryMenu()
        elif user_input in Chooser.sayYay:
            # This is where we will delete a book.
            pass


class QueryMenu:

    def viewBooks():
        ScreenTools.screen_clear()
        # Offer a look at the list
        print('*' * 20)
        print('Would you like to see the list of all books?\nYes or No?')
        print('*' * 20)
        user_input = input()

        # If not, then offer a count
        if user_input in Chooser.sayNay:
            print('*' * 20)
            print('Would you like a total count of all books?\nYes or No?')
            print('*' * 20)
            user_input = input()

            if user_input in Chooser.sayNay:
                MainMenu.startMenu()
            # Access db
            elif user_input in Chooser.sayYay:
                _ = 2
                DBcontrol.viewBookControl(_)
            elif user_input not in (Chooser.sayYay + Chooser.sayNay):
                print("Please answer yes or no.")
                QueryMenu.viewBooks()
        elif user_input in Chooser.sayYay:
            _ = 1
            DBcontrol.viewBookControl(_)
        elif user_input not in (Chooser.sayYay + Chooser.sayNay):
                print("Please answer yes or no.")
                QueryMenu.viewBooks()

    def viewUnreadBooks():
        ScreenTools.screen_clear()
        
        # Offer a look at the list
        print('*' * 20)
        print('Would you like to see the list of unread books?\nYes or No?')
        print('*' * 20)
        user_input = input()

        # If not, then offer a count
        if user_input in Chooser.sayNay:
            print('*' * 20)
            print('Would you like a total count of unread books?\nYes or No?')
            print('*' * 20)
            user_input = input()
            if user_input in Chooser.sayNay:
                MainMenu.startMenu()
            # Access db
            elif user_input in Chooser.sayYay:
                DBcontrol.unreadBookControl()

        # Content Checks for user input
            elif user_input not in (Chooser.sayYay + Chooser.sayNay):
                print("Please answer yes or no.")
                QueryMenu.viewUnreadBooks()   
        elif user_input not in (Chooser.sayYay + Chooser.sayNay):
                print("Please answer yes or no.")
                QueryMenu.viewUnreadBooks()

    def viewReadBooks():
        ScreenTools.screen_clear()
        
        # Offer a look at the list
        print('*' * 20)
        print('Would you like to see the list of read books?\nYes or No?')
        print('*' * 20)
        user_input = input()

        # If not, then offer a count
        if user_input in Chooser.sayNay:
            print('*' * 20)
            print('Would you like a total count of books read?\nYes or No?')
            print('*' * 20)
            user_input = input()
            if user_input in Chooser.sayNay:
                MainMenu.startMenu()
            # Access db
            elif user_input in Chooser.sayYay:
                DBcontrol.readBookControl()

        # Content Checks for user input
            elif user_input not in (Chooser.sayYay + Chooser.sayNay):
                print("Please answer yes or no.")
                QueryMenu.viewReadBooks()     
        elif user_input not in (Chooser.sayYay + Chooser.sayNay):
                print("Please answer yes or no.")
                QueryMenu.viewReadBooks()


class Chooser:
    """
        This class houses chooser functions to aid navigation.
    """
    sayNay = ['N', 'n', 'no', 'No']
    sayYay = ['Y', 'y', 'yes', 'Yes']

    def mainChooser(_):
        """
            This function is a hub for choices on the main menu.
        """
        if _ == 1:
            MainMenu.queryMenu()
        elif _ == 2:
            MainMenu.addBook()
        elif _ == 3:
            MainMenu.markBook()
        elif _ == 4:
            MainMenu.deleteBook()
        elif _ == 5:
            ScreenTools.screen_clear()
            print('*' * 20)
            print("Goodbye! Happy Reading!")
            print('*' * 20)
            ScreenTools.running = False

    def queryChooser(_):
        """
            This function is a hub for choices on the query menu.
        """
        if _ == 1:
            QueryMenu.viewUnreadBooks()
        elif _ == 2:
            QueryMenu.viewReadBooks()
        elif _ == 3:
            QueryMenu.viewBooks()
        elif _ == 4:
            # Begin a custom query on the db
            pass


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

    def sendInsertQuery(query, listed_data, isbn):
        """
            sendInsertQuery() creates a connection string and connects to SQL Server then
            the insert query is executed. A confirmation prints as well as the row created in the table.
        """
        # Contact the db and make the query
        with pyodbc.connect(DBcontrol.CONNECTION_STRING) as conx:
            cursor = conx.cursor()
            cursor.execute(query, listed_data)
            # Commit changes | commented out for testing
            cursor.commit()
            print("Insert Commited")
            print()

            # Create new query for creation of printed check
            checking_query = "SELECT * FROM [PersonalLibrary].[dbo].[BookShelf]"
            # fetch data 
            records = cursor.execute(checking_query).fetchall()
            # Define column names
            columns = [column[0] for column in cursor.description]
            # Dump the data into a dataframe
            df = pd.DataFrame.from_records(
                data=records,
                columns=columns
            )

            ScreenTools.screen_clear()
            print('*' * 20)
            print('Book has been added!')
            print('*' * 20)
            # Print the new row
            filt = (df['ISBN'] == int(isbn))
            print(df.loc[filt])
            print()

    def sendFullQuery(query):
        """
            sendFullQuery() creates a connection string and creates a dataframe.
            It then displays the entire library from the dataframe.
        """
        pd.set_option('display.max_rows', 500)
        # Contact the db and make the query
        with pyodbc.connect(DBcontrol.CONNECTION_STRING) as conx:
            cursor = conx.cursor()
            # extract data from executed query
            records = cursor.execute(query).fetchall()
            # Define column names
            columns = [column[0] for column in cursor.description]
            # Dump the data into a dataframe
            df = pd.DataFrame.from_records(
                data=records,
                columns=columns
            )
            selection = df[['Title', 'Author', 'Read_Yet']]
            ScreenTools.screen_clear()
            print('*' * 20)
            print('Look upon my Library!')
            print('*' * 20)
            print(selection)

    def sendCountQuery(query):
        """
            sendCountQuery() creates a connection string and creates a dataframe.
            It then displays a count of books in the library from the dataframe.
        """
        # Contact the db and make the query
        with pyodbc.connect(DBcontrol.CONNECTION_STRING) as conx:
            # Create a cursor object
            cursor = conx.cursor()
            # extract data from executed query
            records = cursor.execute(query).fetchall()
            # Define column names
            columns = [column[0] for column in cursor.description]
            # Dump the data into a dataframe
            df = pd.DataFrame.from_records(
                data=records,
                columns=columns
            )
            ScreenTools.screen_clear()
            num_rows = df.shape[0]
            print('*' * 20)
            print(f"The library currently has {num_rows} books.")
            print('*' * 20)
            print()

    def sendMarkQuery(isbn):
        """
            sendInsertQuery() creates a connection string and connects to SQL Server then
            the insert query is executed. A confirmation prints as well as the row created in the table.
        """
        # Contact the db and make the query
        with pyodbc.connect(DBcontrol.CONNECTION_STRING) as conx:
            # Create a cursor object
            cursor = conx.cursor()
            # Create new query for creation of printed check
            checking_query = "SELECT * FROM [PersonalLibrary].[dbo].[BookShelf]"
            # fetch data 
            records = cursor.execute(checking_query).fetchall()
            # Define column names
            columns = [column[0] for column in cursor.description]
            # Dump the data into a dataframe
            df = pd.DataFrame.from_records(
                data=records,
                columns=columns
            )

            ScreenTools.screen_clear()
            print('*' * 20)
            print('Is this the book you wish to mark?')
            print('*' * 20)
            # Print the new row
            filt = (df['ISBN'] == isbn)
            new_df = df.loc[filt]
            print(new_df[['Title', 'Author', 'Read_Yet']])
            print()
            user_input = input()
            if user_input in Chooser.sayYay:
                mark_read = 1
                cursor.execute("UPDATE [PersonalLibrary].[dbo].[BookShelf] SET [Read_Yet] = ? WHERE [ISBN] = ?", mark_read, isbn)
                cursor.commit()
                checking_query = "SELECT * FROM [PersonalLibrary].[dbo].[BookShelf]"
                # fetch data 
                records = cursor.execute(checking_query).fetchall()
                # Define column names
                columns = [column[0] for column in cursor.description]
                # Dump the data into a dataframe
                df = pd.DataFrame.from_records(
                    data=records,
                    columns=columns
                )
                filt = (df['ISBN'] == isbn)
                new_df = df.loc[filt]
                print()
                print('*' * 20)
                print('Here are the results:')
                print('*' * 20)
                print(new_df[['Title', 'Author', 'Read_Yet']])
                print()
                print('*' * 20)
                print('Would you like to mark another book?')
                print('*' * 20)
                user_input = input()
                if user_input in Chooser.sayYay:
                    MainMenu.markBook()
                elif user_input in Chooser.sayNay:
                    MainMenu.startMenu()

    def viewBookControl(_):
        """
            Controls the sql query requierd to view the entire library or count the total of books. Creates a connection
        """
        
        query = "SELECT * FROM [PersonalLibrary].[dbo].[BookShelf]" 
        
        # User wants to see all books.
        if _ == 1:
            DBcontrol.sendFullQuery(query)
        # User wants to see a count of books.
        elif _ == 2:
            DBcontrol.sendCountQuery(query)

        # Allow the user to continue.
        print('*' * 20)
        print('Would you like to continue?')
        print('*' * 20)
        user_input = input()
        if user_input in Chooser.sayYay:
            MainMenu.startMenu()
        elif user_input in Chooser.sayNay:
            ScreenTools.running = False
            
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
            ScreenTools.running = False

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
            ScreenTools.running = False

        """
            This function asks the user for information about the publisher they want to add.
        """
        ScreenTools.screen_clear()
        print('*' * 20)
        print('Adding a Publisher')
        print('*' * 20)
        print("Would you like to continue further?")
        print("I will need to ask you a series of questions to continue.")
        print()
        user_input = input()

        if user_input in Chooser.sayYay:
            ScreenTools.screen_clear()
            
            print('*' * 20)
            print('Who is the Publisher?')
            print('*' * 20)
            print()
            pub = input()
            print()

            print('*' * 20)
            print('Where are they located?')
            print('*' * 20)
            print()
            pub_loc = input()
            print()

            
            sleep(2)
            ScreenTools.screen_clear()
            print()
            print('*' * 20)
            print('Here is what you have registered.\nIs this correct? ')
            print('*' * 20)
            print()
            
            print(f"Publisher: {pub}\nLocation: {pub_loc}")
            print()
            print('*' * 20)

            user_input = input("Is this information correct?\nPlease say yes or no.\n")
            if user_input in Chooser.sayYay:
                # Send it out!
                DBcontrol.addToPublisherTable(pub, pub_loc)
            # Send them back if not correct.
            elif user_input in Chooser.sayNay:
                DBcontrol.askPublisherInfo()

    def askBookInfo():
        """
            This function asks the user for information about the book they want to add.
        """
        ScreenTools.screen_clear()
        print('*' * 20)
        print('Adding a Book')
        print('*' * 20)
        print("Would you like to continue further?")
        print("I will need to ask you a series of questions to continue.")
        print()
        user_input = input()

        if user_input in Chooser.sayYay:
            ScreenTools.screen_clear()
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

            print('*' * 20)
            print('What is the genre?')
            print('*' * 20)
            print()
            genre = input()
            print()
            
            ScreenTools.screen_clear()

            print('*' * 20)
            print('What language is the book in?')
            print('*' * 20)
            print()
            lang = input()
            print()

            print('*' * 20)
            print('How many pages are in the book?')
            print('*' * 20)
            print()
            pages = input()
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
                collection_name = input()
            elif user_input in Chooser.sayNay:
                collection_name = ''

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
            ScreenTools.screen_clear()
            print()
            print('*' * 20)
            print('Here is what you have registered.\nIs this correct? ')
            print('*' * 20)
            print()
            
            print(f"ISBN: {isbn}\nTitle: {title}\nAuthor: {author}\nGenre: {genre}\nLanguage: {lang}\nPages: {pages}\nRead: {read_yet}\nPublisher: {pub}\nCollection: {collection_name}\nYear Published: {pub_year}")
            print()
            print('*' * 20)

            user_input = input("Is this information correct?\nPlease say yes or no.\n")
            if user_input in Chooser.sayYay:
                # Send it out!
                DBcontrol.addToBookTable(isbn, title, author, genre, lang, pages, read_yet, pub, collection_name, pub_year)
            # Send them back if not correct.
            elif user_input in Chooser.sayNay:
                DBcontrol.askBookInfo()

        elif user_input in Chooser.sayNay:
            MainMenu.startMenu()

        # Allow the user to continue.
        print('*' * 20)
        print('Would you like to continue adding books?')
        print('*' * 20)
        print()
        user_input = input()
        if user_input in Chooser.sayYay:
            DBcontrol.askBookInfo()
        elif user_input in Chooser.sayNay:
            MainMenu.startMenu()

    def addToBookTable(isbn, title, author, genre, lang, pages, read_yet, pub, collection_name, pub_year):
        """
            Adds a book to the db using user input.
        """

        # [PersonalLibrary].[dbo].[BookShelf] ????
        # Query must be redefined before runtime.
        query_book_table = f"""
        INSERT INTO [PersonalLibrary].[dbo].[BookShelf] 
        (
            [ISBN], 
            [Title], 
            [Author], 
            [Genre], 
            [Lang], 
            [Pages], 
            [Read_Yet], 
            [Publisher], 
            [Collection_Name], 
            [Pub_Year]
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """


        data_values = (
            isbn, 
            title, 
            author,
            genre,
            lang,
            pages, 
            read_yet, 
            pub, 
            collection_name, 
            pub_year
        )

        # params = list(tuple(row) for row in data_values.values)

        DBcontrol.sendInsertQuery(query_book_table, data_values, isbn)

    def deleteBook():
        """
            This function will remove a book from the db.
        """
        ScreenTools.screen_clear()
        print('*' * 20)
        print('Removing a Book')
        print('*' * 20)
        print("Would you like to continue further?")
        print()
        user_input = input()
        if user_input in Chooser.sayYay:
            ScreenTools.screen_clear()
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