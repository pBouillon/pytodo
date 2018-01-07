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


ALL_TASKS = 0


class DB_Handler:
    """
    """
    def __init__(self, dest='./pytodo.db'):
        """
        """
        self.__conn   = sqlite3.connect(dest)
        self.__cursor = self.__conn.cursor()
        self.__conn.isolation_level = None

        self.create_base()

    def __database_abort(self, code, query=''):
        """
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

        if self.__conn:
            self.__cursor.close()
            self.__conn.close()
        exit(code)

    def __execute_query(self, query, param=''):
        """
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
        """
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
        """
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
        """
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
        """
        """
        try:
            with open('./todo_db.sql', 'r') as s:
                sql = s.read()
            tasks = sql.split('--')[0]
            user  = sql.split('--')[1]
        except OperationalError:
            self.__database_abort(1)
        except IOError:
            self.__database_abort(2)

        self.__execute_query(tasks)
        self.__execute_query(user)

    def disconnect(self):
        """
        """
        self.__cursor.close()
        self.__conn.close()

    def task_delete(self, task_id):
        """
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
        """
        """
        sql = '''
            UPDATE `TASK` 
            SET `done` = ? 
            WHERE `id` = ? ;
        '''
        self.__cursor.execute(sql, [state, task_id])

    def task_list (self):
        """
        """
        sql = '''
            SELECT *
            FROM `TASK` ;
        '''
        self.__execute_query(sql)
        
        tasks = self.__cursor.fetchall()
        return tasks

    def task_rename(self, task_id, topic):
        """
        """
        sql = '''
            UPDATE `TASK` 
            SET `topic` = ? 
            WHERE `id` = ? ;
        '''
        self.__cursor.execute(sql, [topic, task_id])

    def task_register(self, topic):
        """
        """
        sql = '''
            INSERT INTO `TASK`(`topic`) 
            VALUES (?) ;
        '''
        self.__cursor.execute(sql, [topic])

    def user_register(self, login, password):
        """
        """
        sql = '''
            INSERT INTO `USER`(`login`, `psswd`) 
            VALUES (?, ?) ;
        '''
        self.__cursor.execute(sql, [login, password])
