from src.mypackage import manage_books
from src.mypackage import accounts
from src.mypackage import search
from src.mypackage import csv_to_sql
from database.tables import SessionLocal, refresh_fines
import os

def search_input(session):
 while True:
        print("Enter -1 to go back")
        print("Search by ISBN, book title, or author")
        user_input = input("Search: ")
        if user_input == "-1": return

        results = search.search(session, user_input)
        if not results:
            print("No books found.")
            continue
        print("ISBN | TITLE | AUTHORS | STATUS")
        for isbn, title, authors, status in results:
            print(f"{isbn} | {title} | {authors} | {status}")

def check_out_input(session):
    while True:
        print("Provide either an ISBN number or Borrower ID")
        print("1. ISBN Number")
        print("2. Borrower ID")
        print("Enter -1 to go back")
        user_input = input("Search: ")
        if user_input == "-1": return
        elif user_input == "1": manage_books.checkout(session, "ISBN Number")
        elif user_input == "2": manage_books.checkout(session, "Borrower ID")
        else: print("Invalid input")

def check_in_input(session):
    while True:
        print("Enter -1 to go back")
        print("Can search using ISBN, Card #, or borrower name")
        print("1. ISBN Number")
        print("2. Card #")
        print("3. Borrower Name") # saved in DB as fname_lname will need to split("_") when using
        print("Enter -1 to go back")
        user_input = input("Search: ")
        if user_input == "-1": return
        elif user_input == "1": manage_books.checkin(session, "ISBN Number")
        elif user_input == "2": manage_books.checkin(session, "Card #")
        elif user_input == "3": manage_books.checkin(session, "Borrower Name")
        else: print("Invalid input")

def fines_input(session):
    while True:
        print("Enter -1 to go back")
        print("1. Display fines")
        print("2. Pay fines")
        user_input = input("Enter your choice: ")
        if user_input == "-1": return
        elif user_input == "1": accounts.display_fines(session)
        elif user_input == "2": accounts.pay_fines(session)
        else: print("Invalid input")

if __name__ == '__main__':
    if not os.path.exists(os.path.join("database", "database.db")):
        csv_to_sql.createDatabase()

    session = SessionLocal()
    refresh_fines(session)

    while True:
        print("Enter -1 to exit")
        print("1. Search for a book")
        print("2. Check out a book")
        print("3. Return book")
        print("4. Create an account") # add new borrowers
        print("5. Fines")
        user_input = input("Enter your choice: ")
        if user_input == "-1":
            session.close()
            exit(0)
        elif user_input == "1": search_input(session)
        elif user_input == "2": check_out_input(session)
        elif user_input == "3": check_in_input(session)
        elif user_input == "4": accounts.create_borrower(session)
        elif user_input == "5": fines_input(session)
        else: print("Invalid input")
