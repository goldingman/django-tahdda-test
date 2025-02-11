from django.urls import path, include
from bookapp.views import (
    MyObtainTokenPairView, 
    RegisterView, 
    action_book, 
    add_or_get_book,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login', MyObtainTokenPairView.as_view(), name='auth_login'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('books', add_or_get_book, name='add_or_get_book'),
    path('books/<int:id>', action_book, name='action_book'),
]