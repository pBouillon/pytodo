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

COMMANDS = [
    CMD_ADD ,
    CMD_DONE,
    CMD_HELP,
    CMD_LIST,
    CMD_QUIT,
    CMD_REMOVE
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
        print('\n--- SUCCESSFULLY CONNECTED ---\n')
        while True:
            inp = input(CMD_INPUT)
            if inp.startswith(CMD_PREFIX):
                cmd = inp.split()[0]
                if cmd in COMMANDS:
                    if cmd == CMD_LIST :
                        self.__task_list()
                    elif cmd == CMD_ADD:
                        self.__task_add(inp)
                    elif cmd == CMD_DONE:
                        self.__task_done(inp)
                    elif cmd == CMD_REMOVE:
                        self.__task_remove(inp)
                    elif cmd == CMD_HELP :
                        self.__print_help()
                    else:
                        self.__quit_app()
                else:
                    print('Unhandled command type ' + CMD_HELP +' for help')
            else:
                print('Commands must start with \'' + CMD_PREFIX + '\'')

    def __print_help(self):
        """
        """
        helper = 'Available commands:\n'
        helper+= '\t'+CMD_ADD   +' [desc] .. add a new task\n'
        helper+= '\t'+CMD_DONE  +' id ...... pass the task to \'done\'\n'
        helper+= '\t'+CMD_LIST  +' ......... list all tasks\n'
        helper+= '\t'+CMD_REMOVE+' id ...... remove the task\n'
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
        print('Task added.\n')

    def __task_done(self, cmd):
        """
        """
        if len(cmd.split()) < 2:
            print('Missing parameter, see ' + CMD_HELP + '.\n')
        else:
            task_id = cmd.split()[1]
            self.__db.task_done(task_id)
            print('Task status changed.\n')

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
            print('Task removed.\name')

    def __quit_app(self):
        """
        """
        self.__db.disconnect()
        print('--- SUCCESSFULLY DISCONNECTED ---')
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

                name = input('Name> ')

                psswd = 'foo'
                verif = 'bar'
                while psswd != verif:
                    psswd = getpass('Password> ')
                    verif = getpass('Repeat password> ')

                    if psswd != verif:
                        print('\nPasswords don\'t match')

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
                    print('\nLogin failed.')

        self.__poll() # start the app
