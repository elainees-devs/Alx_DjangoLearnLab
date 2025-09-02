from bookshelf.models import Author, Book, Library, Librarian

#Query all books by a specific author
def get_books_by_author(author_name):
    author=Author.objects.get(name=author_name)
    return author.books.all()

#Retrieve the librarian for a library
def librarian_for_library(library_name):
    library=Library.objects.get(namme=library_name)
    return library.librarian