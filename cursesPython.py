import curses
from curses import wrapper

def main(stdscr):
    stdscr.clear()
    while True:
        # Store the key value in the variable `c`
        c = stdscr.getch()
        # Clear the terminal
        stdscr.clear()
        if c == ord('a'):
            stdscr.addstr("You pressed the 'a' key.", curses.A_REVERSE)
        elif c == curses.KEY_UP:
            stdscr.addstr("You pressed the up arrow.")
        elif c == ord('\n'):
            wrapper(menu)
        else:
            stdscr.addstr("This program doesn't know that key.....")
    stdscr.refresh()
    stdscr.getkey()



def menu(stdscr):
    dims = stdscr.getmaxyx()
    stdscr.nodelay(0)
    stdscr.clear()
    selection = -1
    option = 0
    while selection < 0:
        menuOptions = [0]*4
        menuOptions[option] = curses.A_REVERSE
        stdscr.addstr(int(dims[0]/2)-2, int(dims[1]/2-4), 'Blink LED', menuOptions[0])
        stdscr.addstr(int(dims[0]/2)-1, int(dims[1]/2-3), 'Compare', menuOptions[1])
        stdscr.addstr(int(dims[0]/2), int(dims[1]/2)-6, 'Instructions', menuOptions[2])
        stdscr.addstr(int(dims[0]/2)+1, int(dims[1]/2)-2, 'Exit', menuOptions[3])
        action = stdscr.getch()
        if action == curses.KEY_UP:
            option = (option - 1) % 4
        elif action == curses.KEY_DOWN:
            option = (option + 1) % 4
        elif action == ord('\n'):
            selection = option
        stdscr.refresh()
        if selection == 0:
            stdscr.clear()
            stdscr.addstr('Blink LED selected')
            stdscr.addstr(1,0,'Return to Menu on Using Enter')
            stdscr.addstr(2,0,'Test Using t')
            choice = stdscr.getch()
            if choice == ord("t"):
                wrapper(main)
                stdscr.clear()
                stdscr.refresh()
                selection = -1
            elif choice == ord('\n'):
                stdscr.clear()
                stdscr.refresh()
                selection = -1
            else:
                selection = -1
        if selection == 2:
            stdscr.clear()
            stdscr.addstr(1,int(dims[1]/2)-6,'Instructions')
            message = """Designed to turn on Drive LEDs on Failure for SSG systems.\n
                         Blink LED will turn on or off LEDs on connected backplanes.\n
                         Compare will bring up a table of all drive curretly found
                         versus all drives that were found on startup. \n
                         Instructions will bring up this menu. \n
                         Exit will exit the program. \n
                         """
            stdscr.addstr(5,int(dims[1]/2)- 30,message)
            stdscr.getch()
            stdscr.clear()
            selection = -1

wrapper(menu)
