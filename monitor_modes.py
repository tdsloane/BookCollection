"""
    The classes and functions herein are for the express purpose
    of creating and displaying menus while also connecting menus to eachother.
"""
from time import sleep
from screen_tools import Tools
from db_functions import DBcontrol

class MainMenu:

    def startMenu():
        """
            This function displays the main menu.
        """
        Tools.screen_clear()
        print()
        print('*' * 20)
        print('Welcome to the\nGiioke Book System!')
        print('*' * 20)
        sleep(5)
        Tools.screen_clear()

        print('*' * 20)
        print('What would you like to do?')
        print('*' * 20)
        print()
        print('* To query the library:\n* Press 1')
        print()
        print('* To add a book:\n* Press 2')
        print()
        print('* To mark a book as read:\n* Press 3')
        print()
        print('* To remove a book from the system:\n* Press 4')
        print()
        user_input = input()
        try:
            user_input = int(user_input)
            print(type(user_input))
            if user_input > 4:
                print("Please enter a number 1-4")
                sleep(5)
                MainMenu.startMenu()
        except ValueError as e:
            print(f"{e} Please enter a number 1-4.")
            sleep(5)
            MainMenu.startMenu()
        print("Int Check")
        Chooser.mainChooser(user_input) 


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
        user_input = input()
        if user_input != int or user_input > 4:
            print("Please enter a number 1-4")
            MainMenu.queryMenu()
        Chooser.queryChooser(user_input)

    def addBook():
        """
            This function uses an insert statement to add a book to the db.
        """
        Tools.screen_clear()
        print('*' * 20)
        print("So, you want to add a book to the list?")
        print("Say yes or no.")
        print('*' * 20)
        print()
        user_input = input()
        if user_input in Chooser.sayNay:
            MainMenu.queryMenu()
        elif user_input in Chooser.sayYay:
            DBcontrol.addBookInfo()


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
        user_input = input()
        if user_input in Chooser.sayNay:
            MainMenu.queryMenu()
        elif user_input in Chooser.sayYay:
            # This is where we will update a book.
            pass


    def deleteBook():
        """
            This function uses an delete statement to remove a book from the db.
        """
        Tools.screen_clear()
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
        Tools.screen_clear()
        
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
                DBcontrol.viewBookControl()
            
        # Content Checks for user input
            elif user_input not in (Chooser.sayYay + Chooser.sayNay):
                print("Please answer yes or no.")
                QueryMenu.viewBooks()
        elif user_input not in (Chooser.sayYay + Chooser.sayNay):
                print("Please answer yes or no.")
                QueryMenu.viewBooks()

    def viewUnreadBooks():
        Tools.screen_clear()
        
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
        Tools.screen_clear()
        
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
    sayYay = ['Y', 'n', 'yes', 'Yes']

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