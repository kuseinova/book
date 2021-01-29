from django.contrib import admin

from books.models import Book, Favorites, Ratings, Comment

admin.site.register(Book)
admin.site.register(Favorites)
admin.site.register(Ratings)
admin.site.register(Comment)