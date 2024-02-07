from os import name
from django.urls import path

from . import views

urlpatterns = [
    path('composite/', views.index_view, name='index'),
    path('composite/search/', views.SearchItemView.as_view(), name='search-item'),
    path('composite/detail/<int:pk>/', views.DetailCompView.as_view(), name='detail-composite'),
    path('composite/create/item/', views.CreateItemView.as_view(), name='create-item'),
    path('composite/create/composite/', views.CreateCompView.as_view(), name='create-composite'),
    path('composite/delete/item/<int:pk>/', views.DeleteItemView.as_view(), name='delete-item'),
    path('composite/list/composite/', views.ListCompView.as_view(), name='list-composite'),
    path('composite/delete/composite/<int:pk>/', views.DeleteCompView.as_view(), name='delete-composite'),
    path('composite/update/item/<int:pk>/', views.UpdateItemView.as_view(), name='update-item'),
    path('composite/update/composite/<int:pk>/', views.UpdateCompView.as_view(), name='update-composite'),
    path('composite/composite/', views.CompCompFormView.as_view(), name='composite-composite'),
    path('composite/composite/delete/<int:pk>/', views.CompCompDelete, name='delete-compcomp'),
]