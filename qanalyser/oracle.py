#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python Jinja2 module import
from jinja2 import Template

# Application modules
from .odbc import db_odbc


class oracle_database(db_odbc):
    def __init__(
        self,
        server,
        instance,
        username,
        password,
        top_limit,
        port=None
    ):
        from os.path import dirname
        from os.path import join as join_path

        # Server / Database
        self.server = server
        self.instance = instance

        # Port
        if port is None:
            port = 1521  # Default Oracle SQL*Net Listener port

        # Oracle ODBC data source
        data_source = 'QanalyserOracle'

        # Connection string for ODBC
        odbc_string = self._generate_odbc_string(
            data_source=data_source,
            server=server,
            port=str(port),
            instance=instance,
            uid=username,
            pwd=password
        )

        # ODBC object
        super().__init__(
            odbc_string=odbc_string
        )

        # Jinja2 Templates
        self.STATS_QUERY_SQL_J2 = join_path(
            dirname(__file__), 'templates', 'oracle', 'stats_query.sql.j2'
        )
        self.STATS_REPORT_HTML_J2 = join_path(
            dirname(__file__), 'templates', 'oracle', 'stats_report.html.j2'
        )

        # Limit number of queries
        self.top_limit = int(top_limit)

    def stats_query(self, order_by):
        raise Exception('Stats query is in development for Oracle.')

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
        data_source,
        server,
        port,
        instance,
        uid,
        pwd
    ):
        return (
            'DSN={data_source};'
            'DQB={server}:{port}/{instance};'
            'UID={uid};'
            'PWD={pwd};'
        ).format(
            data_source=data_source,
            server=server,
            port=port,
            instance=instance,
            uid=uid,
            pwd=pwd
        )

    def _stats_report_html(self):
        raise Exception('HTML report is not supported for Oracle.')

    def _stats_report_xml(self):
        raise Exception('XML report is not supported for Oracle.')
