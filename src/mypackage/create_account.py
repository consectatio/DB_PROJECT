def create_borrower(session):
    """
    have inputs and prints for:
        - fname (when inserting bname = fname_lname)
        - lname
        - SSN (no dashes (strip dashes) 9 digits
        - address attributes ("address": b["address"] + ", " + b["city"] + ", " + b["state"])
    values must not be null (ssn must be numbers
    """