# Generated by Django 2.2.17 on 2021-01-04 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('master', '0002_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userbooks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('book_id', models.ForeignKey(blank=True, db_column='book_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Userbooks_book_id', to='books.books')),
                ('user_id', models.ForeignKey(blank=True, db_column='user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Userbooks_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Userbooks',
            },
        ),
    ]
