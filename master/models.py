from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from books.models import books


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
      db_table = "users"
    def __str__(self):
        return str(self.id)

class Userbooks(models.Model):
    id=models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, models.SET_NULL, db_column="user_id", blank=True, null=True,related_name='Userbooks_user_id')
    date = models.DateField(auto_now_add=True)
    book_id = models.ForeignKey(books,models.SET_NULL, db_column="book_id", blank=True, null=True,related_name='Userbooks_book_id')
    class Meta:
      db_table = "Userbooks"
    def __str__(self):
        return str(self.id)