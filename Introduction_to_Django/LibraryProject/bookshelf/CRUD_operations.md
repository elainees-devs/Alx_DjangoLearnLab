
# CRUD Operations in Django Shell

This document records all four CRUD operations performed in the Django shell.

---

## 1. Create

```python
from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
````

**Output:**

```
1984 by George Orwell (1949)
```

---

## 2. Retrieve

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
```

**Output:**

```
1984 George Orwell 1949
```

---

## 3. Update

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

print(book)
```

**Output:**

```
Nineteen Eighty-Four by George Orwell (1949)
```

---

## 4. Delete

```python
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

print(Book.objects.all())
```

**Output:**

```
<QuerySet []>
```

