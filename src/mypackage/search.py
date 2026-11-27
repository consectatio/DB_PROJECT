from database.crud import search_books


def search(session, text):
        return [
        (book.isbn, book.title, ", ".join(sorted(author.Name for author in book.authors)),
         "OUT" if checked_out else "IN")
        for book, checked_out in search_books(session, text)
    ]