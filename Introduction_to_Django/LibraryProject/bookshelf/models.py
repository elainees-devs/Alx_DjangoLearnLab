from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, name='books')
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
    
class Librar(models.Model):
    name = models.CharField(max_length=100)
    books=models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name

