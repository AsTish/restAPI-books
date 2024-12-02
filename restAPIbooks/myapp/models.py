import uuid
from django.db import models

class Author(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    name = models.CharField(
        max_length=255, 
        blank=False, 
        null=False, 
        verbose_name="Name", 
        help_text="Enter the full name of the author."
    )
    birth_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Birth Date", 
        help_text="Enter the author's date of birth (format: YYYY-MM-DD)."
    )
    nationality = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Nationality", 
        help_text="Enter the nationality of the author."
    )

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Title",
        help_text="Enter the title of the book."
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name="Author",
        help_text="Select the author of the book."
    )
    publication_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Publication Date",
        help_text="Enter the publication date of the book (format: YYYY-MM-DD)."
    )
    genre = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Genre",
        help_text="Enter the genre of the book (e.g., Historical Fiction)."
    )

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["-publication_date", "title"]

    def __str__(self):
        return self.title
