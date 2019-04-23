#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All modules below are part of standard distribution for python
import sys


class cli():
    def __init__(self):
        self.args = self._built_parser().parse_args()
        self.file_path = None
        if self.args.file:
            self.file_path = self._gen_file_path(
                self.args.file,
                self.args.export_type
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
                'name of the DBMS'
            )
        )
        parser.add_argument(
            '-s',
            '--server',
            type=str,
            required=True,
            help=(
                'name of the database server'
            )
        )
        parser.add_argument(
            '-d',
            '--database',
            type=str,
            required=True,
            help=(
                'name of the database'
            )
        )
        parser.add_argument(
            '-u',
            '--username',
            type=str,
            required=True,
            help=(
                'name of the database user'
            )
        )
        parser.add_argument(
            '-p',
            '--password',
            type=str,
            required=True,
            help=(
                'password of the database user'
            )
        )
        parser.add_argument(
            '-l'
            '--top-limit',
            type=str,
            required=True,
            help=(
                'number of entries for the top'
            )
        )
        parser.add_argument(
            '-x',
            '--export-type',
            type=str,
            choices=[
                'csv',
                'html'
            ],
            required=True,
            help=(
                'type of export'
            )
        )
        parser.add_argument(
            '-f',
            '--file',
            type=str,
            required=False,
            help=(
                'save output in file'
            )
        )
        return parser

    def _format_path(self, path):
        from os.path import normpath, normcase

        return normcase(normpath(path))

    def _gen_file_path(self, path, type):
        from os.path import isdir
        from os.path import join

        default_filename = '{dbms}_{server}_{database}'.format(
            dbms=self.args.dbms,
            server=self.args.server,
            database=self.args.database
        )

        if type == 'html':
            valid_extentions = (
                '.html',
                '.htm'
            )
            default_extention = '.html'
        if type == 'csv':
            valid_extentions = (
                '.csv'
            )
            default_extention = '.csv'

        formated_path = self._format_path(path)
        if isdir(formated_path):
            return join(
                formated_path,
                default_filename,
                default_extention
            )
        else:
            if not formated_path.endswith(valid_extentions):
                formated_path += default_extention
            return formated_path


def run():
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

    elif c.args.dbms == 'openedge':
        print(
            'Progress OpenEdge will be supported in '
            'the upcoming releases, stay tuned!',
        )
        sys.exit(0)
    elif c.args.dbms == 'oracle':
        print(
            'Oracle will be supported in'
            'the upcoming releases, stay tuned!',
        )
        sys.exit(0)
    else:
        print(
            '{} is not supported.'.format(c.args.dbms),
            file=sys.stderr
        )

    output = db_object.stats_report(
        c.args.export_type
    )

    if c.args.file_path:
        with open(c.file_path, 'w+') as file_stream:
            file_stream.write(output)
    else:
        print(output)

    # Exit the application without error
    sys.exit(0)
