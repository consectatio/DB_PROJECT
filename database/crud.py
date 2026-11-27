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
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from database.tables import Borrower, Authors, Book, Book_loans

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

def ssn_exists(session, ssn):
    return session.scalar(select(Borrower.card_id).where(Borrower.ssn == ssn)) is not None

def create_borrower(session, fname, lname, ssn,
                    address, city, state, phone=None):
    try:
        # Retrieve the highest existing card ID.
        last_id = session.scalar(
            select(func.max(Borrower.card_id))
        )

        # Verify that the existing ID follows the expected format.
        if last_id is not None:
            if (len(last_id) != 8
                    or not last_id.startswith("ID")
                    or not last_id[2:].isascii()
                    or not last_id[2:].isdigit()):
                raise ValueError("Unexpected card ID format.")

        # Generate the next card ID.
        next_number = int(last_id[2:]) + 1 if last_id else 1

        if next_number > 999999:
            raise ValueError("No more card IDs are available.")

        card_id = f"ID{next_number:06d}"

        # Create the new borrower record.
        borrower = Borrower(
            card_id=card_id,
            ssn=ssn,
            Bname=f"{fname}_{lname}",
            address=f"{address}, {city}, {state}",
            phone=phone
        )

        # Insert and commit the new record.
        session.add(borrower)
        session.commit()

        return card_id

    except Exception:
        session.rollback()
        raise
