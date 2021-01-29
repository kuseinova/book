from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListApiView.as_view()),
    path('favorites/', views.FavoritesListApiView.as_view()),
    path('activate_book/<int:id>/', views.ActivationView.as_view(),
         name='activate_book'),
    path('rating/', views.RatingCreate.as_view()),
    path('<int:pk>/', views.BookDetailApiView.as_view()),
    path('<int:pk>/add/', views.FavoriteAdd.as_view()),
    path('<int:pk>/favorite_delete/', views.FavoriteDelete.as_view()),

]
