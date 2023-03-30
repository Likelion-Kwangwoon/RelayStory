from django.urls import path,include
from .views import getBook,postBook,allBooks,postComment,getBookById


urlpatterns = [
    path("write/",postBook),
    path("view/", getBook),
    path("all/", allBooks),
    path("comment/",postComment),
    path("getbook/",getBookById)
]
