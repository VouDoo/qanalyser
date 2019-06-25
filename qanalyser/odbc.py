#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python ODBC module import
import pyodbc


class db_odbc():
    def __init__(
        self,
        dbms,
        server,
        uid,
        pwd,
        service_name=None,
        database=None,
        port='',
    ):
        if dbms == 'mssql':
            # Microsoft SQL driver name for ODBC
            driver = 'ODBC Driver 17 for SQL Server'
            if driver not in pyodbc.drivers():
                raise Exception(
                    'The ODBC driver "{}" does not exist.'.format(
                        driver
                    )
                )
            # Gererate the ODBC string
            if database is None:
                raise Exception(
                    'The database name is mandatory '
                    'to initialize the ODBC connection '
                    'to a Microsoft SQL server database.'
                )
            if port is None:
                port = '1433'  # Default instance running over TCP port
            self.odbc_string = (
                'DRIVER={driver};'
                'SERVER={server},{port};'
                'DATABASE={database};'
                'UID={uid};'
                'PWD={pwd};'
            ).format(
                driver=str('{' + driver + '}'),
                server=server,
                port=port,
                database=database,
                uid=uid,
                pwd=pwd
            )
        elif dbms == 'oracle':
            # Oracle data source for ODBC
            data_source = 'QanalyserOracle'
            if data_source not in pyodbc.dataSources():
                raise Exception(
                    'The ODBC data source "{}" does not exist.'.format(
                        data_source
                    )
                )
            # Gererate the ODBC string
            if service_name is None:
                raise Exception(
                    'The service name is mandatory '
                    'to initialize the ODBC connection '
                    'to an Oracle database.'
                )
            if port is None:
                port = '1521'  # Default Oracle SQL*Net Listener port
            self.odbc_string = (
                'DSN={data_source};'
                'DQB={server}:{port}/{service_name};'
                'UID={uid};'
                'PWD={pwd};'
            ).format(
                data_source=data_source,
                server=server,
                port=port,
                service_name=service_name,
                uid=uid,
                pwd=pwd
            )
        else:
            raise Exception(
                'The ODBC connection cannot be initialized for this DBMS.'
            )

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
