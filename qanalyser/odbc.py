#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python ODBC module import
import pyodbc


class db_odbc():
    def __init__(self, odbc_string):
        self.odbc_string = odbc_string

    def select_query(self, query):
        try:
            conn = pyodbc.connect(self.odbc_string)
            cursor = conn.cursor()
            rows = cursor.execute(query).fetchall()
            columns = [column[0] for column in cursor.description]
            cursor.close()
            conn.close()
            return columns, rows
        except Exception as e:
            raise e
