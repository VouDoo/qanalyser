#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All modules below are part of standard distribution for python
import sys


class cli():
    def __init__(self):
        from os.path import isdir

        self.args = self._built_parser().parse_args()
        self.args.save_html = self._format_path(self.args.save_html)
        if not isdir(self.args.save_html):
            print(
                'the path referred in --save-html is not a directory',
                file=sys.stderr
            )

    def _built_parser(self):
        import argparse

        # Arguments parser
        parser_desc = (
            'Qanalyser - '
            'a simple tool for analyzing queries in databases'
        )
        parser_epilog = (
            'If you encounter any problems, '
            'please log an issue on GitHub.'
        )
        parser = argparse.ArgumentParser(
            description=parser_desc,
            epilog=parser_epilog
        )
        parser.add_argument(
            'dbms',
            type=str,
            choices=[
                'mssql',
                'openedge',
                'oracle'
            ],
            help=(
                'select the DBMS'
            )
        )
        parser.add_argument(
            '--server',
            type=str,
            required=True,
            help=(
                'name of the database server'
            )
        )
        parser.add_argument(
            '--database',
            type=str,
            required=True,
            help=(
                'name of the database'
            )
        )
        parser.add_argument(
            '--username',
            type=str,
            required=True,
            help=(
                'name of the database user'
            )
        )
        parser.add_argument(
            '--password',
            type=str,
            required=True,
            help=(
                'password string of the database user'
            )
        )
        parser.add_argument(
            '--top-limit',
            type=str,
            required=True,
            help=(
                'limit number of top queries'
            )
        )
        parser.add_argument(
            '--save-html',
            type=str,
            required=True,
            help=(
                'save HTML reports in a directory'
            )
        )
        return parser

    def _format_path(self, path):
        from os.path import normpath, normcase

        return normcase(normpath(path))


def main():
    from os.path import join as join_path
    # Application modules
    from .mssql import mssql_database

    c = cli()

    if c.args.dbms == 'mssql':
        db_object = mssql_database(
            c.args.server,
            c.args.database,
            c.args.username,
            c.args.password,
            c.args.top_limit
        )
        html = db_object.stats_report_html()
        html_file = join_path(
            c.args.save_html,
            '{server}_{database}_mssql_report.html'.format(
                server=db_object.server,
                database=db_object.database
            )
        )
        with open(html_file, 'w+') as file_stream:
            file_stream.write(html)

    elif c.args.dbms == 'openedge':
        print('Progress OpenEdge is not supported yet.')

    elif c.args.dbms == 'oracle':
        print('Oracle is not supported yet.')

    # Exit the application without error
    sys.exit(0)
