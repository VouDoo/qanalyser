# Installation guide

Thanks for downloading Qanalyser.

Please, follow the order of each step carefully.

## Installing prerequisites

These following components **MUST** be installed on your system.

### Python

Ensure that **Python version 3.4 or newer** is installed on your system.

#### Install Python 3.4 on RHEL6

Run the command:

    sudo yum install python34 python34-libs python34-devel python34-pip

### UNIX ODBC

> This package is required for installing the Python module "pyodbc".

#### Install UNIX ODBC on RHEL6

Run the command:

    sudo yum install unixODBC-devel

### PyODBC

> This module is automatically installed during the Qanalyser installation.

To install the module with pip,
run the command:

    pip install pyodbc

### Jinja2

> This module is automatically installed during the Qanalyser installation.

To install the module with pip,
run the command:

    pip install Jinja2

### ODBC Driver for SQL Server

Follow the steps to install the ODBC Driver 17 for SQL Server.

> You do not need to install the optional packages.

How to install the Microsoft ODBC Driver for SQL Server: `https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017`

## Install Qanalyser

To install Qanalyser,
run the command:

    python setup.py install

> If you are upgrading from a previous version, you need to remove it first.

## Microsoft SQL Server specifications

### Add User permissions for SQL Server databases

Qanalyser requires a user with READ and VIEW SERVER STATE permissions on SQL Server databases.

1. Create a user in SQL Server if it does not exist (e.g. "qanalyser").

2. Run the T-SQL command lines:

    ```sql
    GRANT VIEW SERVER STATE TO '<user>'
    USE '<database_name>'
    EXEC sp_addrolemember 'db_datareader', '<user>'
    ```
