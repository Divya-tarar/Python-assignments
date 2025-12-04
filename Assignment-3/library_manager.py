import json
import os


# Book Class

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status  # "available" or "issued"

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["author"],
            data["isbn"],
            data.get("status", "available")
        )



# Library Inventory Class

class LibraryInventory:
    def __init__(self, filename="catalog.json"):
        self.filename = filename
        self.books = []
        self.load_from_json()

    def load_from_json(self):
        if not os.path.exists(self.filename):
            self.books = []
            return

        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.books = [Book.from_dict(x) for x in data]
        except:
            print("Error reading catalog file. Starting with empty catalog.")
            self.books = []

    def save_to_json(self):
        data = [book.to_dict() for book in self.books]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

    def add_book(self, book):
        # prevent duplicate ISBN
        for b in self.books:
            if b.isbn == book.isbn:
                print("Book with this ISBN already exists.")
                return
        self.books.append(book)
        print("Book added successfully.")

    def find_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def search_by_title(self, keyword):
        keyword = keyword.lower()
        return [b for b in self.books if keyword in b.title.lower()]

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
            return
        print("\n--- Library Catalog ---")
        for b in self.books:
            print(f"{b.title} | {b.author} | ISBN: {b.isbn} | Status: {b.status}")
        print("-------------------------")


# Menu / CLI

def main():
    inventory = LibraryInventory()

    while True:
        print("\n=== Library Inventory Manager ===")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Save & Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            isbn = input("Enter ISBN: ")
            inventory.add_book(Book(title, author, isbn))

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            book = inventory.find_by_isbn(isbn)
            if book:
                if book.issue():
                    print("Book issued successfully.")
                else:
                    print("Book already issued.")
            else:
                print("Book not found.")

        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = inventory.find_by_isbn(isbn)
            if book:
                if book.return_book():
                    print("Book returned successfully.")
                else:
                    print("Book was not issued.")
            else:
                print("Book not found.")

        elif choice == "4":
            inventory.display_all()

        elif choice == "5":
            keyword = input("Enter title keyword: ")
            results = inventory.search_by_title(keyword)
            if results:
                for b in results:
                    print(f"{b.title} | {b.author} | ISBN: {b.isbn} | Status: {b.status}")
            else:
                print("No matching books found.")

        elif choice == "6":
            inventory.save_to_json()
            print("Catalog saved. Exiting...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
