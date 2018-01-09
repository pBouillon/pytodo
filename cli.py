# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2017 Pierre Bouillon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# auhtor: Pierre Bouillon [https://github.com/pBouillon]

import db_handler
from db_handler import ALL_TASKS
from db_handler import DB_Handler

import getpass
from getpass import getpass


""" commands for add """
CMD_ADD      = 'a'
CMD_ADD_L    = 'add'
""" commands for done """
CMD_DONE     = 'd'
CMD_DONE_L   = 'done'
""" commands for help """
CMD_HELP     = 'h'
CMD_HELP_L   = 'help'
""" commands for list """
CMD_LIST     = 'l'
CMD_LIST_L   = 'list'
""" commands for modification """
CMD_MODIF    = 'm'
CMD_MODIF_L  = 'modif'
""" commands for quit """
CMD_QUIT     = 'q'
CMD_QUIT_L   = 'quit'
""" commands for remove """
CMD_REMOVE   = 'rm'
CMD_REMOVE_L = 'remove'
""" commands for reset """
CMD_RESET    = 'rs'
CMD_RESET_L  = 'reset'


""" list of all commands """
COMMANDS = [
    CMD_ADD,
    CMD_ADD_L,
    CMD_DONE,
    CMD_DONE_L,
    CMD_HELP,
    CMD_HELP_L,
    CMD_LIST,
    CMD_LIST_L,
    CMD_MODIF,
    CMD_MODIF_L,
    CMD_QUIT,
    CMD_QUIT_L,
    CMD_REMOVE,
    CMD_REMOVE_L,
    CMD_RESET,
    CMD_RESET_L 
]


""" color: reset """
COLOR_END  = '\033[0m'
""" color: red """
COLOR_FAIL = '\033[91m'
""" color: green """
COLOR_OKGREEN = '\033[92m'
""" color: orange """
COLOR_WARNING = '\033[93m'


""" pytodo CLI display """
CMD_INPUT  = 'pytodo> '
TASK_DONE  = '[x]'
TASK_TO_DO = '[ ]'
""" warnings"""
W_NO_ARG_NEEDED = 'This command does not require any other argument'
W_NO_ARG_PROV   = 'Missing parameter, see ' + CMD_HELP + '.'
W_BAD_CMD       = 'Unhandled command type \'' + CMD_HELP_L +'\' for help'

 
class Cli:
    """Reference Cli

    Manage the user commands and display

    Attributes:
        __db : pytodo database handler (see DB_Handler)
    """
    def __init__(self):
        """
        """
        self.__db = DB_Handler()

    def __cli_print(self, text, color):
        """Format text with color
        """
        print(color + text + COLOR_END)

    def __log_usr(self, check=0):
        """Ensure that the user has the good credentials

        Parameters:
            check : [optionnal] 1 if this is a verification
                    (if 0 the user will have to type his password twice)

        Returns:
            (name, password) : if the user is connected, returns its credentials

        """
        name = input('Name> ')
        psswd = 'foo'

        if not check:
            verif = 'bar'
            while psswd != verif:
                psswd = getpass('Password> ')
                verif = getpass('Repeat password> ')

                if psswd != verif:
                    self.__cli_print('\nPasswords don\'t match', COLOR_FAIL)
        else:
            psswd = getpass('Password> ')

        return (name, psswd)

    def __poll(self):
        """CLI display

        Handle every pytodo commands and execute them
        """
        self.__cli_print('\n--- SUCCESSFULLY CONNECTED ---\n', COLOR_OKGREEN)
        aborted = 1

        while True:
            inp = input(CMD_INPUT)
            cmd = inp.split()[0]

            if cmd in COMMANDS:
                if inp == CMD_LIST or cmd == CMD_LIST_L:
                    if cmd != inp :
                        print(W_NO_ARG_NEEDED)
                    self.__task_list()
                elif cmd == CMD_ADD or cmd == CMD_ADD_L :
                    self.__task_add(inp)
                elif cmd == CMD_DONE or cmd == CMD_DONE_L :
                    self.__task_done(inp)
                elif cmd == CMD_REMOVE or cmd == CMD_REMOVE :
                    self.__task_remove(inp)
                elif cmd == CMD_MODIF or cmd == CMD_MODIF_L :
                    self.__task_modif(inp)
                elif cmd == CMD_RESET or cmd == CMD_RESET_L :
                    if cmd != inp :
                        print(W_NO_ARG_NEEDED)
                    aborted = self.__task_reset()
                    if not aborted:
                        break
                elif cmd == CMD_HELP or cmd == CMD_HELP_L :
                    if cmd != inp :
                        print(W_NO_ARG_NEEDED)
                    self.__print_help()
                elif cmd == CMD_QUIT or cmd == CMD_QUIT_L:
                    if cmd != inp :
                        print(W_NO_ARG_NEEDED)
                    self.__quit_app()
            else:
                self.__cli_print (W_BAD_CMD, COLOR_WARNING)

        self.start() # restart on CMD_RESET

    def __print_help(self):
        """Displays help with all commands

        Prints available actions and their commands
        Prints their shortcuts
        """
        helper = '\n'
        helper+= 'Available commands:\n'
        helper+= '\t- add a new task .......... ' + CMD_ADD_L
        helper+= ' [desc]\n'
        helper+= '\t- pass the task to done ... ' + CMD_DONE_L
        helper+= ' [undo] id\n'
        helper+= '\t- list all tasks .......... ' + CMD_LIST_L   + ' \n'
        helper+= '\t- remove task ............. ' + CMD_REMOVE_L
        helper+= ' (all | id)\n'
        helper+= '\t- rename a task ........... ' + CMD_MODIF_L
        helper+= ' id new_name\n'
        helper+= '\t- reset pytodo ............ ' + CMD_RESET_L  + ' \n'
        helper+= '\t- displays help ........... ' + CMD_HELP_L   + ' \n'
        helper+= '\t- quit pytodo cli ......... ' + CMD_QUIT_L   + ' \n'
        helper+= '\n'
        helper += 'Shortcuts:\n'
        helper+= '\t- ' + CMD_ADD_L + '    -> ' + CMD_ADD    + ' \n'
        helper+= '\t- ' + CMD_DONE_L + '   -> ' + CMD_DONE   + ' \n'
        helper+= '\t- ' + CMD_LIST_L + '   -> ' + CMD_LIST   + ' \n'
        helper+= '\t- ' + CMD_REMOVE_L + ' -> ' + CMD_REMOVE + ' \n'
        helper+= '\t- ' + CMD_MODIF_L + '  -> ' + CMD_MODIF  + ' \n'
        helper+= '\t- ' + CMD_RESET_L + '  -> ' + CMD_RESET  + ' \n'
        helper+= '\t- ' + CMD_HELP_L + '   -> ' + CMD_HELP   + ' \n'
        helper+= '\t- ' + CMD_QUIT_L + '   -> ' + CMD_QUIT   + ' \n'
        print(helper)

    def __task_add(self, cmd):
        """Add a task

        If the topic is provided, add it directly
        otherwise, asks for it

        Parameters:
            cmd : user's command line
        """
        description = ''

        if len(cmd) > 3 :
            description = cmd[3:]
        else:
            try:
                print('Please specify a description: ')
                description = input('> ')
            except KeyboardInterrupt:
                self.__cli_print('\nAborted.\n', COLOR_FAIL)
                return

        self.__db.task_register(description)
        self.__cli_print('Task added.\n', COLOR_OKGREEN)

    def __task_done(self, cmd):
        """Change task's status

        Switch a task to done if only the id is provided
        If 'undo' option is set, switch the task to 'to do'

        Parameters:
            cmd : user's command line
        """
        args = len(cmd.split())
        if args == 2:
            task_id = cmd.split()[1]
            self.__db.task_done(task_id)
        elif args == 3:
            if cmd.split()[1] == 'undo':
                task_id = cmd.split()[2]
                self.__db.task_done(task_id, state=0)
            else:
                self.__cli_print('Option: ' + cmd.split()[1] + ' not hanled.', COLOR_FAIL)
                return
        else:
            print(W_NO_ARG_PROV + '\n')
            return
        self.__cli_print('Task status changed.\n', COLOR_OKGREEN)

    def __task_list(self):
        """List all tasks

        Lists tasks as:
            [ ] (id) task     if not done
            [x] (id) task     if done
        """
        tasks = self.__db.task_list()
        if len(tasks) == 0 :
            print('No task planified yet, add one with ' + CMD_ADD + '\n')
        else:
            print('Registered task(s):')
            for task in tasks:
                task_sum = '\t'
                if task[2] == 0:
                    task_sum += TASK_TO_DO
                else:
                    task_sum += TASK_DONE
                task_sum += ' (' + str(task[0]) + ') '
                task_sum += task[1]
                print (task_sum)
            print('')

    def __task_modif(self, cmd):
        """Change the topic of a task

        Parameters:
            cmd : user's command line
        """
        args = len(cmd.split())
        if args < 3:
            print(W_NO_ARG_PROV + '\n')
        else:
            task_id   = cmd.split()[1]
            new_topic = ''
            sep = ''
            for i in range(2, args):
                new_topic += sep + cmd.split()[i]
                sep = ' '
            self.__db.task_rename(task_id, new_topic)
            self.__cli_print('Task renamed.\n', COLOR_OKGREEN)

    def __task_remove(self, cmd):
        """
        """
        args = len(cmd.split())
        if args == 1:
            print(W_NO_ARG_PROV + '\n')
        else:
            task_id = cmd.split()[1]
            if task_id == 'all':
                print('Do you really want to delete all tasks?')
                inp = -1
                while inp not in ['y', 'n']:
                    inp = input('(y/n) > ')
                if inp == 'y':
                    self.__db.task_delete(ALL_TASKS)
                    self.__cli_print('Tasks removed.\n', COLOR_OKGREEN)
            else:
                task_id = cmd.split()[1]
                self.__db.task_delete(task_id)
                self.__cli_print('Task removed.\n', COLOR_OKGREEN)

    def __task_reset(self):
        """Delete all informations

        Delete all existing tasks
        Then delete the user

        Returns:
            0 on success
            1 on abort
        """
        try:
            self.__cli_print('Are you sure ?', COLOR_WARNING)
            
            inp = -1
            while inp not in ['y', 'n']:
                inp = input('(y/n) > ')

            if inp == 'n':
                self.__cli_print('Aborted.\n', COLOR_FAIL)
                return 1

            print("Please verify your identity: ")
            name, psswd = self.__log_usr(check=1)

        except KeyboardInterrupt:
                self.__cli_print('\nAborted.\n', COLOR_FAIL)
                return 1

        if not self.__db.connect(name, psswd):
            self.__cli_print('Verification failed.\n', COLOR_FAIL)
            return 1

        print('\nDeleting data...')
        self.__db.delete_all()
        print('Success.\n')

        return 0

    def __quit_app(self):
        """Exit pytodo

        Close the database and exit
        """
        print() # prevent '^C' and path display on the same line in terminal
        self.__db.disconnect()
        exit()

    def start(self):
        """ Start pytodo

        If no user detected, register one
        If one user detected, asks for authentication
        """
        if not self.__db.user_exists(): # user doest not exists
            msg = 'It seems that no users are registered \n'
            msg+= 'Do you want to sign in ?'
            print(msg)

            inp = -1

            try:
                while inp not in ['y', 'n']:
                    inp = input('(y/n) > ')
            except KeyboardInterrupt:
                self.__quit_app()

            if inp == 'y':
                print('\nPlease enter your informations: ')
                name, psswd = self.__log_usr()
                self.__db.user_register(name, psswd)
            else: 
                self.__quit_app()

        else: # user exists
            connected = 0
            try:
                while not connected:
                    name  = input('User name: ')
                    psswd = getpass('Password: ')
                    connected = self.__db.connect(name, psswd)
                    if not connected:
                        self.__cli_print('\nLogin failed.', COLOR_FAIL)

            except KeyboardInterrupt:
                self.__quit_app()

        self.__poll() # start the app
