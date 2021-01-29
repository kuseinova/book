from django.urls import path

from category import views

urlpatterns = [
    path('', views.CategoryApiView.as_view()),
]
