# api/models.py
from django.db import models

class Author(models.Model):
    """Author model representing a writer who can have many books."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Book model linked to an Author (One-to-Many)."""
    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

