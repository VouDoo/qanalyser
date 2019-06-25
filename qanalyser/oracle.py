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
        service_name,
        username,
        password,
        top_limit,
        port=None
    ):
        from os.path import dirname
        from os.path import join as join_path

        # Server / Database
        self.server = server
        self.service_name = service_name

        # ODBC object
        super().__init__(
            dbms='oracle',
            server=self.server,
            port=port,
            uid=username,
            pwd=password,
            service_name=self.service_name,
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

    def _stats_report_html(self):
        raise Exception('HTML report is not supported for Oracle.')

    def _stats_report_xml(self):
        raise Exception('XML report is not supported for Oracle.')
