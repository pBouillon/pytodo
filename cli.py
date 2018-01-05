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

CMD = 'pytodo> '
COMMANDS = [
    '/h', # help
    '/a', # add
    '/d', # done
    '/r', # remove
    '/q'  # quit
]

class Cli:
    """
    """
    def __init__(self):
        """
        """
        self.__db = DB_Handler()
        self.__start()

    def __poll(self):
        """
        """
        print('--- SUCCESSFULLY CONNECTED ---')
        while True:
            inp = input(CMD)
            if inp.startswith('/'):
                cmd = inp[:2]
                if cmd in COMMANDS:
                    if cmd == '/a':
                        self.__task_add(inp)
                    elif cmd == '/d':
                        self.__task_done(inp)
                    elif cmd == '/r':
                        self.__task_remove(inp)
                    elif cmd == '/h':
                        self.__print_help()
                    else:
                        self.__quit_app()
                else:
                    print('Unhandled command type /h for help')
            else:
                print('Commands must start with \'/\'')
        self.__quit_app()

    def __print_help(self):
        """
        """
        helper = 'Available commands:\n'
        helper+= '\t/a <task_name> --- add a new task\n'
        helper+= '\t/d <task_name> --- pass the task to \'done\'\n'
        helper+= '\t/r <task_name> --- delete task\n'
        helper+= '\t/h             --- displays help\n'
        helper+= '\t/q             --- quit\n'
        print(helper)


    def __task_add(self, cmd):
        """
        """
        pass

    def __task_done(self, cmd):
        """
        """
        pass

    def __task_remove(self, cmd):
        """
        """
        pass

    def __quit_app(self):
        """
        """
        self.__db.disconnect()

    def __start(self):
        """
        """
        if not self.__db.check_user(): # user doest not exists
            msg = 'It seems that no users are registered \n'
            msg+= 'Do you want to sign in ? (y/n)'
            print(msg)

            inp = -1
            while inp not in ['y', 'n']:
                inp = input(CMD)

            if inp == 'y':
                print('\nPlease enter your informations: ')

                name = input('Name> ')

                psswd = 'foo'
                verif = 'bar'
                while psswd != verif:
                    psswd = getpass('Password> ')
                    verif = getpass('Repeat password> ')

                    if psswd != verif:
                        print('Passwords don\'t match')

                self.__db.user_register(name, psswd)

            else: 
                self.__quit_app()

        else: # user exists
            connected = 0

            while not connected:
                name  = input('User name: ')
                psswd = getpass('Password: ')
                connected = self.__db.connect(name, psswd)

        self.__poll() # start the app
