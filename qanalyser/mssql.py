#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All modules below are part of standard distribution for python
from os.path import dirname
from os.path import join as join_path
from datetime import datetime

# Python Jinja2 module import
from jinja2 import Template

# Application modules
from .odbc import db_odbc


class mssql_database(db_odbc):
    def __init__(self, server, database, username, password, top_limit):
        # Server / Database
        self.server = str(server)
        self.database = str(database)

        # Microsoft SQL driver name for ODBC
        driver = '{ODBC Driver 17 for SQL Server}'

        # ODBC object
        super().__init__(
            driver,
            self.server,
            self.database,
            str(username),
            str(password)
        )

        # Jinja2 Templates
        self.STATS_QUERY_SQL_J2 = join_path(
            dirname(__file__), 'templates', 'mssql', 'stats_query.sql.j2'
        )
        self.STATS_REPORT_HTML_J2 = join_path(
            dirname(__file__), 'templates', 'mssql', 'stats_report.html.j2'
        )

        # Limit number of queries
        self.top_limit = int(top_limit)

    def stats_query(self, order_by):
        with open(
            file=self.STATS_QUERY_SQL_J2,
            mode='r'
        ) as file_stream:
            query_template = Template(file_stream.read())
        query = query_template.render(
            top_limit=self.top_limit,
            database=self.database,
            order_by=order_by
        )
        columns, rows = self.select_query(query)
        return columns, rows

    def stats_report(self, type):
        from sys import stderr

        if type == 'html':
            return self._stats_report_html()
        else:
            print(
                'cannot generate the stats report because '
                'the type {} is not supported'.format(type),
                file=stderr
            )

    def _beautify_column_name(self, column_name):
        return str(column_name).replace('_', ' ').capitalize()

    def _stats_report_html(self):
        with open(
            file=self.STATS_REPORT_HTML_J2,
            mode='r'
        ) as file_stream:
            html_template = Template(file_stream.read())
        order_by_list = [
            {
                'column_name': 'execution_count',
                'column_alias': None
            },
            {
                'column_name': 'total_logical_reads',
                'column_alias': None
            },
            {
                'column_name': 'total_logical_writes',
                'column_alias': None
            },
            {
                'column_name': 'total_worker_time',
                'column_alias': None
            },
            {
                'column_name': 'total_elapsed_time',
                'column_alias': 'total_elapsed_time_in_second'
            }
        ]
        queries_result = []
        for order_by in order_by_list:
            query_result = {}
            columns, rows = self.stats_query(
                order_by['column_name']
            )
            if order_by['column_alias']:
                query_result[
                    'order_by_column_name'
                ] = self._beautify_column_name(
                    order_by['column_alias']
                )
                query_result[
                    'order_by_column_index'
                ] = columns.index(
                    order_by['column_alias']
                )
            else:
                query_result[
                    'order_by_column_name'
                ] = self._beautify_column_name(
                    order_by['column_name']
                )
                query_result[
                    'order_by_column_index'
                ] = columns.index(
                    order_by['column_name']
                )
            query_result['columns'] = [
                self._beautify_column_name(column) for column in columns
            ]
            query_result['rows'] = rows
            queries_result.append(query_result)
        report_datetime = datetime.now()
        html = html_template.render(
            server=self.server,
            database=self.database,
            top_limit=self.top_limit,
            queries_result=queries_result,
            report_date=report_datetime.strftime('%d-%m-%Y'),
            report_time=report_datetime.strftime('%H:%M')
        )
        return html
