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
from db_handler import DB_Handler

import getpass
from getpass import getpass


CMD_INPUT     = 'pytodo> '
CMD_PREFIX    = '/'

CMD_ADD    = '/a'
CMD_DONE   = '/d'
CMD_HELP   = '/h'
CMD_LIST   = '/l'
CMD_QUIT   = '/q'
CMD_REMOVE = '/r'
CMD_RESET  = '/reset'

COMMANDS = [
    CMD_ADD ,
    CMD_DONE,
    CMD_HELP,
    CMD_LIST,
    CMD_QUIT,
    CMD_REMOVE,
    CMD_RESET
]

ENDC    = '\033[0m'
FAIL    = '\033[91m'
HEADER  = '\033[95m'
OKBLUE  = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'

 
class Cli:
    """
    """
    def __init__(self):
        """
        """
        self.__db = DB_Handler()
        self.__start()

    def __cli_print(self, text, color):
        """
        """
        print(color + text + ENDC)

    def __log_usr(self, check=0):
        """
        """
        name = input('Name> ')

        psswd = 'foo'

        if not check:
            verif = 'bar'
            while psswd != verif:
                psswd = getpass('Password> ')
                verif = getpass('Repeat password> ')

                if psswd != verif:
                    self.__cli_print('\nPasswords don\'t match', FAIL)
        else:
            psswd = getpass('Password> ')

        return (name, psswd)

    def __poll(self):
        """
        """
        self.__cli_print('\n--- SUCCESSFULLY CONNECTED ---\n', OKGREEN)
        aborted = 1

        while True:
            inp = input(CMD_INPUT)
            if inp.startswith(CMD_PREFIX):
                cmd = inp.split()[0]
                if cmd in COMMANDS:
                    if inp == CMD_LIST :
                        if cmd != inp :
                            print('Listing does not required an argument')
                        self.__task_list()
                    elif cmd == CMD_ADD:
                        self.__task_add(inp)
                    elif cmd == CMD_DONE:
                        self.__task_done(inp)
                    elif cmd == CMD_REMOVE:
                        self.__task_remove(inp)
                    elif cmd == CMD_RESET:
                        if cmd != inp :
                            print('Reset does not required an argument')
                        aborted = self.__task_reset()
                        if not aborted:
                            break
                    elif cmd == CMD_HELP:
                        if cmd != inp :
                            print('Help does not required an argument')
                        self.__print_help()
                    elif cmd == CMD_QUIT:
                        if cmd != inp :
                            print('Quit does not required an argument')
                        self.__quit_app()
                else:
                    self.__cli_print (
                            'Unhandled command type ' + CMD_HELP +' for help',
                             WARNING
                        )
            else:
                self.__cli_print (
                        'Commands must start with \'' + CMD_PREFIX + '\'',
                         WARNING
                    )

        self.__start() # restart on CMD_RESET

    def __print_help(self):
        """
        """
        helper = '\nAvailable commands:\n'
        helper+= '\t'+CMD_ADD   +' [desc] .. add a new task\n'
        helper+= '\t'+CMD_DONE  +' id ...... pass the task to \'done\'\n'
        helper+= '\t'+CMD_LIST  +' ......... list all tasks\n'
        helper+= '\t'+CMD_REMOVE+' id ...... remove the task\n'
        helper+= '\t'+CMD_RESET +' ..... delete everything\n'
        helper+= '\t'+CMD_HELP  +' ......... displays help\n'
        helper+= '\t'+CMD_QUIT  +' ......... quit\n'
        print(helper)


    def __task_add(self, cmd):
        """
        """
        description = ''

        if len(cmd) > 3 :
            description = cmd[3:]
        else:
            print('Please specify a description: ')
            description = input('> ')

        self.__db.task_register(description)
        self.__cli_print('Task added.\n', OKGREEN)

    def __task_done(self, cmd):
        """
        """
        if len(cmd.split()) < 2:
            print('Missing parameter, see ' + CMD_HELP + '.\n')
        else:
            task_id = cmd.split()[1]
            self.__db.task_done(task_id)
            self.__cli_print('Task status changed.\n', OKGREEN)

    def __task_list(self):
        """
        """
        tasks = self.__db.task_list()
        if len(tasks) == 0 :
            print('No task planified yet, add one with ' + CMD_ADD)
        else:
            print('Registered task(s):')
            for task in tasks:
                task_sum = '\t'
                if task[2] == 0:
                    task_sum += '[ ] '
                else:
                    task_sum += '[x] '
                task_sum += '(' + str(task[0]) + ') '
                task_sum += task[1]
                print (task_sum)
            print('')

    def __task_remove(self, cmd):
        """
        """
        if len(cmd.split()) < 2:
            print('Missing parameter, see ' + CMD_HELP + '.\n')
        else:
            task_id = cmd.split()[1]
            self.__db.task_delete(task_id)
            self.__cli_print('Task removed.\n', OKGREEN)

    def __task_reset(self):
        """
        """
        self.__cli_print('Are you sure ?', WARNING)
        
        inp = -1
        while inp not in ['y', 'n']:
            inp = input('(y/n) > ')
        if inp == 'n':
            self.__cli_print('Aborted.\n', FAIL)
            return 1

        print("Please verify your identity: ")
        name, psswd = self.__log_usr(check=1)

        if not self.__db.connect(name, psswd):
            self.__cli_print('Verification failed.\n', FAIL)
            return 1

        print('\nDeleting data...')
        self.__db.delete_all()
        print('Success.\n')

        return 0


    def __quit_app(self):
        """
        """
        self.__db.disconnect()
        exit()

    def __start(self):
        """
        """
        if not self.__db.user_exists(): # user doest not exists
            msg = 'It seems that no users are registered \n'
            msg+= 'Do you want to sign in ?'
            print(msg)

            inp = -1
            while inp not in ['y', 'n']:
                inp = input('(y/n) > ')

            if inp == 'y':
                print('\nPlease enter your informations: ')

                name, psswd = self.__log_usr()

                self.__db.user_register(name, psswd)

            else: 
                self.__quit_app()

        else: # user exists
            connected = 0

            while not connected:
                name  = input('User name: ')
                psswd = getpass('Password: ')
                connected = self.__db.connect(name, psswd)
                if not connected:
                    self.__cli_print('\nLogin failed.', FAIL)

        self.__poll() # start the app
