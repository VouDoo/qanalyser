#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All modules below are part of standard distribution for python
import argparse
from sys import exit, stderr
from os.path import normpath, isdir
from os.path import join as join_path
from os.path import normcase as normcase_path

# Application modules
from .mssql import mssql_database

if __name__ == '__main__':
    # Arguments parser
    parser_desc = (
        'QAnalyser - '
        'a simple tool for analyzing queries in databases'
    )
    parser_epilog = (
        'If you encounter any issue, '
        'please, log an issue on GitHub.'
    )
    parser = argparse.ArgumentParser(
        description=parser_desc,
        epilog=parser_epilog
    )
    parser.add_argument(
        'dbms',
        type=str,
        choices=['mssql', 'openedge', 'oracle'],
        help='select the DBMS'
    )
    parser.add_argument(
        '--server',
        type=str,
        required=True,
        help='name of the database server'
    )
    parser.add_argument(
        '--database',
        type=str,
        required=True,
        help='name of the database'
    )
    parser.add_argument(
        '--username',
        type=str,
        required=True,
        help='name of the database user'
    )
    parser.add_argument(
        '--password',
        type=str,
        required=True,
        help='password string of the database user'
    )
    parser.add_argument(
        '--top-limit',
        type=str,
        required=True,
        help='Number of top queries'
    )
    parser.add_argument(
        '--save-html',
        type=str,
        required=True,
        help='save HTML reports in a directory'
    )
    args = parser.parse_args()

    save_html_dir = normcase_path(normpath(args.save_html))
    if not isdir(save_html_dir):
        print(
            'the path referred in --save-html is not a directory',
            file=stderr
        )

    if args.dbms == 'mssql':
        db_object = mssql_database(
            args.server,
            args.database,
            args.username,
            args.password,
            args.top_limit
        )
        html = db_object.stats_report_html()
        html_file = join_path(
            save_html_dir,
            '{server}_{database}_mssql_report.html'.format(
                server=db_object.server,
                database=db_object.database
            )
        )
        with open(html_file, 'w+') as file_stream:
            file_stream.write(html)

    elif args.dbms == 'openedge':
        print('To be developed.')

    elif args.dbms == 'oracle':
        print('To be developed.')

    else:
        print(
            'Incorrect referred DBMS.',
            file=stderr
        )

    # Exit the application without error
    exit(0)
