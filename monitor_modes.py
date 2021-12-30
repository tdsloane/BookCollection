"""
    The classes and functions herein are for the express purpose
    of creating and displaying menus while also connecting menus to eachother.
"""
from numpy import ushort
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
        sleep(2)
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
            DBcontrol.addBookControl()
        elif _ == 3:
            MainMenu.markBook()
        elif _ == 4:
            DBcontrol.deleteBook()
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
            ScreenTools.screen_clear()
            print('*' * 20)
            print('Tell me what you want to see!')
            print('*' * 20)
            print()
            print('* View a list of unread books:\n* Press 1')
            print()
            print('* View a count of unread books:\n* Press 2')
            print()
            user_input = int(input())

            DBcontrol.unreadBookControl(user_input)

        elif _ == 2:
            ScreenTools.screen_clear()
            print('*' * 20)
            print('Tell me what you want to see!')
            print('*' * 20)
            print()
            print('* View a list of all read books:\n* Press 1')
            print()
            print('* View a count of all read books:\n* Press 2')
            print()
            user_input = int(input())

            DBcontrol.readBookControl(user_input)

        elif _ == 3:
            ScreenTools.screen_clear()
            print('*' * 20)
            print('What do you want to view?')
            print('*' * 20)
            print()
            print('* View a list of all books:\n* Press 1')
            print()
            print('* View a count of all books:\n* Press 2')
            print()
            user_input = int(input())

            DBcontrol.viewBookControl(user_input)

        elif _ == 4:
            ScreenTools.screen_clear()
            print('*' * 20)
            print("What is your query?\nPlease note that [Brackets] must be used around column names.\nAlso note that 'Parentheses' are required for word values.")
            print('!! This will be inserted into an SQL WHERE clause. !!')
            print('*' * 20)
            print()
            user_input = input()

            DBcontrol.customQueryControl(user_input)


class DBcontrol:
    """
        All Functions within this class have access to the database to send and retrieve queries.
    """

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
        print("Display Settings Activated")
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
            ScreenTools.screen_clear()
            selection = df[['Title', 'Author', 'Read_Yet']]
            print('*' * 20)
            print('Look upon my Library!')
            print('*' * 20)
            print(selection)
            print()


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
        print('Would you like to close the program?')
        print('*' * 20)
        user_input = input()
        if user_input in Chooser.sayYay:
            ScreenTools.running = False
        elif user_input in Chooser.sayNay:
            MainMenu.startMenu()
            
    def unreadBookControl(_):
        """
            Controls the sql query requierd to view all unread books in the db.
        """
        query = "SELECT * FROM [PersonalLibrary].[dbo].[BookShelf] WHERE [Read_Yet] = 0" 
        
        # User wants to see all books.
        if _ == 1:
            DBcontrol.sendFullQuery(query)
        # User wants to see a count of books.
        elif _ == 2:
            DBcontrol.sendCountQuery(query)

        # Allow the user to continue.
        print('*' * 20)
        print('Would you like to close the program?')
        print('*' * 20)
        user_input = input()
        if user_input in Chooser.sayYay:
            ScreenTools.running = False
        elif user_input in Chooser.sayNay:
            MainMenu.startMenu()

    def readBookControl(_):
        """
            Controls the sql query requierd to view all read books in the db.
        """
        query = "SELECT * FROM [PersonalLibrary].[dbo].[BookShelf] WHERE [Read_Yet] = 1" 
        
        # User wants to see all books.
        if _ == 1:
            DBcontrol.sendFullQuery(query)
        # User wants to see a count of books.
        elif _ == 2:
            DBcontrol.sendCountQuery(query)

        # Allow the user to continue.
        print('*' * 20)
        print('Would you like to close the program?')
        print('*' * 20)
        user_input = input()
        if user_input in Chooser.sayYay:
            ScreenTools.running = False
        elif user_input in Chooser.sayNay:
            MainMenu.startMenu()

    def addBookControl():
        """
            This function asks the user for information about the book they want to add.
        """
        ScreenTools.screen_clear()
        print('*' * 20)
        print("I will need to ask ten questions.")
        print("This may take a while, would you like to continue?")
        print("Say yes or no.")
        print('*' * 20)
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
                DBcontrol.addBookControl()

        elif user_input in Chooser.sayNay:
            MainMenu.startMenu()

        # Allow the user to continue.
        print('*' * 20)
        print('Would you like to continue adding books?')
        print('*' * 20)
        print()
        user_input = input()
        if user_input in Chooser.sayYay:
            DBcontrol.addBookControl()
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
        print("So, you want to remove a book?")
        print("Say yes or no.")
        print('*' * 20)
        print()
        user_input = input()
        if user_input in Chooser.sayNay:
            MainMenu.queryMenu()
        elif user_input in Chooser.sayYay:
            ScreenTools.screen_clear()
            print('*' * 40)
            print('What is the isbn of the book you would like to remove?')
            print('*' * 40)
            print()
            isbn = input()

            with pyodbc.connect(DBcontrol.CONNECTION_STRING) as conx:
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

                filt = (df['ISBN'] == int(isbn))
                print(df.loc[filt])
                print()
                print('*' * 20)
                print("Is this the book you wish to remove?")
                print('*' * 20)
                print()
                user_input = input()
                if user_input in Chooser.sayYay:
                    # Query must be redefined before runtime.
                    # Mutliple queries might need to be run.
                    delete_query = f"DELETE FROM [PersonalLibrary].[dbo].[BookShelf] WHERE [ISBN] = {isbn}"
                    cursor.execute(delete_query)
                    cursor.commit()
                    ScreenTools.screen_clear()
                    print('*' * 20)
                    print("Book removed from list.")
                    print('*' * 20)
                elif user_input in Chooser.sayNay:
                    DBcontrol.deleteBook()


    def customQueryControl(_):
        """
            This function allows for the user to enter custom information into 
        """
        # Create the query based on user input.
        open_query = f"SELECT * FROM [PersonalLibrary].[dbo].[BookShelf] WHERE {_}"

        # Contact the db and make the query
        with pyodbc.connect(DBcontrol.CONNECTION_STRING) as conx:
            cursor = conx.cursor()
            # extract data from executed query
            records = cursor.execute(open_query).fetchall()
            # Define column names
            columns = [column[0] for column in cursor.description]
            # Dump the data into a dataframe
            df = pd.DataFrame.from_records(
                data=records,
                columns=columns
            )
            selection = df[['Title', 'Author', 'Pages', 'Read_Yet']]
            print('*' * 20)
            print('Here are your results:')
            print('*' * 20)
            print(selection)
            print()

        print('*' * 20)
        print('Would you like to enter another query?')
        print('*' * 20)
        print()
        user_input = input()
        if user_input in Chooser.sayYay:
            Chooser.queryChooser(4)
        elif user_input in Chooser.sayNay:
            MainMenu.startMenu()