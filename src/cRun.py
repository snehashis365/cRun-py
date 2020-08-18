#!/usr/bin/python3
import sys
import os
import getopt
import curses
import time

# Some variables declared are for future use
VERSION = "0.0.3"  # This is redundant will be removed soon
OS = os.name
CACHE_FOLDER = ".crun-cache/"
COMPILE = False
EXECUTE = True
BUILD_MENU = False
SINGLE_FILE = False
CLEANUP = False
SHOW_TIME = False
TEST_MODE = False
TEST_RETURN = 0
MAX_FILE_NAME = 0
# Color codes
LGREEN = "\033[1;32m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
LBLUE = "\033[0;36m"
NORMAL = "\033[0m"
# BANNER_ART = "                 ____                __  __\n          _____ / __ \\ __  __ ____   \\ \\ \\ \\\n         / ___// /_/ // / / // __ \\   \\ \\ \\ \\\n        / /__ / _, _// /_/ // / / /   / / / /\n        \\___//_/ |_| \\__,_//_/ /_/   /_/ /_/\n\n                          - by snehashis365"
BANNER_ART = r"""
                 ____                __  __
          _____ / __ \ __  __ ____   \ \ \ \
         / ___// /_/ // / / // __ \   \ \ \ \
        / /__ / _, _// /_/ // / / /   / / / /
        \___//_/ |_| \__,_//_/ /_/   /_/ /_/
                                -by snehashis365
"""


def clear():  # Executes command depending on OS
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_help():
    print(f"cRun Version:{VERSION}(test-release) by snehashis365")
    print("""This script will compile the files specified and generate object files with same name as the C file and
    Execute them in the order entered.\n""")
    print(f"Usage: {sys.argv[0]} [-h help] [-c compile] [-r execute] [-m menu ] [-t test] [-d cleanup] *filename.c")
    print("The above command will consider only the files specified\n")
    print(f"Usage: {sys.argv[0]} [-c compile] [-t test] [-d cleanup]")
    print("The above command will consider all .c files in the working directory")


def banner():  # Builds banner
    print(LBLUE, end="")
    print(BANNER_ART, end="")
    print(f"Version : {LGREEN}{VERSION}(test-release){NORMAL}")
    print("Re-Compile : ", end="")
    if COMPILE:
        print(f"{BLUE}On{NORMAL}")
    else:
        print(f"{LGREEN}Off{NORMAL}")
    print("Auto Cleanup : ", end="")
    if CLEANUP:
        print(f"{RED}On{NORMAL}")
    else:
        print(f"{LGREEN}Off{NORMAL}")
    print("\n")


def compile_c(file_name):
    print(BLUE, end="")  # Setting color prior
    if os.path.exists(CACHE_FOLDER + file_name[:-2] + ".out"):
        print("Re-", end="")
    print(f"Compiling{NORMAL}->{file_name}\n")
    return os.system("cc " + file_name + " -o " + CACHE_FOLDER + file_name[:-2] + ".out -lm")


def run(file_name):
    return_code = 0
    if not os.path.exists(CACHE_FOLDER + file_name[:-2] + ".out") or COMPILE:
        return_code = compile_c(file_name)
    if return_code == 0:
        print(f"{LGREEN}Executing{NORMAL}->{file_name}\n")
        os.system("./" + CACHE_FOLDER + file_name[:-2] + ".out")
        print(f"\n{LGREEN}Done{NORMAL}\n")
    else:
        print("Compile error!")
    if CLEANUP:
        os.system(f"rm {CACHE_FOLDER}{file_name[:-2]}.out")


def build_submenu(file_name):
    while True:
        clear()
        banner()
        print(f"{LBLUE}Selected->{LGREEN}{file_name}{NORMAL}\n")
        print("1. Run\n2. Compile\n")
        if not SINGLE_FILE:
            print("9. Return to main menu")
        print("0. Exit")
        try:
            choice = int(input(">> "))
            if choice == 1:
                run(file_name)
            elif choice == 2:
                compile_c(file_name)
            elif choice == 9 and not SINGLE_FILE:
                break
            elif choice == 0:
                print("\nExiting...\n")
                sys.exit()
            else:
                print("Wrong choice!!!")
        except Exception as e:
            print(e)
            print(f"{RED}Wrong input!!{NORMAL}\nPlease Enter desired option {LGREEN}number{NORMAL}\n")
        input("Screen will be cleared\nPress enter to continue...")


def build_menu(file_list):
    while True:
        clear()
        banner()
        index = 1
        # Generate menu from file list
        for file in file_list:
            print(f"{index}. ", end="")
            if os.path.exists(CACHE_FOLDER + file[:-2] + ".out"):
                print(LGREEN, end="")
            else:
                print(RED, end="")
            print(f"{file}{NORMAL}")
            index += 1
        print("\n0. Exit\n")
        try:
            choice = int(input(">> "))
            if choice == 0:
                print("\nExiting...\n")
                sys.exit()
            elif 0 < choice <= index:
                build_submenu(file_list[choice - 1])
                print("Returned...")
            else:
                print("Invalid input try again")
                input("Press enter to continue...")
        except Exception as e:
            print(e)
            print(f"{RED}Wrong input!!{NORMAL}\nPlease Enter desired option {LGREEN}number{NORMAL}\n")


def test_banner(stdscr):  # This will replace the banner function once finished
    stdscr.clear()
    try:
        y = 0
        for line in BANNER_ART.splitlines():
            stdscr.addstr(y, 0, line, curses.color_pair(6))
            y += 1
        stdscr.addstr(y, 10, f"{VERSION}(test-release)", curses.color_pair(3))
        if COMPILE:
            stdscr.addstr(y + 1, 13, "On", curses.color_pair(5))
        else:
            stdscr.addstr(y + 1, 13, "Off")
        if CLEANUP:
            stdscr.addstr(y + 2, 15, "On", curses.A_BLINK)
        else:
            stdscr.addstr(y + 2, 15, "Off")
        stdscr.addstr(y, 0, "Version : ", curses.color_pair(5))
        stdscr.addstr(y + 1, 0, "Re-Compile : ")
        stdscr.addstr(y + 2, 0, "Auto Cleanup : ")
        stdscr.refresh()
    except curses.error:
        pass


def test(stdscr, file_list):  # This will replace the build menu function once finished
    global TEST_RETURN, MAX_FILE_NAME
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    sel_index = 0

    while True:
        h, w = stdscr.getmaxyx()
        test_banner(stdscr)
        if sel_index < len(file_list):
            stdscr.addstr(h-1, 0, f"Press Enter to select -> {file_list[sel_index]}")
        else:
            stdscr.addstr(h - 1, 0, f"Press Enter to confirm Exit")
        index = 0
        y, x = 12, 0
        for file in file_list:
            pair = 1
            if os.path.exists(CACHE_FOLDER + file[:-2] + ".out"):
                pair = 3
            stdscr.attron(curses.color_pair(pair))
            try:
                if y == h-3:
                    y = 12
                    x += MAX_FILE_NAME+3  # Reset X and Y
                if index == sel_index:
                    stdscr.addstr(y, x, f"> {file[:-2]}", curses.A_STANDOUT)
                else:
                    stdscr.addstr(y, x, f"> {file[:-2]}")
            except curses.error:
                pass
            index += 1
            y += 1
            stdscr.attroff(curses.color_pair(pair))
        try:
            if sel_index == len(file_list):
                stdscr.addstr(h-2, (w//2) - 2, "Exit", curses.A_REVERSE)
            else:
                stdscr.addstr(h-2, (w//2) - 2, "Exit")
        except curses.error:
            pass
        # stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            break
        elif key == curses.KEY_UP:
            if sel_index > 0:
                sel_index -= 1
            else:
                sel_index = len(file_list)
        elif key == curses.KEY_DOWN:
            if sel_index < len(file_list):
                sel_index += 1
            else:
                sel_index = 0
        elif key == curses.KEY_RIGHT and sel_index+(h-12)-3 <= len(file_list):
            sel_index += (h - 12) - 3
        elif key == curses.KEY_LEFT and sel_index-((h-12)-3) >= 0:
            sel_index -= (h - 12) - 3
        elif key == 27:
            try:
                stdscr.addstr(h - 2, (w // 2) - 7, "...Exiting...", curses.A_REVERSE)
                stdscr.refresh()
            except curses.error:
                pass
            time.sleep(1)
            sys.exit()
    TEST_RETURN = sel_index


def main():
    global EXECUTE, COMPILE, BUILD_MENU, CLEANUP, SINGLE_FILE, TEST_MODE, TEST_RETURN, MAX_FILE_NAME
    # Handle options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hcrmtvdsiu",
                                   ["help", "compile", "run", "menu", "test", "version", "cleanup", "super", "install",
                                    "update"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, a in opts:
        if opt in ["-h", "--help"]:
            get_help()
            sys.exit()
        elif opt in ["-c", "--compile"]:
            COMPILE = True
            EXECUTE = False
        elif opt in ["-r", "--run"]:
            EXECUTE = True
        elif opt in ["-m", "--menu"]:
            BUILD_MENU = True
            print(BUILD_MENU)
        elif opt in ["-t", "--time"]:
            TEST_MODE = True
        elif opt in ["-v", "--version"]:
            print(f"cRun {VERSION}(test-release) by snehashis365")
            sys.exit()
        elif opt in ["-d", "--cleanup"]:
            CLEANUP = True
        elif opt in ["-s", "--super"]:
            print("Attempting sudo")
            os.system(f"sudo {sys.argv[0]}")
            sys.exit()
        elif opt in ["-i", "--install"]:
            print("Call Install function(Coming Soon)")
        elif opt in ["-u", "--update"]:
            print("Call update function(Coming Soon)")
    # End of options handling

    # Checking cache folder
    if not os.path.exists(CACHE_FOLDER[:-1]):
        os.mkdir(CACHE_FOLDER[:-1])
    if BUILD_MENU and len(args) == 1:
        SINGLE_FILE = True
        build_submenu(args[0])
    elif BUILD_MENU and len(args) > 1:
        build_menu(args)
    elif len(args) == 0:
        directory_content, c_files = os.listdir(), []
        for content in directory_content:
            if content[-2:] == ".c":
                c_files.append(content)
                if len(content) > MAX_FILE_NAME:
                    MAX_FILE_NAME = len(content)
        directory_content.clear()
        if len(c_files) == 1:
            build_submenu(c_files[0])
        elif len(c_files) > 1:
            if TEST_MODE:
                while True:
                    curses.wrapper(test, c_files)
                    if TEST_RETURN < len(c_files):
                        build_submenu(c_files[TEST_RETURN])
                    else:
                        print("Exiting...")
                        break
            else:
                build_menu(c_files)
        else:
            print("No .c files in current directory")
    else:
        banner()
        count = 0
        err_count = 0
        for arg in args:
            if EXECUTE:
                run(arg)
            else:
                return_code = compile_c(arg)
                if return_code > 0:
                    err_count += 1
            count += 1
        print(f"Total: {count}\nFailed: {err_count}\nSuccess: {count - err_count}")


if __name__ == "__main__":
    main()
