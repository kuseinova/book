from django.urls import path
from . import views
from .views import CommentCreate

urlpatterns = [
    path('', views.BookListApiView.as_view()),
    path('favorites/', views.FavoritesListApiView.as_view()),
    path('activate/<int:id>/', views.ActivationView.as_view(),
         name='activate'),
    path('rating/', views.RatingCreate.as_view()),
    path('<int:pk>/', views.BookDetailApiView.as_view()),
    path('<int:pk>/add/', views.FavoriteAdd.as_view()),
    path('<int:pk>/favorite_delete/', views.FavoriteDelete.as_view()),
    path('comments/create/', CommentCreate.as_view()),
]
