# Installation guide

Thanks for downloading Qanalyser.

Please, follow the order of each step carefully.

## Installing prerequisites

These following components **MUST** be installed on your system.

### Python

Ensure that **Python version 3.4 or newer** is installed on your system.

#### Linux

On RHEL or CentOS, install the following packages:

- python3
- python3-libs
- python3-devel
- python3-pip

> Package names can vary depending on your Linux distribution.

#### Windows

Download and install the latest version of Python for Windows on <https://www.python.org/downloads/>

### ODBC Driver

> ODBC is required for using the Python module "pyodbc".

#### Linux

On RHEL or CentOS, install the following package:

- unixODBC-devel

> Package names can vary depending on your Linux distribution.

#### Windows

ODBC driver is part of the recent Windows operating systems.

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

### Microsoft ODBC Driver for SQL Server (only for Linux systems)

> Install this driver only if you need to connect Qanalyser to SQL Server.

#### Linux

Follow the steps to install the ODBC Driver 17 for SQL Server:

_How to install the Microsoft ODBC Driver for SQL Server_ - <https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017>

> You do not need to install the optional packages.

#### Windows

Download and install the ODBC Driver 17 for SQL Server:

From Microsoft Download Center - <https://www.microsoft.com/en-us/download/details.aspx?id=56567>

### Instant Client for Oracle

> Install this driver only if you need to connect Qanalyser to Oracle.

#### Linux

On RHEL or CentOS, follow the steps to install Instant Client for Oracle:

_Install the Oracle Instant Client (ODBC Driver) for Linux_ - <https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-Oracle-from-RHEL-or-Centos#install-the-oracle-instant-client-odbc-driver-for-linux>

#### Windows

Go to <https://www.oracle.com/technetwork/topics/winsoft-085727.html>

Download (requires an Oracle account) and install the following packages:

- Basic Light Package
- ODBC Package

> These packages are for Windows 32-bit. It is required for pyodbc.

##### Install Instant Client Basic Light Package

Extract the Zip archive in the directory:

    C:\Oracle\instantclient\

##### Install Instant Client ODBC Package

Extract the Zip archive in the same directory as Instant Client Basic Light Package.

Execute the file as administrator:

    odbc_install.exe

##### Add Data Source in ODBC Data Sources (32-bit)

Open "ODBC Data Source (32-bit)".

> Before starting, ensure that you have "Oracle in _dirname_" into the list in "Drivers".

To add the data source, follow the steps carefully:

1. Go to "User DSN"
2. Click on "Add"
3. Select "Oracle in _dirname_"
4. Click on "Finish"
5. Enter *"QanalyserOracle"* in "Data Source Name" (Please, do not change the name)
6. Check the "Read-Only Connection" box
7. Click on "OK" and apply the changes

## Install Qanalyser

To install Qanalyser,
run the command:

    python setup.py install

> If you are upgrading from a previous version, you need to remove it first.

## DBMS specifications

### Microsoft SQL Server

#### Add User permissions for SQL Server databases

Qanalyser requires a user with READ and VIEW SERVER STATE permissions on SQL Server databases.

1. Create a user in SQL Server if it does not exist.

2. Run the T-SQL command lines:

    ```sql
    GRANT VIEW SERVER STATE TO '<username>'
    USE '<database_name>'
    EXEC sp_addrolemember 'db_datareader', '<username>'
    ```

### Oracle

Qanalyser requires a user with READ ONLY permission on Oracle databases.

1. Connect on the database

2. Run the SQL command lines:

    ```sql
    create user '<username>' identified by '<password>';
    grant create session to '<username>';
    grant select any table to '<username>';
    ```
