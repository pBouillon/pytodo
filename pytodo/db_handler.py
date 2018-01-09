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

import sqlite3
from sqlite3 import Error
from sqlite3 import OperationalError

import sys
from sys import exit
from sys import stderr


""" option to handle all rows of `TASKS` """
ALL_TASKS = 0

""" path to database save """
DB_SAVE_DEST = './pytodo.db'


class DB_Handler:
    """Reference DB_Handler

    Manipulate the sqlite database

    Attributes:
        __conn   : connection with the sqlite database
        __cursor : cursor to manipulate rows
    """
    def __init__(self, dest=DB_SAVE_DEST):
        """
        """
        self.__conn   = sqlite3.connect(dest)
        self.__cursor = self.__conn.cursor()
        self.__conn.isolation_level = None

        self.create_base()

    def __database_abort(self, code, query=''):
        """Exit with error

        Exit with a specified error
        and close the connection with the database

        Parameters:
            code  : error code
            query : query that made the request failed
        """
        errmsg = 'Error: '

        if code == 1:
            errmsg += 'Database initialization failed'
        elif code == 2:
            errmsg += 'SQL source file is missing'
        elif code == 3:
            errmsg += 'SQL request failed.'
            errmsg += query

        print(errmsg, file=stderr)

        self.disconnect()
        exit(code)

    def __execute_query(self, query, param=''):
        """Execute a given query

        Parameters:
            query : sql request
            param : parameter(s) for the request
        """
        try:
            if param:
                self.__cursor.execute(query, param)
            else:
                self.__cursor.execute(query)
        except Error:
            self.__conn.rollback()
            self.__database_abort(3, query)

    def delete_all(self):
        """Delete all datas (tasks + user)
        """
        sql = '''
            DROP TABLE `TASK` ;
        '''
        self.__execute_query(sql)
        sql = '''
            DROP TABLE `USER` ;
        '''
        self.__execute_query(sql)
        self.create_base()

    def user_exists(self):
        """Check if one user is registered

        Returns:
            Number of registered users
        """
        sql = '''
            SELECT count(*) 
            FROM `USER` ;
        '''

        self.__execute_query(sql)
        row = self.__cursor.fetchone()

        if row == None:
            self.__database_abort(4)
        return int(row[0])

    def connect(self, login, password):
        """Log a user

        Parameters:
            login    : user's login
            password : user's password

        Returns:
            users matching credentials login/passowrd
        """
        sql = '''
            SELECT count(*) 
            FROM  `USER` 
            WHERE `login` LIKE ? 
                AND `psswd` LIKE ? ;
        '''

        self.__execute_query(sql, [login, password])
        usr = self.__cursor.fetchone()

        if usr == None:
            self.__database_abort(4)
        return int(usr[0])

    def create_base(self):
        """Initialize the database

        Read the source file and execute it with SQLite
        """
        tasks = '''
            CREATE TABLE IF NOT EXISTS `TASK` (
                `id`     integer     primary key autoincrement,
                `topic`  varchar(50) not null,
                `done`   integer     default 0
            ) ;
        '''

        user= '''
            CREATE TABLE IF NOT EXISTS `USER` (
                `login`  varchar(150)  not null,
                `psswd`  varchar(150)  not null
            ) ;
        '''

        self.__execute_query(tasks)
        self.__execute_query(user)

    def disconnect(self):
        """Close the database
        """
        if self.__conn:
            self.__cursor.close()
            self.__conn.close()

    def task_delete(self, task_id):
        """Delete a task

        Parameters:
            task_id : id of the task to delete
        """
        if task_id == ALL_TASKS:
            sql = '''
                DELETE FROM `TASK` ;
            '''
            self.__cursor.execute(sql)
        else:
            sql = '''
                DELETE FROM `TASK` 
                WHERE `id` = ? ;
            '''
            self.__cursor.execute(sql, [task_id])

    def task_done (self, task_id, state=1):
        """Switch a task to `state`

        Parameters:
            task_id : id of the task to switch
            state   : state of the task (1 for done)
        """
        sql = '''
            UPDATE `TASK` 
            SET `done` = ? 
            WHERE `id` = ? ;
        '''
        self.__cursor.execute(sql, [state, task_id])

    def task_list (self):
        """Gather all rows of `TASKS`
    
        Returns:
            tasks: all rows as (id, topic, done)
        """
        sql = '''
            SELECT *
            FROM `TASK` ;
        '''
        self.__execute_query(sql)
        
        tasks = self.__cursor.fetchall()
        return tasks

    def task_rename(self, task_id, topic):
        """Rename a task

        Parameters:
            task_id : id of the task to rename
            topic   : new topic
        """
        sql = '''
            UPDATE `TASK` 
            SET `topic` = ? 
            WHERE `id` = ? ;
        '''
        self.__cursor.execute(sql, [topic, task_id])

    def task_register(self, topic):
        """Register a new task

        Parameters:
            topic : new task's topic
        """
        sql = '''
            INSERT INTO `TASK`(`topic`) 
            VALUES (?) ;
        '''
        self.__cursor.execute(sql, [topic])

    def user_register(self, login, password):
        """Register a new user

        Parameters:
            login    : user's login
            password : user's password
        """
        sql = '''
            INSERT INTO `USER`(`login`, `psswd`) 
            VALUES (?, ?) ;
        '''
        self.__cursor.execute(sql, [login, password])
