"""
    These are connection tools, scren clear tools, etc.
"""
import os


class Tools:

    running = True

    def screen_clear():
        """
            This function clears the terminal screen.
        """
        if os.name == 'nt':
            _ = os.system('cls')


    def goodbye():
        Tools.screen_clear()
        print('*' * 20)
        print("Goodbye! Happy Reading!")
        print('*' * 20)
        Tools.running = False