from django.urls import path, include

from .views import RegisterView, LoginView, LogoutView, \
    ActivationView, ProfileViewSet

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/<int:pk>/', ProfileViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'put': 'update'
    }))
]
