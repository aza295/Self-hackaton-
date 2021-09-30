
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from music.views import UpdateCommentView, DeleteCommentView, CreateCommentView, FavoriteListView, CreateReviewView, \
    RetrieveUpdateDestroyReviewView

urlpatterns = [
    path('comments/', CreateCommentView.as_view()),
    path('comments/update/<int:pk>/', UpdateCommentView.as_view()),
    path('comments/delete/<int:pk>/', DeleteCommentView.as_view()),
    path('favorites/', FavoriteListView.as_view()),
    path('review/', CreateReviewView.as_view()),
    path('review/<int:pk>/', RetrieveUpdateDestroyReviewView.as_view()),
    path('review/create/', RetrieveUpdateDestroyReviewView.as_view()),
    path('review/update/<int:pk>/', RetrieveUpdateDestroyReviewView.as_view()),
    path('review/delete/<int:pk>/', RetrieveUpdateDestroyReviewView.as_view()),

]