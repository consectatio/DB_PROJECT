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


def search_books(session, text):
    pass

def checkout_book(session, isbn, card_id):
    pass

def checkin_book(session, loan_id):
    pass

def create_borrower(session, fname, lname, ssn, address, city, state):
    bname = fname + "_" + lname
    address = address + ", " + city + ", " + state
    pass
