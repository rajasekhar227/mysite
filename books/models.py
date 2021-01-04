from django.db import models

# Create your models here.

class books(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100,unique=True)
    author = models.CharField(max_length=100)
    Book_count = models.IntegerField(default=0)
    class Meta:
      db_table = "books"
    def __str__(self):
        return str(self.book_id)

