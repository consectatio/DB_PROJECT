# HOW TO SET UP
1. HAVE ANY VERSION OF PYTHON (PROBABLY ANY VERSION)
2. in your cmd type `git clone (whatever i call the repo -> it's url)` will clone the code to whatever directory you are in.
3. create `py -m venv .venv` (your ide may already do it automatically)
3. type `pip install requirements.txt` (make sure you're in your venv / your venv is activated)
4. run the `src/mypackage/csv_to_sql.py` to get the database file generated in the database directory
5. okay you have working code now, for milestone 2 run the run.py: I left stubs for you guys to fill in.
    - PLEASE, you will have to make database CRUD update insert query whatever commands, put them and call them from the crud.py file, but put the logic code for the three functions in side the `src/mypackage/{function_whatever}.py` file.

# WHAT IS DONE
1. I have made the .db file (so the database and it's tables are made)
   - it is okay if you have broken the file just rerun the `csv_to_sql.py` file to get a brand new copy.

# WHAT NEEDS TO BE DONE
1. Create the `search` function -> `search.py`
2. Create the `checkout` function -> `manage_books.py`
3. Create the `checkin` function -> `manage_books.py`
4. Create the `create_borrowers` function -> `create_account.py`

- Write the logic for these functions in their respective file: `src/mypackage/{function}.py`
- Any required database commands should be in `database/crud.py`
- Hook them in to their respective places (call them) in the `run.py`. When running run.py should work.
- Update and remove the respective *what needs to be done* bullet points when done.
