import pandas as pd
from database import crud
from database.crud import query_fines


def create_borrower(session):
    print("\n--- Create Borrower Account ---")
    print("Enter -1 to go back a step")

    # -1 goes back one step, and from the first step back to the main menu
    step = 0
    while step < 7:
        # can only be letters
        if step == 0:
            fname = input("First name: ").strip()
            if fname == "-1": return
            if fname.isalpha(): step += 1
            else: print("Error: First name must contain letters only.")

        # can only be letters, and the combined name must fit the database column
        elif step == 1:
            lname = input("Last name: ").strip()
            if lname == "-1": step -= 1
            elif not lname.isalpha(): print("Error: Last name must contain letters only.")
            elif len(f"{fname}_{lname}") > 60: print("Error: Borrower name is too long.")
            else: step += 1

        # exactly nine digits, dashes are stripped
        elif step == 2:
            ssn = input("SSN: ").strip()
            if ssn == "-1": step -= 1
            else:
                ssn = ssn.replace("-", "")
                if not (len(ssn) == 9 and ssn.isascii() and ssn.isdigit()): print("Error: SSN must contain exactly 9 digits.")
                elif crud.ssn_exists(session, ssn): print("Error: A borrower with this SSN already exists.")
                else: step += 1

        elif step == 3:
            address = input("Street address: ").strip()
            if address == "-1": step -= 1
            elif address: step += 1
            else: print("Error: Street address is required.")

        elif step == 4:
            city = input("City: ").strip()
            if city == "-1": step -= 1
            elif city.isalpha(): step += 1
            else: print("Error: City must contain letters only.")

        elif step == 5:
            state = input("State: ").strip()
            if state == "-1": step -= 1
            elif not state.isalpha(): print("Error: State must contain letters only.")
            elif len(f"{address}, {city}, {state}") > 100: print("Error: Address is too long.")
            else: step += 1

        elif step == 6:
            phone = input("Phone number (optional): ").strip()
            if phone == "-1": step -= 1
            elif not phone or (phone.isascii() and phone.isdigit() and len(phone) <= 16): step += 1
            else: print("Error: Phone number must contain numbers only.")

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


# will need to show every borrower grouped by card_id with the amounts summed
# ^ probably just a public api to call the TODO crud function.
def display_fines(session):
    #print("\nEnter -1 to return to the main menu")
    user_input = input("Enter borrower card ID (optional): ").strip()
    if user_input == "-1": return
    fines = crud.query_fines(session, user_input)
    if not fines:
        print("No fines found.")
        return
    print(pd.DataFrame(fines, columns=["Card ID", "Total Fine"]).to_string(index=False))

def pay_fines(session):
    while True:
        user_input = input("Enter pay card ID: ").strip()
        if user_input == "-1": return
        if not crud.query_fines(session, user_input):
            print("Error: No unpaid fines found for that card ID.")
            continue
        paid = crud.pay_fines(session, user_input)
        if paid == 0:
            print("Error: Fines can only be paid once the book has been returned.")
            continue
        print(f"Paid ${paid} in fines for {user_input}.")
        return