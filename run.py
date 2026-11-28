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
        print("Enter -1 to go back")
        isbn = input("ISBN: ").strip()
        if isbn == "-1": 
            return
        card_id = input("Card ID: ").strip()
        if card_id == "-1": 
            continue
        ok, message = manage_books.checkout(session, isbn, card_id)
        print(message)

def check_in_input(session):
    while True:
        print("Enter -1 to go back")
        print("Search by ISBN, card ID, or borrower name")
        text = input("Search: ").strip()
        if text == "-1": return

        loans = manage_books.find_loans(session, text)
        if not loans:
            print("No checked-out books match that search.")
            continue

        print("NO | ISBN | TITLE | CARD ID | BORROWER | DUE")
        for n, loan in enumerate(loans, 1):
            print(f"{n} | {loan.isbn} | {loan.title} | {loan.card_id} | "
                  f"{loan.Bname.replace('_', ' ')} | {loan.due_date:%Y-%m-%d}")

        choice = input("Pick up to 3 numbers to check in (eg. 1 3), or -1 to search again: ").strip()
        if choice == "-1":
            continue
        ok, result = manage_books.parse_selection(choice, len(loans))
        if not ok:
            print(result)
            continue
        ok, message = manage_books.checkin(session, [loans[i].loan_id for i in result])
        print(message)

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
