"""
    The classes and functions herein are for the express purpose
    of creating and displaying menus while also connecting menus to eachother.
"""
from os import altsep
import pyodbc
import pandas as pd
from time import sleep
from screen_tools import Tools


class MainMenu:

    def startMenu(): 
        """
            This function displays the main menu.
        """
        Tools.screen_clear()
        print()
        print('*' * 20)
        print('Welcome to the\nTDSloane Book System!')
        print('*' * 20)
        sleep(2)
        Tools.screen_clear()

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
        try:
            user_input = int(input())
            if user_input < 6:
                Chooser.mainChooser(user_input) 
            else:
                raise ValueError
        except ValueError:
            Tools.screen_clear()
            print('*' * 20)
            print("Please enter a number 1-5.")
            print('*' * 20)
            sleep(3)
            MainMenu.startMenu()
        
        


    def queryMenu():
        """
            This function displays the query menu.
        """
        Tools.screen_clear()
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
        try:
            user_input = int(input())
            if user_input < 5:
                Chooser.queryChooser(user_input)
            else:
                raise ValueError
        except ValueError:
            Tools.screen_clear()
            print('*' * 20)
            print("Please enter a number 1-5.")
            print('*' * 20)
            sleep(3)
            MainMenu.queryMenu()
        


    def markBook():
        """
            This function uses an update statement to update a books read status.
        """
        Tools.screen_clear()
        print('*' * 20)
        print("So, you want to mark a book as read?")
        print("Say yes or no.")
        print('*' * 20)
        print()
        try:
            user_input = str(input())
            if user_input in Chooser.sayNay:
                MainMenu.queryMenu()
            elif user_input in Chooser.sayYay:
                Tools.screen_clear()
                print('*' * 20)
                print("Congradulations!!")
                print("Please enter the ISBN of the book you read.")
                print('*' * 20)
                print()
                user_input = int(input())
                DBcontrol.sendMarkQuery(user_input)
            else:
                raise ValueError
        except ValueError:
            Tools.screen_clear()
            print('*' * 20)
            print("Please enter yes or no.")
            print('*' * 20)
            sleep(3)
            MainMenu.startMenu()
        

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
            Tools.screen_clear()
            print('*' * 20)
            print("Goodbye! Happy Reading!")
            print('*' * 20)
            Tools.running = False

    def queryChooser(_):
        """
            This function is a hub for choices on the query menu.
        """
        if _ == 1:
            Tools.screen_clear()
            print('*' * 20)
            print('Tell me what you want to see!')
            print('*' * 20)
            print()
            print('* View a list of unread books:\n* Press 1')
            print()
            print('* View a count of unread books:\n* Press 2')
            print()
            try:
                user_input = int(input())
                if user_input < 3:
                    DBcontrol.unreadBookControl(user_input)
                else:
                    raise ValueError
            except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter a number 1-2.")
                print('*' * 20)
                sleep(3)
                Chooser.queryChooser(1)

            

        elif _ == 2:
            Tools.screen_clear()
            print('*' * 20)
            print('Tell me what you want to see!')
            print('*' * 20)
            print()
            print('* View a list of all read books:\n* Press 1')
            print()
            print('* View a count of all read books:\n* Press 2')
            print()
            
            try:
                user_input = int(input())
                if user_input < 3:
                    DBcontrol.readBookControl(user_input)
                else:
                    raise ValueError
            except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter a number 1-2.")
                print('*' * 20)
                sleep(3)
                Chooser.queryChooser(2)

            

        elif _ == 3:
            Tools.screen_clear()
            print('*' * 20)
            print('What do you want to view?')
            print('*' * 20)
            print()
            print('* View a list of all books:\n* Press 1')
            print()
            print('* View a count of all books:\n* Press 2')
            print()
            try:
                user_input = int(input())
                if user_input < 3:
                    DBcontrol.viewBookControl(user_input)
                else:
                    raise ValueError
            except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter a number 1-2.")
                print('*' * 20)
                sleep(3)
                Chooser.queryChooser(3)

            

        elif _ == 4:
            Tools.screen_clear()
            print('*' * 20)
            print("What is your query?\nPlease note that [Brackets] must be used around column names.\nAlso note that 'Parentheses' are required for word values.")
            print('!! This will be inserted into an SQL WHERE clause. !!')
            print('*' * 20)
            print()
            user_input = input()

            # I need to sit down and figure out how I can lock down potential errors is.

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

            Tools.screen_clear()
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
            Tools.screen_clear()
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
            Tools.screen_clear()
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

            Tools.screen_clear()
            print('*' * 20)
            print('Is this the book you wish to mark?')
            print('*' * 20)
            # Print the new row
            filt = (df['ISBN'] == isbn)
            new_df = df.loc[filt]
            print(new_df[['Title', 'Author', 'Read_Yet']])
            print()
            try:
                user_input = str(input())
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
                    try:
                        user_input = str(input())
                        if user_input in Chooser.sayYay:
                            MainMenu.markBook()
                        elif user_input in Chooser.sayNay:
                            MainMenu.startMenu()
                        else:
                            raise ValueError
                    except ValueError:
                        Tools.screen_clear()
                        print('*' * 20)
                        print("Please enter yes or no.")
                        print('*' * 20)
                        sleep(3)
                        MainMenu.startMenu()
            except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter yes or no.")
                print('*' * 20)
                sleep(3)
                MainMenu.markBook()

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
        try:
            user_input = str(input())
            if user_input in Chooser.sayYay:
                Tools.running = False
            elif user_input in Chooser.sayNay:
                MainMenu.startMenu()
            else:
                raise ValueError
        except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter yes or no.")
                print('*' * 20)
                sleep(3)
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
        try:
            user_input = str(input())
            if user_input in Chooser.sayYay:
                Tools.running = False
            elif user_input in Chooser.sayNay:
                MainMenu.startMenu()
            else:
                raise ValueError
        except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter yes or no.")
                print('*' * 20)
                sleep(3)
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
        try:
            user_input = str(input())
            if user_input in Chooser.sayYay:
                Tools.running = False
            elif user_input in Chooser.sayNay:
                MainMenu.startMenu()
            else:
                raise ValueError
        except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter yes or no.")
                print('*' * 20)
                sleep(3)
                MainMenu.startMenu()

    def addBookControl():
        """
            This function asks the user for information about the book they want to add.
        """
        Tools.screen_clear()
        print('*' * 20)
        print("I will need to ask ten questions.")
        print("This may take a while, would you like to continue?")
        print("Say yes or no.")
        print('*' * 20)
        print()
        try:
            user_input = str(input())
            if user_input in Chooser.sayYay:
                Tools.screen_clear()
                print('*' * 20)
                print('What is the ISBN?')
                print('*' * 20)
                print()
                try:
                    isbn = int(input())
                except ValueError:
                    Tools.screen_clear()
                    print('*' * 20)
                    print("ISBN must consist of integers.")
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()
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
                if len(author) > 50:
                    print('*' * 20)
                    print('Try again...\nAuthor cannot be more than 50 characters long.')
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()
                print()

                print('*' * 20)
                print('What is the genre?')
                print('*' * 20)
                print()
                genre = input()
                if len(genre) > 50:
                    print('*' * 20)
                    print('Try again...\nGenre cannot be more than 50 characters long.')
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()
                print()
                
                Tools.screen_clear()

                print('*' * 20)
                print('What language is the book in?')
                print('*' * 20)
                print()
                lang = input()
                if len(lang) > 50:
                    print('*' * 20)
                    print('Try again...\nLanguage cannot be more than 50 characters long.')
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()
                elif int(lang) or float(lang):
                    print('*' * 20)
                    print('Try again...\nLanguage cannot contain numbers.')
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()
                print()

                print('*' * 20)
                print('How many pages are in the book?')
                print('*' * 20)
                print()
                try:
                    pages = int(input())
                except ValueError:
                    print('*' * 20)
                    print('Try again...\nEnter the NUMBER of pages.')
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()
                print()

                print('*' * 20)
                print('Who is the Publisher?')
                print('*' * 20)
                print()
                pub = input()
                if len(pub) > 50:
                    print('*' * 20)
                    print('Try again...\nPublisher cannot be more than 50 characters long.')
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()
                print()

                print('*' * 20)
                print('What year was it published?')
                print('*' * 20)
                print()
                try:
                    pub_year = int(input())
                except ValueError:
                    print('*' * 20)
                    print('Try again...\nYear of publication should be integers.')
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()
                print()

                print('*' * 20)
                print('Is it part of a collection?')
                print('*' * 20)
                print()
                user_input = input()
                try:
                    if user_input in Chooser.sayYay:
                        print()
                        print('*' * 20)
                        print('Which collection?')
                        print('*' * 20)
                        print()
                        collection_name = input()
                        if len(collection_name) > 50:
                            print('*' * 20)
                            print('Try again...\nThe Collection Name cannot be more than 50 characters long.')
                            print('*' * 20)
                            sleep(5)
                            DBcontrol.addBookControl()
                    elif user_input in Chooser.sayNay:
                        collection_name = ''
                except ValueError:
                    print('*' * 20)
                    print('Try again...\nPlease say Yes or No.')
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()

                print()
                print('*' * 20)
                print('Have you read this book yet?')
                print('*' * 20)
                print()
                user_input = input()
                try:
                    if user_input in Chooser.sayYay:
                        read_yet = 1
                    elif user_input in Chooser.sayNay:
                        read_yet = 0
                except Exception:
                    print('*' * 20)
                    print('Try again...\nPlease say Yes or No.')
                    print('*' * 20)
                    sleep(5)
                    DBcontrol.addBookControl()

                sleep(2)
                Tools.screen_clear()
                print()
                print('*' * 20)
                print('Here is what you have registered.\nIs this correct? ')
                print('*' * 20)
                print()
                
                print(f"ISBN: {isbn}\nTitle: {title}\nAuthor: {author}\nGenre: {genre}\nLanguage: {lang}\nPages: {pages}\nRead: {read_yet}\nPublisher: {pub}\nCollection: {collection_name}\nYear Published: {pub_year}")
                print()
                print('*' * 20)
                user_input = input("Is this information correct?\nPlease say yes or no.\n")
                try:
                    user_input = str(user_input)
                    if user_input in Chooser.sayYay:
                        # Send it out!
                        DBcontrol.addToBookTable(isbn, title, author, genre, lang, pages, read_yet, pub, collection_name, pub_year)
                    # Send them back if not correct.
                    elif user_input in Chooser.sayNay:
                        DBcontrol.addBookControl()
                    else:
                        raise ValueError
                except ValueError:
                    Tools.screen_clear()
                    print('*' * 20)
                    print("Please enter yes or no.")
                    print('*' * 20)
                    sleep(3)
                    DBcontrol.addBookControl()

            elif user_input in Chooser.sayNay:
                MainMenu.startMenu()

        except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter yes or no.")
                print('*' * 20)
                sleep(3)
                MainMenu.startMenu()

        # Allow the user to continue.
        print('*' * 20)
        print('Would you like to continue adding books?')
        print('*' * 20)
        print()
        try:
            user_input = str(input())
            if user_input in Chooser.sayYay:
                DBcontrol.addBookControl()
            elif user_input in Chooser.sayNay:
                MainMenu.startMenu()
            else:
                raise ValueError
        except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter yes or no.")
                print('*' * 20)
                sleep(3)
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
    
        Tools.screen_clear()
        print('*' * 20)
        print("So, you want to remove a book?")
        print("Say yes or no.")
        print('*' * 20)
        print()
        try:
            user_input = str(input())
            if user_input in Chooser.sayNay:
                MainMenu.queryMenu()
            elif user_input in Chooser.sayYay:
                Tools.screen_clear()
                print('*' * 40)
                print('What is the isbn of the book you would like to remove?')
                print('*' * 40)
                print()
                try:
                    isbn = int(input())
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
                        try:
                            user_input = str(input())
                            if user_input in Chooser.sayYay:
                                # Query must be redefined before runtime.
                                # Mutliple queries might need to be run.
                                delete_query = f"DELETE FROM [PersonalLibrary].[dbo].[BookShelf] WHERE [ISBN] = {isbn}"
                                cursor.execute(delete_query)
                                cursor.commit()
                                Tools.screen_clear()
                                print('*' * 20)
                                print("Book removed from list.")
                                print('*' * 20)
                            elif user_input in Chooser.sayNay:
                                DBcontrol.deleteBook()
                            else:
                                raise ValueError
                        except ValueError:
                            Tools.screen_clear()
                            print('*' * 20)
                            print("Please enter yes or no.")
                            print('*' * 20)
                            sleep(3)
                            MainMenu.startMenu()

                except ValueError:
                    Tools.screen_clear()
                    print('*' * 20)
                    print("ISBN must consist of integers only.")
                    print('*' * 20)
                    sleep(3)
                    DBcontrol.deleteBook()
                

        except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter yes or no.")
                print('*' * 20)
                sleep(3)
                MainMenu.startMenu()


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
        try:
            user_input = str(input())
            if user_input in Chooser.sayYay:
                Chooser.queryChooser(4)
            elif user_input in Chooser.sayNay:
                MainMenu.startMenu()
            else:
                raise ValueError
        except ValueError:
                Tools.screen_clear()
                print('*' * 20)
                print("Please enter yes or no.")
                print('*' * 20)
                sleep(3)
                MainMenu.startMenu()
