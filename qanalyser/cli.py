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
            epilog=parser_epilog,
            usage='use "python -m qanalyser --help" for more information',
            formatter_class=argparse.RawTextHelpFormatter
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
                'name of the database management system'
            )
        )
        parser.add_argument(
            '-s',
            '--server',
            type=str,
            required=True,
            help=(
                'hostname of the database server'
            )
        )
        parser.add_argument(
            '-P',
            '--port',
            type=int,
            required=False,
            help=(
                'port to connect'
            )
        )
        parser.add_argument(
            '-i',
            '--instance',
            type=str,
            required=True,
            help=(
                'name of the instance:\n'
                '- database name (dbms: mssql)\n'
                '- service name (dbms: oracle)\n'
                '- SID (dbms: oracle)'
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
            '-x',
            '--export-type',
            type=str,
            choices=[
                'html',
                'xml'
            ],
            required=True,
            help=(
                'type of export'
            )
        )
        parser.add_argument(
            '-l',
            '--top-limit',
            type=str,
            required=True,
            help=(
                'limit of entries for the top-ranking'
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

        default_filename = '{dbms}_{server}_{instance}'.format(
            dbms=self.args.dbms,
            server=self.args.server,
            instance=self.args.instance.replace('.', '-')
        )

        if type == 'html':
            valid_extentions = (
                '.html',
                '.htm'
            )
            default_extention = '.html'
        if type == 'xml':
            valid_extentions = (
                '.xml'
            )
            default_extention = '.xml'

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
    from .oracle import oracle_database

    c = cli()

    if c.args.dbms == 'mssql':
        db_object = mssql_database(
            server=c.args.server,
            port=c.args.port,
            database=c.args.instance,
            username=c.args.username,
            password=c.args.password,
            top_limit=c.args.top_limit
        )
    elif c.args.dbms == 'openedge':
        print(
            'Progress OpenEdge will be supported in '
            'the upcoming releases, stay tuned!'
        )
        sys.exit(0)
    elif c.args.dbms == 'oracle':
        db_object = oracle_database(
            server=c.args.server,
            port=c.args.port,
            instance=c.args.instance,
            username=c.args.username,
            password=c.args.password,
            top_limit=c.args.top_limit
        )
    else:
        raise Exception(
            '{} is not supported.'.format(c.args.dbms)
        )

    output = db_object.stats_report(
        c.args.export_type
    )

    if c.file_path:
        with open(c.file_path, 'w+') as file_stream:
            file_stream.write(output)
    else:
        print(output)

    # Exit the application without error
    sys.exit(0)
