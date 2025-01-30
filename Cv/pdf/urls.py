from django.urls import path
from django.contrib.auth.views import LogoutView
from pdf.views import download, formulaire, generer, index, verification, statistics, register, user_login, user_logout



urlpatterns = [
    path('', index, name="acceuil"),
    path('creercv', formulaire, name="formulaire"),
    path('verification', verification, name="verification"),
    path('verification/<int:id>', verification, name="verification_with_id"),
    path('<int:id>', generer, name="generer"),
    path('download', download, name="download"),
    path('statistics/', statistics, name='statistics'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
