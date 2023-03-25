from django.urls import path,include
from .views import getBook,postBook,allBooks


urlpatterns = [
    path("write/",postBook),
    path("view/", getBook),
    path("all/", allBooks)

]
