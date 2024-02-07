from django.urls import path

from . import views


urlpatterns = [
    path('', views.index_view,name='index'),
    path('dictionary/', views.ListDicView.as_view(), name='list-dictionary'),
    path('dictionary/create/', views.CreateDicView.as_view(), name='create-dictionary'),
    path('dictionary/search/', views.SearchDicView.as_view(), name='search-dictionary'),
    path('dictionary/category/<str:category>/', views.CategoryDicView.as_view(), name='category-dictionary'),
    path('dictionary/detail/<str:title>/', views.DetailDicView.as_view(), name='detail-dictionary'),
    path('dictionary/<pk>/delete/', views.DeleteDicView.as_view(), name='delete-dictionary'),
    path('dictionary/<str:title>/update/', views.UpdateDicView.as_view(), name='update-dictionary'),
]