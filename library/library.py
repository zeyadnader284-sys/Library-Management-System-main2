from .exceptions import (
    BookNotAvailableError,
    BookNotFoundError,
    DuplicateEntryError,
    MemberNotFoundError,
)


class Library:
    def remove_member(self, member_id):
        member = self.find_member(member_id)
        if member.borrowed_isbns:
            raise ValueError("Member still has borrowed books.")
        self.members.remove(member)

    def list_borrowed_books(self, member_id):
     member = self.find_member(member_id)
     return [self.find_book(isbn) for isbn in member.borrowed_isbns]

    def available_books(self):
     return [book for book in self.books if not book.is_borrowed]



    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        if any(existing.isbn == book.isbn for existing in self.books):
            raise DuplicateEntryError(
                f"A book with ISBN {book.isbn} already exists."
            )
        self.books.append(book)

    def remove_book(self, isbn):
        book = self.find_book(isbn)
        self.books.remove(book)

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        raise BookNotFoundError(f"No book found with ISBN {isbn}.")

    def add_member(self, member):
        if any(
            existing.member_id == member.member_id
            for existing in self.members
        ):
            raise DuplicateEntryError(
                f"A member with ID {member.member_id} already exists."
            )
        self.members.append(member)

    def find_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        raise MemberNotFoundError(
            f"No member found with ID {member_id}."
        )

    def search_books(self, keyword):
        keyword = keyword.lower()
        return [
            book
            for book in self.books
            if keyword in book.title.lower()
            or keyword in book.author.lower()
        ]

    def list_books(self):
        return sorted(self.books, key=lambda book: book.title)

    def borrow_book(self, member_id, isbn):
        member = self.find_member(member_id)
        book = self.find_book(isbn)

        if book.is_borrowed:
            raise BookNotAvailableError(
                f'"{book.title}" is already borrowed.'
            )

        book.is_borrowed = True
        member.borrowed_isbns.append(isbn)

    def return_book(self, member_id, isbn):
        member = self.find_member(member_id)
        book = self.find_book(isbn)

        if isbn not in member.borrowed_isbns:
            raise BookNotAvailableError(
                f'{member.name} did not borrow "{book.title}".'
            )

        book.is_borrowed = False
        member.borrowed_isbns.remove(isbn)
