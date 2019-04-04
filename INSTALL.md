# Installation guide

Thanks for downloading Qanalyser.

Please, follow the order of each step carefully.

## Installing prerequisites

These following components **MUST** be installed on your system.

### Python

Ensure that **Python version 3.4 or newer** is installed on your system.

#### Linux

Install the following packages:

- python3
- python3-libs
- python3-devel
- python3-pip

> Package names can vary depending on your Linux distribution.

#### Windows

Download and install the latest version of Python for Windows on <https://www.python.org/downloads/>

### UNIX ODBC

> ODBC is required for using the Python module "pyodbc".

#### Linux

Install the following package:

- unixODBC-devel

> Package names can vary depending on your Linux distribution.

#### Windows

ODBC is part of the recent Windows operating systems.

### PyODBC

> This module is automatically installed during the Qanalyser installation.

To install the module with pip,
run the command:

    pip install pyodbc

> Ensure that pip uses the correct version of Python

### Jinja2

> This module is automatically installed during the Qanalyser installation.

To install the module with pip,
run the command:

    pip install Jinja2

> Ensure that pip uses the correct version of Python

### ODBC Driver for SQL Server

Follow the steps to install the ODBC Driver 17 for SQL Server.

> You do not need to install the optional packages.

How to install the Microsoft ODBC Driver for SQL Server: <https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017>

## Install Qanalyser

To install Qanalyser,
run the command:

    python setup.py install

> If you are upgrading from a previous version, you need to remove it first.

## DBMS specifications

### Microsoft SQL Server

#### Add User permissions for SQL Server databases

Qanalyser requires a user with READ and VIEW SERVER STATE permissions on SQL Server databases.

1. Create a user in SQL Server if it does not exist (e.g. "qanalyser").

2. Run the T-SQL command lines:

    ```sql
    GRANT VIEW SERVER STATE TO '<user>'
    USE '<database_name>'
    EXEC sp_addrolemember 'db_datareader', '<user>'
    ```
