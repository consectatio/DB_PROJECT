from src.mypackage import manage_books
from src.mypackage import create_account
from src.mypackage import search
from src.mypackage import csv_to_sql
import os

def search_input():
    while True:
        print("Enter -1 to go back")
        print("Can search using ISBN, book title, author, or availability")
        user_input = input("Search: ")
        if user_input == "-1": return

        # create & call function in search.py
        # single text search do like some kind of matching in the following columns
        # ISBN, Book Title, author, and availability
        # print(search.search(user_input)

def check_out_input():
    while True:
        print("Provide either an ISBN number or Borrower ID")
        print("1. ISBN Number")
        print("2. Borrower ID")
        print("Enter -1 to go back")
        user_input = input("Search: ")
        if user_input == "-1": return
        elif user_input == "1": manage_books.checkout("ISBN Number")
        elif user_input == "2": manage_books.checkout("Borrower ID")
        else: print("Invalid input")

def check_in_input():
    while True:
        print("Enter -1 to go back")
        print("Can search using ISBN, Card #, or borrower name")
        print("1. ISBN Number")
        print("2. Card #")
        print("3. Borrower Name") # saved in DB as fname_lname will need to split("_") when using
        print("Enter -1 to go back")
        user_input = input("Search: ")
        if user_input == "-1": return
        elif user_input == "1": manage_books.checkin("ISBN Number")
        elif user_input == "2": manage_books.checkin("Card #")
        elif user_input == "3": manage_books.checkin("Borrower Name")
        else: print("Invalid input")

if __name__ == '__main__':
    if not os.path.exists(os.path.join("database", "database.db")):
        csv_to_sql.createDatabase()

    while True:
        print("1. Search for a book")
        print("2. Check out a book")
        print("3. Return book")
        print("4. Create an account") # add new borrowers
        user_input = input("Enter your choice: ")
        if user_input == "1": search_input()
        elif user_input == "2": check_out_input()
        elif user_input == "3": check_in_input()
        elif user_input == "4": create_account.create_borrower()
        else: print("Invalid input")
