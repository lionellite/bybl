from django.urls import path
from bible import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:book_id>/", views.read, name="read"),
    path("<int:book_id>/<int:chapter>/", views.read, name="read_chap"),
    path("search/", views.search, name="search"),
]