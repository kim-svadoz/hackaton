from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('profile_update/', views.profile_update, name="profile_update"),
    path('logout/', views.logout, name="logout"),
    path('delete/', views.delete, name="delete"),
    path('update/', views.update, name="update"),
    path('password/', views.password, name="password"),
    
    path('<str:username>/', views.profile, name="profile"),
]
