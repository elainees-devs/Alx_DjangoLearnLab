
---

### 📄 **retrieve.md**
```markdown
# Retrieve Operation
## Command

```python
from bookshelf.models import Book

# Retrieve the book created earlier
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

```
## Django Shell Transcript

>>> from bookshelf.models import Book
>>> 
>>> # Retrieve the book created earlier
>>> book = Book.objects.get(title="1984")
>>> print(book.title, book.author, book.publication_year)
1984 George Orwell 1949
>>> 
