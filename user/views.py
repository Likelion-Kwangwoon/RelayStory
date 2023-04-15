from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import jwt
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

from relaystory.settings import SECRET_KEY
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
import requests

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def refreshToken(request):
    try:
        # access token을 decode 해서 유저 id 추출 => 유저 식별
        access = request.META['HTTP_AUTHORIZATION'][7:]  # Bearer 뺀게 7부터
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])

        email = payload.get('email')
        print(email)
        user = get_object_or_404(User, email=email)
        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)
        res = Response(
            {
                "access": access_token
            },
            status=status.HTTP_200_OK,
        )
        return res
    except Exception as e:
        print(e)
        return Response(e, status=status.HTTP_400_BAD_REQUEST)
class AuthAPIView(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.META['HTTP_AUTHORIZATION'][7:] #Bearer 뺀게 7부터
            print(access)
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])

            email = payload.get('email')
            print(email)
            user = get_object_or_404(User, email=email)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
        # 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response

@api_view(['GET'])
def hello(request):
    return Response("HelloWolrd")

@api_view(['GET'])
def signin(request):
    print(request.GET["code"])
    url1='https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id=5e90fdaec3d61d8cc6ec0616fa4d8ff2&client_secret=Bmp1KrvsloFcwxSj0G5F8Kd8guPU3Fn7&redirect_uri=http://localhost:3000/oauth&code='+request.GET["code"]
    headers= {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    res = requests.get(url1, headers=headers)
    print(res.json())
    url2='https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization':'Bearer '+res.json()['access_token']}
    res = requests.get(url2, headers=headers)
    print(res.json())

    data={
        "nickname":res.json()['properties']['nickname'],
        "email":res.json()['kakao_account']['email']
    }
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        print("isvalid")
        user = serializer.save()
        print(user.nickname)
        print(user.email)

        res=retToken(user)
        print(res)
        return Response(str(res), status=status.HTTP_200_OK)
    else:

        try:
            user=User.objects.get(email=res.json()['kakao_account']['email'])
            print(user.nickname)
            print(user.email)
            res = retToken(user)
            print(res)
            return Response(str(res), status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def retToken(user):
    try:
        print("1")
        token = TokenObtainPairSerializer.get_token(user)
        print("1")
        refresh_token = str(token)
        print("1")
        access_token = str(token.access_token)
        print("1")
        res ={
                "user": {
                    "email":user.email,
                    "nickname":user.nickname
                },
                "message": "register successs",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            }

        print("1")
        # jwt 토큰 => 쿠키에 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)

        return res
    except Exception as e:
        print("generate token error")
        print(e)
        return "token"