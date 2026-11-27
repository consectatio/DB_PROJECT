from database import crud


def create_borrower(session):
    print("\n--- Create Borrower Account ---")

    # Collect the borrower's information.
    fname = input("First name: ").strip()
    lname = input("Last name: ").strip()
    ssn = input("SSN: ").strip().replace("-", "")
    address = input("Street address: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    phone = input("Phone number (optional): ").strip()

    # Verify that all required fields are provided.
    if not all([fname, lname, ssn, address, city, state]):
        print("Error: All required fields must be completed.")
        return

    # Verify that the SSN contains exactly nine digits.
    if len(ssn) != 9 or not ssn.isascii() or not ssn.isdigit():
        print("Error: SSN must contain exactly 9 digits.")
        return

    # Verify that inputs fit the database column lengths.
    if len(f"{fname}_{lname}") > 60:
        print("Error: Borrower name is too long.")
        return

    if len(f"{address}, {city}, {state}") > 100:
        print("Error: Address is too long.")
        return

    if len(phone) > 16:
        print("Error: Phone number is too long.")
        return

    # Attempt to create the borrower through the CRUD function.
    try:
        card_id = crud.create_borrower(
            session,
            fname,
            lname,
            ssn,
            address,
            city,
            state,
            phone or None
        )

        print("\nBorrower account created successfully!")
        print(f"Name: {fname} {lname}")
        print(f"Library Card ID: {card_id}")

    except ValueError as e:
        print(f"Error: {e}")

    except Exception:
        print("Error: Unable to create borrower account.")