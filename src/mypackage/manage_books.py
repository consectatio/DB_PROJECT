# 3 max active book_loans
# give descriptive error log for if max books is checked out or that book is already checked out
# cannot check out books if the current borrower has a fine


from database import crud
from database.tables import refresh_fines

MAX_ACTIVE_LOANS = 3

def checkout(session, isbn, card_id):
    isbn = isbn.strip()
    card_id = card_id.strip().upper()

    if not crud.book_exists(session, isbn):
        return False, "404: Book not found"
    if not crud.borrower_exists(session, card_id):
        return False, "No borrower exists with this card ID"
    if crud.checked_out(session, isbn):
        return False, "Checkout Failed: Book, unavailable."

    currentBorrowCount = crud.loan_count(session, card_id)
    if currentBorrowCount >= MAX_ACTIVE_LOANS:
        return False, f"Checkout failed: {card_id} already has the maximum amount of books ({MAX_ACTIVE_LOANS}) checked out."

    # bring fines up to date
    refresh_fines(session)
    if crud.has_fines(session, card_id):
        return False, "Checkout failed: borrower has unpaid fines."

    try:
        loan = crud.checkout_book(session, isbn, card_id)
    except Exception:
        return False, "Checkout failed: Database Error"
    return True, f"{card_id} checked out {isbn}. Loan {loan.loan_id} is due on {loan.due_date:%Y-%m-%d}"

def checkin(session, input):
    pass