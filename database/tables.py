from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Optional

from sqlalchemy import (
    create_engine,
    event,
    select,
    Integer,
    Numeric,
    String,
    Date,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import (
    mapped_column,
    sessionmaker,
    DeclarativeBase,
    Mapped,
    relationship,
    Session,
)

# probably should move to .env but I cba getting people to set up that
SQLite_connection_string = f"sqlite:///{Path(__file__).resolve().parent / 'database.db'}"  # always database/database.db
engine = create_engine(SQLite_connection_string)
SessionLocal = sessionmaker(bind=engine)

LOAN_DAYS = 14                      # just set that due date to be 2 weeks wasn't specified in the pdf
FINE_PER_DAY = Decimal("0.25")      # $0.25 / day - specified in the milestone 2 pdf

# call at startup
def init_db() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        refresh_fines(session)


# SQLite ignores FOREIGN KEY constraints unless this is switched on per connection.
@event.listens_for(engine, "connect")
def _enable_sqlite_fks(dbapi_connection, _):
    dbapi_connection.execute("PRAGMA foreign_keys=ON")


class Base(DeclarativeBase): pass


class Book(Base):
    __tablename__ = 'books'
    isbn: Mapped[str] = mapped_column(String(13), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    authors: Mapped[list["Authors"]] = relationship(secondary="book_authors", back_populates="books")
    loans: Mapped[list["Book_loans"]] = relationship(back_populates="book")


class Authors(Base):
    __tablename__ = 'authors'
    author_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Name: Mapped[str] = mapped_column(String(100), nullable=False)
    books: Mapped[list["Book"]] = relationship(secondary="book_authors", back_populates="authors")


class Book_authors(Base):
    __tablename__ = 'book_authors'
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id"), primary_key=True)
    isbn: Mapped[str] = mapped_column(ForeignKey("books.isbn"), primary_key=True, index=True)


class Borrower(Base):
    __tablename__ = 'borrowers'
    card_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    ssn: Mapped[str] = mapped_column(String(9), unique=True, nullable=False)

    # im just going to combine `fname_lname` and we will have to manually separate it each time it's used.
    # Borrower name I guess just has to equal both of them for some reason :D.
    Bname: Mapped[str] = mapped_column(String(60), nullable=False)

    address: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(16))
    loans: Mapped[list["Book_loans"]] = relationship(back_populates="borrower")


class Book_loans(Base):
    __tablename__ = 'book_loans'
    loan_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(ForeignKey("books.isbn"), nullable=False)
    card_id: Mapped[str] = mapped_column(ForeignKey("borrowers.card_id"), nullable=False)
    date_out: Mapped[date] = mapped_column(Date, default=date.today)
    due_date: Mapped[date] = mapped_column(Date, default=lambda: date.today() + timedelta(days=LOAN_DAYS))
    date_in: Mapped[Optional[date]] = mapped_column(Date, nullable=True)  # NULL = still out
    book: Mapped["Book"] = relationship(back_populates="loans")
    borrower: Mapped["Borrower"] = relationship(back_populates="loans")
    fine: Mapped[Optional["Fines"]] = relationship(back_populates="loan", uselist=False)


class Fines(Base):
    __tablename__ = 'fines'
    loan_id: Mapped[int] = mapped_column(ForeignKey("book_loans.loan_id"), primary_key=True)
    Fine_amt: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    paid: Mapped[bool] = mapped_column(Boolean, default=False)
    loan: Mapped["Book_loans"] = relationship(back_populates="fine")


def calc_fine(loan: Book_loans, today: Optional[date] = None) -> Decimal:
    end_date = loan.date_in or today or date.today()
    days_late = (end_date - loan.due_date).days
    if days_late <= 0:
        return Decimal("0.00")
    return (days_late * FINE_PER_DAY).quantize(Decimal("0.01"))


def refresh_fines(session: Session, today: Optional[date] = None) -> int:
    """Create/update FINES rows for every late loan (meant to be run daily).

    - no row yet            -> insert one
    - row exists, unpaid    -> update Fine_amt only if it changed
    - row exists, paid      -> leave alone
    Returns the number of rows inserted or changed.
    """
    today = today or date.today()
    changed = 0

    for loan in session.scalars(select(Book_loans)):
        amount = calc_fine(loan, today)
        if amount == 0:
            continue

        if loan.fine is None:
            session.add(Fines(loan_id=loan.loan_id, Fine_amt=amount, paid=False))
            changed += 1
        elif not loan.fine.paid and loan.fine.Fine_amt != amount:
            loan.fine.Fine_amt = amount
            changed += 1

    session.commit()
    return changed
