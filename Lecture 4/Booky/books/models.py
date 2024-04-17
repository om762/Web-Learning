from django.db import models

class Book(models.Model):
    isbn = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=80)
    publication_year = models.IntegerField()
    publisher = models.CharField(max_length=50)
    image = models.URLField()

    def __str__(self):
        return self.title

class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)

    def __str__(self) -> str:
        return f"{str(self.first_name).capitalize()}"

class BookReader(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reading_book")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="reading_by")
    stared_reading  = models.DateField()
