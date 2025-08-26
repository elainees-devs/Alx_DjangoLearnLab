
---

### 📄 **update.md**
```markdown
# Update Operation
## Command

```python
from bookshelf.models import Book

# Retrieve and update the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

print(book)

```
## Django Shell Transcript
>>> from bookshelf.models import Book
>>> 
>>> # Retrieve and update the book
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> 
>>> print(book)
Nineteen Eighty-Four by George Orwell (1949)
>>> 


