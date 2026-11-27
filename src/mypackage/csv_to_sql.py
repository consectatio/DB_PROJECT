# run once to convert the csvs into an sqllite database (saved to database/database.db)
import sys
import pandas as pd
from pathlib import Path
from sqlalchemy import select
from database.tables import SessionLocal, Book, engine, init_db

ROOT = Path(__file__).resolve().parents[2]
CSV_DIR = ROOT / "database"
sys.path.insert(0, str(ROOT))


def createDatabase() -> None:
    init_db()

    with SessionLocal() as session:
        if session.scalars(select(Book).limit(1)).first():
            print("database already has data - nothing imported.")
            return

    books = pd.read_csv(CSV_DIR / "books.csv").rename(columns={"ISBN13": "isbn", "Title": "title"})

    authors = pd.read_csv(CSV_DIR / "authors.csv").rename(columns={"id": "author_id", "Author": "Name"})
    authors["Name"] = authors["Name"].fillna("")

    book_authors = pd.read_csv(CSV_DIR / "book_authors.csv").rename(columns={"ISBN13": "isbn", "Author": "author_id"})

    b = pd.read_csv(CSV_DIR / "borrowers.csv")
    borrowers = pd.DataFrame({
        "card_id": b["ID0000id"],
        "ssn": b["ssn"].str.replace("-", ""),
        "Bname": b["first_name"] + "_" + b["last_name"],
        "address": b["address"] + ", " + b["city"] + ", " + b["state"],
        "phone": b["phone"],
    })

    with engine.begin() as conn:
        for df, table in [(books, "books"), (authors, "authors"),(book_authors, "book_authors"), (borrowers, "borrowers")]:
            df.to_sql(table, conn, if_exists="append", index=False)

    print(f"imported into {engine.url.database}")
