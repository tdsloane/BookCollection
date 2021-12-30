from screen_tools import Tools
from monitor_modes import MainMenu

"""
    This program is for the recording and tracking of the books in my collection.
    A menu with multiple options guides the user through looking at the collection,
    modifying the collection, adding to, or reducing the colleciton, etc.
"""


class LibStart:

    def mainLoop(running):
        while Tools.running:

            # Main Menu: Choose from options to branch from.
            MainMenu.startMenu()
            
            # End Program
            Tools.running = False

# Launch
LibStart.mainLoop(Tools.running)