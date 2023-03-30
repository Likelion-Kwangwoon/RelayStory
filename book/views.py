from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from relaystory.settings import SECRET_KEY
import jwt
from django.shortcuts import render, get_object_or_404
from user.serializers import UserSerializer
from .models import Book,Comment
from user.models import *

@api_view(['GET'])
def allBooks(request):
    try:
        responseData = []
        books=Book.object.all()
        for b in books:
            comments = Comment.object.filter(book=b)
            book={"book":BookSerializer(b,many=False).data,"comments":CommentSerializer(comments,many=True).data}
            responseData.append(book)

        return Response(responseData, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getBook(request):
    try:
        # access token을 decode 해서 유저 id 추출 => 유저 식별
        access = request.META['HTTP_AUTHORIZATION'][7:]  # Bearer 뺀게 7부터
        print(access)
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])

        email = payload.get('email')
        print(email)
        user = get_object_or_404(User, email=email)
        serializer = UserSerializer(instance=user)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)
    books=Book.object.filter(user=user)
    responseData=[]
    for b in books:
        comments = Comment.object.filter(book=b)
        book={"book":BookSerializer(b,many=False).data,"comments":CommentSerializer(comments,many=True).data}
        responseData.append(book)

    return Response(responseData, status=status.HTTP_200_OK)

@api_view(['GET'])
def getBookById(request):
    bookId=request.GET["bookId"]
    book=Book.object.get(pk=bookId)
    comments = Comment.object.filter(book=book)
    responseData = {"book": BookSerializer(book, many=False).data, "comments": CommentSerializer(comments, many=True).data}
    return Response(responseData, status=status.HTTP_200_OK)
@api_view(['POST'])
def postBook(request):
    try:
        # access token을 decode 해서 유저 id 추출 => 유저 식별
        access = request.META['HTTP_AUTHORIZATION'][7:]  # Bearer 뺀게 7부터
        print(access)
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])

        email = payload.get('email')
        print(email)
        user = get_object_or_404(User, email=email)
        print(user.nickname)
        serializer = UserSerializer(instance=user)
        print(request.data["title"])
        print(request.data["cover"])
        print(request.data["content"])


        data = {
            "user":user.pk,
            "title": request.data["title"],
            "cover": request.data["cover"]
        }
        bookSerializer = BookSerializer(data=data)

        if bookSerializer.is_valid(raise_exception=True):
            book=bookSerializer.save()

            data={
                "book":book.pk,
                "nickname":user.nickname,
                "content":request.data["content"]
            }
            commentSerializer=CommentSerializer(data=data)
            if commentSerializer.is_valid(raise_exception=True):
                commentSerializer.save()
                return Response(book.pk, status=status.HTTP_201_CREATED)


    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

    return Response("error",status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def postComment(request):
    try:
        data = {
            "book": request.data["bookId"],
            "nickname": request.data["nickname"],
            "content": request.data["content"]
        }
        commentSerializer = CommentSerializer(data=data)
        if commentSerializer.is_valid(raise_exception=True):
            commentSerializer.save()
    except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
    return Response(request.data["bookId"],status=status.HTTP_201_CREATED)
