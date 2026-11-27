from database import crud


def create_borrower(session):
    print("\n--- Create Borrower Account ---")
    print("Enter -1 to go back")

    # can only be letters
    while True:
        fname = input("First name: ").strip()
        if fname == "-1": return
        if fname.isalpha(): break
        print("Error: First name must contain letters only.")

    # can only be letters, and the combined name must fit the database column
    while True:
        lname = input("Last name: ").strip()
        if lname == "-1": return
        if not lname.isalpha(): print("Error: Last name must contain letters only.")
        elif len(f"{fname}_{lname}") > 60: print("Error: Borrower name is too long.")
        else: break

    # exactly nine digits, dashes are stripped
    while True:
        ssn = input("SSN: ").strip()
        if ssn == "-1": return
        ssn = ssn.replace("-", "")
        if len(ssn) == 9 and ssn.isascii() and ssn.isdigit(): break
        print("Error: SSN must contain exactly 9 digits.")

    while True:
        address = input("Street address: ").strip()
        if address == "-1": return
        if address: break
        print("Error: Street address is required.")

    while True:
        city = input("City: ").strip()
        if city == "-1": return
        if city.isalpha(): break
        print("Error: City must contain letters only.")

    while True:
        state = input("State: ").strip()
        if state == "-1": return
        if not state.isalpha(): print("Error: State must contain letters only.")
        elif len(f"{address}, {city}, {state}") > 100: print("Error: Address is too long.")
        else: break

    while True:
        phone = input("Phone number (optional): ").strip()
        if phone == "-1": return
        if not phone: break
        if phone.isascii() and phone.isdigit() and len(phone) <= 16: break
        print("Error: Phone number must contain numbers only.")

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
