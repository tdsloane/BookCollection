"""
    These are connection tools, scren clear tools, etc.
"""
import os


class ScreenTools:

    running = True

    def screen_clear():
        """
            This function clears the terminal screen.
        """
        if os.name == 'nt':
            _ = os.system('cls')