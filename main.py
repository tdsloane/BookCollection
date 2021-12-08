import os
from monitor_modes import MainMenu

"""
    This program is for the recording and tracking of the books in my collection.
    A menu with multiple options guides the user through looking at the collection,
    modifying the collection, adding to, or reducing the colleciton, etc.
"""

class LibStart:
    running = True

    def mainLoop():
        while running:

            # Main Menu: Choose from options to branch from.
            MainMenu.startMenu()
            
            # End Program
            running = False

# Launch
LibStart.mainLoop()