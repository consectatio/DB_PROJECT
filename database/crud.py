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
from sqlalchemy import select, func
from database.tables import Borrower

def search_books(session, text):
    pass

def checkout_book(session, isbn, card_id):
    pass

def checkin_book(session, loan_id):
    pass

def create_borrower(session, fname, lname, ssn,
                    address, city, state, phone=None):
    try:
        # Check if a borrower with this SSN already exists.
        existing = session.scalar(
            select(Borrower.card_id).where(Borrower.ssn == ssn)
        )

        if existing is not None:
            raise ValueError("A borrower with this SSN already exists.")

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