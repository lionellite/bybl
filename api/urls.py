from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('books/<int:book_id>/chapters/', views.ChapterList.as_view(), name='chapter-list'),
    path('chapters/<int:pk>/', views.ChapterDetail.as_view(), name='chapter-detail'),
    path('chapters/<int:chapter_id>/verses/', views.VerseList.as_view(), name='verse-list'),
    path('verses/<int:pk>/', views.VerseDetail.as_view(), name='verse-detail'),
]
