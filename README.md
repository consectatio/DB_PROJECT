# Library Management System - CS-4347 Milestone 2

Command-line library system written in Python with a SQLite database (SQLAlchemy ORM).

## Requirements
- Python 3.14 (developed and tested on 3.14.3; 3.11 or newer should also work)
- Third-party modules, pinned in `requirements.txt`: SQLAlchemy 2.1.9 and pandas 3.1.1 (these also install numpy, python-dateutil, typing_extensions and tzdata)
- No compiler or separate database server is needed. SQLite is part of Python.

## How to build and run
1. Unzip the archive and open a terminal in the unzipped `DB_PROJECT` folder.
2. (Recommended) Create and activate a virtual environment:
   ```
   py -m venv .venv
   .venv\Scripts\activate
   ```
3. Install the modules:
   ```
   pip install -r requirements.txt
   ```
4. Start the program from the project folder:
   ```
   python run.py
   ```

On the first run, the program creates `database/database.db` automatically from the CSV files in the `database` folder (books, authors, book_authors, borrowers). This takes a few seconds. To rebuild the database from scratch, delete `database/database.db` and run again.

## Using the program
The main menu is a list of numbered options. Type `-1` at any menu to go back (or to exit from the main menu).

1. **Search for a book** - one search box. Enter any part of an ISBN, title or author (case-insensitive). Results show ISBN, title, authors and IN/OUT status.
2. **Check out a book** - enter an ISBN and a borrower card ID. A borrower may have at most 3 books out, a book that is already out cannot be checked out, and borrowers with unpaid fines are refused. The due date is 14 days out.
3. **Return book** - search by ISBN, card ID or part of the borrower's name, then select 1 to 3 loans to check in.
4. **Create an account** - enter first name, last name, SSN, address, city, state and an optional phone number. A card ID is generated automatically, and a duplicate SSN is rejected.
5. **Fines** - display fines grouped by card ID (unpaid only), or pay all of one borrower's fines (only books that have been returned can be paid).

## Fines
Fines are $0.25 per day late. They are refreshed automatically every time `run.py` starts and whenever a book is checked out or checked in.
