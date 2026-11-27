# HOW TO SET UP
1. HAVE ANY VERSION OF PYTHON (PROBABLY ANY VERSION)
2. in your cmd type `git clone https://github.com/consectatio/DB_PROJECT` will clone the code to whatever directory you are in.
3. create `py -m venv .venv` (your ide may already do it automatically)
3. type `pip install requirements.txt`
4. okay you have working code now, for milestone 2 run the run.py: I left stubs for you guys to fill in.
    - PLEASE, you will have to make database CRUD update insert query whatever commands, put them and call them from the crud.py file, but put the logic code for the three functions in side the `src/mypackage/{function_whatever}.py` file.

# WHAT IS DONE
1. I have made the .db file (so the database and it's tables are made)
   - it is okay if you have broken the file just rerun the `csv_to_sql.py` file to get a brand new copy.
2. Create the `search` function -> `search.py`
# WHAT NEEDS TO BE DONE
1. Create the `checkout` function -> `manage_books.py`
2. Create the `checkin` function -> `manage_books.py`
3. Create the `create_borrowers` function -> `create_account.py`

- Write the logic for these functions in their respective file: `src/mypackage/{function}.py`
- Any required database commands should be in `database/crud.py`
- Also reuse the database session that is passed in and to wrap database writes in a try loop with the main success route
being `session.commit()` and the except side having `session.rollback()`.
- Hook them in to their respective places (call them) in the `run.py`. When running run.py should work.
- Update and remove the respective *what needs to be done* bullet points when done.
