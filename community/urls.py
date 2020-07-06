from django.urls import path
from . import views
app_name = "community"
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:community_pk>/update/', views.update, name="update"),
    path('<int:community_pk>/detail', views.detail, name="detail"),
    path('<int:community_pk>/delete/', views.delete, name="delete"),
    path('<int:community_pk>/comment_create/',views.comment_create, name="comment_create"),
    path('<int:community_pk>/comment_delete/<int:comment_pk>/',views.comment_delete, name="comment_delete"),
    path('<int:community_pk>/like/', views.like, name="like"),
    path('<int:community_pk>/recommend/', views.recommend, name="recommend"),
    path('search/', views.border_search, name='search'),

    path('all_paging/',views.all_paging, name='all_paging'),
    path('popular_paging/',views.popular_paging, name='popular_paging'),
    path('all_search/', views.all_search, name='all_search'),
    path('popular_search/', views.popular_search, name='popular_search'),
    path('<int:community_pk>/comment_select/<int:comment_pk>',views.comment_select, name="comment_select"),
]
