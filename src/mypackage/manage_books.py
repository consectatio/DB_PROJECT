# 3 max active book_loans
# give descriptive error log for if max books is checked out or that book is already checked out
# cannot check out books if the current borrower has a fine


from database import crud
from database.tables import refresh_fines

MAX_ACTIVE_LOANS = 3
MAX_CHECKIN = 3

def checkout(session, isbn, card_id):
    isbn = isbn.strip()
    card_id = card_id.strip().upper()

    if not crud.book_exists(session, isbn):
        return False, "404: Book not found"
    if not crud.borrower_exists(session, card_id):
        return False, "Who is this? No borrower exists with this card ID"
    if crud.checked_out(session, isbn):
        return False, "Checkout Failed: Book, unavailable."

    currentBorrowCount = crud.loan_count(session, card_id)
    if currentBorrowCount >= MAX_ACTIVE_LOANS:
        return False, f"Checkout failed: {card_id} already has {currentBorrowCount} books checked out. The maximum allowed is {MAX_ACTIVE_LOANS}"

    # bring fines up to date
    refresh_fines(session)
    if crud.has_fines(session, card_id):
        return False, "Checkout failed: borrower has unpaid fines"

    try:
        loan = crud.checkout_book(session, isbn, card_id)
    except Exception:
        return False, "Checkout failed: Database Error"
    return True, f"{card_id} checked out {isbn}. Loan {loan.loan_id} is due on {loan.due_date:%Y-%m-%d}"

#def checkout(session, input):
#    pass

# def checkin(session, input):
#     pass


def find_loans(session, text):
    return crud.get_open_loans(session, text)

def parse_selection(text, count):
    parts = text.replace(",", " ").split()
    if not parts:
        return False, "Error, enter at least one selection"
    if not all(p.isascii() and p.isdigit() for p in parts):
        return False, "Error: only enter intigers"
    picks = sorted({int(p) for p in parts})
    if len(picks) > MAX_CHECKIN:
        return False, f"Error: You can only check in a maximum of {MAX_CHECKIN} books at once."
    if picks[0] < 1 or picks[-1] > count:
        return False, f"Error: out of range 1 – {count}." # Minor note, did you know the en-dash is the proper dash for ranges? Very obscure formnatting thing.
    return True, [p - 1 for p in picks]

def checkin(session, loan_ids):
    if not 1 <= len(loan_ids) <= MAX_CHECKIN:
        return False, f"Error: You can only check in a maximum of {MAX_CHECKIN} books at once, and must check in at least one."
    try:
        loans = crud.checkin_books(session, loan_ids)
    except Exception:
        return False, "Check-in failed: Database Error"
    if not loans:
        return False, "Error: Those books are already checked in."
    refresh_fines(session)
    lines = [f"Checked in {len(loans)} book(s):"]
    for loan in loans:
        late = " (late - fine assessed)" if loan.fine and not loan.fine.paid else ""
        lines.append(f"  {loan.isbn} {loan.book.title}{late}")
    return True, "\n".join(lines)