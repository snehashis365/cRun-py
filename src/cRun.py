#!/usr/bin/python3
import sys
import os
import getopt

# Some variables declared are for future use
VERSION = "0.0.2"  # This is redundant will be removed soon
OS = os.name
CACHE_FOLDER = ".crun-cache/"
COMPILE = False
EXECUTE = True
BUILD_MENU = False
SINGLE_FILE = False
CLEANUP = False
SHOW_TIME = False

# Color codes
LGREEN = "\033[1;32m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
LBLUE = "\033[0;36m"
NORMAL = "\033[0m"


def clear():  # Executes command depending on OS
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def banner():  # Builds banner
    print(LBLUE, end="")
    print(r"""
                 ____                __  __
          _____ / __ \ __  __ ____   \ \ \ \
         / ___// /_/ // / / // __ \   \ \ \ \
        / /__ / _, _// /_/ // / / /   / / / /
        \___//_/ |_| \__,_//_/ /_/   /_/ /_/

    """)
    print(f"{LGREEN}                          - by snehashis365{NORMAL}")
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


def main():
    global EXECUTE, COMPILE, BUILD_MENU, SHOW_TIME, CLEANUP, SINGLE_FILE
    # Handle options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hcrmtvdsiu",
                                   ["help", "compile", "run", "menu", "time", "version", "cleanup", "super", "install",
                                    "update"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, a in opts:
        if opt in ["-h", "--help"]:
            print("Help message here")
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
            SHOW_TIME = True
            print(SHOW_TIME)
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
    banner()
    count = 0
    err_count = 0
    if len(args) == 1:
        SINGLE_FILE = True
        build_submenu(args[0])
    elif BUILD_MENU and len(args) > 1:
        build_menu(args)
    elif len(args) == 0:
        directory_content, c_files = os.listdir(), []
        for content in directory_content:
            if content[-2:] == ".c":
                c_files.append(content)
        directory_content.clear()
        if len(c_files) == 1:
            build_submenu(c_files[0])
        elif len(c_files) > 1:
            build_menu(c_files)
        else:
            print("No .c files in current directory")
    else:
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
