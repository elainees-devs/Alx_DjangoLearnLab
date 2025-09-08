
---

### 📄 **delete.md**
```markdown
# Delete Operation
## Command
```python
from bookshelf.models import Book

# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
print(Book.objects.all())

```

## Django Shell Transcript
>>> from bookshelf.models import Book
>>> 
>>> # Retrieve and delete the book
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> 
>>> # Confirm deletion
>>> print(Book.objects.all())
<QuerySet []>
>>> 

