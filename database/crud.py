"""
PUT ANY DATABASE QUERYING INSERTING OR WHATEVER THING IN HERE

you will need to probably need to import sqlAlchemy functions feel free to do so

for queries and reads default format should look something like;
rows = session.execute(select({something}).where({somethingelse})).all()
return rows

for writes / insert / upserts default format should be like:
try:
    session.add({whatever})
    session.commit()
except:
    session.rollback()
    print("something went wrong")
"""
from sqlalchemy import func, or_, select
from sqlalchemy.orm import selectinload

from database.tables import Authors, Book, Book_loans

def search_books(session, text):
    terms = text.split()
    if not terms:
        return []

    session.connection().connection.driver_connection.create_function(
        "casefold", 1, str.casefold, deterministic=True
    )
    active_loan = Book.loans.any(Book_loans.date_in.is_(None))
    query = select(Book, active_loan).options(selectinload(Book.authors))

    exact_isbn = session.execute(
        query.where(func.casefold(Book.isbn) == text.strip().casefold())
        .order_by(Book.isbn).limit(1)
    ).all()
    if exact_isbn:
        return exact_isbn

    for term in terms:
        term = term.casefold()
        query = query.where(or_(
            func.instr(func.casefold(Book.isbn), term) > 0,
            func.instr(func.casefold(Book.title), term) > 0,
            Book.authors.any(func.instr(func.casefold(Authors.Name), term) > 0),
        ))
    return session.execute(query.order_by(Book.title, Book.isbn)).all()

def checkout_book(session, isbn, card_id):
    pass

def checkin_book(session, loan_id):
    pass

def create_borrower(session, fname, lname, ssn, address, city, state):
    bname = fname + "_" + lname
    address = address + ", " + city + ", " + state
    pass
