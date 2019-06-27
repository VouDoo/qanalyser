#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All modules below are part of standard distribution for python
from datetime import datetime

# Python Jinja2 module import
from jinja2 import Template

# Application modules
from .odbc import db_odbc


class mssql_database(db_odbc):
    def __init__(
        self,
        server,
        database,
        username,
        password,
        top_limit,
        port=None
    ):
        from os.path import dirname
        from os.path import join as join_path

        # Server / Database
        self.server = server
        self.database = database

        # Port
        if port is None:
            port = 1433  # Default instance running over TCP port

        # Microsoft SQL Server ODBC driver
        driver = 'ODBC Driver 17 for SQL Server'

        # Connection string for ODBC
        odbc_string = self._generate_odbc_string(
            driver=driver,
            server=server,
            port=str(port),
            database=database,
            uid=username,
            pwd=password
        )

        # ODBC object
        super().__init__(
            odbc_string=odbc_string,
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
        if type == 'html':
            return self._stats_report_html()
        elif type == 'xml':
            return self._stats_report_xml()
        else:
            raise Exception(
                'Cannot generate the stats report. '
                'The type "{}" is not supported.'.format(type)
            )

    def _generate_odbc_string(
        self,
        driver,
        server,
        port,
        database,
        uid,
        pwd
    ):
        return (
            'DRIVER={driver};'
            'SERVER={server},{port};'
            'DATABASE={database};'
            'UID={uid};'
            'PWD={pwd};'
        ).format(
            driver=('{' + driver + '}'),
            server=server,
            port=port,
            database=database,
            uid=uid,
            pwd=pwd
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

    def _stats_report_xml(self):
        import xml.etree.cElementTree as ET

        order_by_list = (
            'execution_count',
            'total_logical_reads',
            'total_logical_writes',
            'total_worker_time',
            'total_elapsed_time'
        )

        root = ET.Element("report")  # Initialize tree
        server_elem = ET.SubElement(root, 'server')
        server_elem.text = self.server
        database_elem = ET.SubElement(root, 'database')
        database_elem.text = self.database
        top_elem = ET.SubElement(root, 'top_queries')
        top_elem.set('limit', str(self.top_limit))
        for order_by in order_by_list:
            columns, rows = self.stats_query(order_by)
            order_by_elem = ET.SubElement(top_elem, 'order_by')
            order_by_elem.set('name', order_by)
            rank = 1
            for row in rows:
                query_elem = ET.SubElement(order_by_elem, 'query')
                query_elem.set('rank', str(rank))
                for i in range(len(columns)):
                    column_elem = ET.SubElement(query_elem, 'column')
                    column_elem.set('name', str(columns[i]))
                    column_elem.text = str(row[i])
                rank += 1
        root.set(
            'reported_datetime',
            datetime.now().strftime('%d-%m-%Y_%H:%M')
        )

        return ET.tostring(root).decode()
