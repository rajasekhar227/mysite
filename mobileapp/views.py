import json

from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from books.models import books
from master.models import User, Userbooks
from rest_framework.decorators import authentication_classes

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        result = {}
        role = 0
        referred_by = ''
        returndata = {}
        if request.data.get('name') == '' or request.data.get('name') is None:
            returndata = {'Result': result, 'MessageType': 0, 'Message': "Name is Required"}
        if request.data.get('email') == '' or request.data.get('email') is None:
            returndata = {'Result': result, 'MessageType': 0, 'Message': "Email is Required"}
        if request.data.get('password') == '' or request.data.get('password') is None:
            returndata = {'Result': result, 'MessageType': 0, 'Message': "Password is Required"}
        if request.data.get('email') != '' and request.data.get('email') is not None:
            check = User.objects.filter(email=request.data.get('email')).exists()
            if check == True:
                returndata = {'Result': result, 'MessageType': 0, 'Message': "Email Alredy Exists"}
        if returndata:
            return JsonResponse(returndata)
        try:
            password = request.data.get('password')
            object = {
                'name': request.data.get('name'),
                'email': request.data.get('email'),
                'is_superuser': False,
                'is_active': True,
                'is_staff': False,
            }
            user = User.objects.create(**object)
            user.set_password(password)
            user.save()
            result['status'] = 200
            returndata = {'result': result, 'MessageType': 1, 'Message': "Registered Successfully"}
            return JsonResponse(returndata)
        except Exception as e:
                returndata = {'result': result, 'MessageType': 0, 'Message': "Something Went Wrong Please Try Again"}
                return JsonResponse(returndata)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        returndata = {}
        result = {}
        if request.data.get('email') == '' or request.data.get("email", None) is None:
            returndata = {'Result': result, 'MessageType': 0, 'Message': "Email Id is Required"}
        if request.data.get('password') == '' or request.data.get('password', None) is None:
            returndata = {'Result': result, 'MessageType': 0, 'Message': "Password is Required"}
        if returndata:
            return JsonResponse(returndata)
        email = request.data.get('email')
        password = request.data.get('password')
        usercheck = User.objects.filter(email=email).exists()
        if usercheck == True:
            userdata = User.objects.filter(email=email).get()
            valid = userdata.check_password(password)
            if valid:
                login(request, userdata)
                token, _ = Token.objects.get_or_create(user=userdata)
                result['user_id'] = userdata.id
                result['token'] = token.key
                returndata = {'result': result, 'MessageType': 1, 'Message': "Login Successfully"}
                return JsonResponse(returndata)
            else:
                returndata = {'result': result, 'MessageType': 0,'Message': "Data Not Found"}
                return JsonResponse(returndata)
        else:
            returndata = {'result': result, 'MessageType': 0,'Message': "Data Not Found"}
            return JsonResponse(returndata)


class barrrowView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        tokenheader = request.headers.get('Authorization')
        split = tokenheader.split(' ')
        token = split[1]
        user = Token.objects.get(key=token).user
        returndata = {}
        result = {}
        if request.data.get('book_id') == '' or request.data.get("book_id", None) is None:
            returndata = {'Result': result, 'MessageType': 0, 'Message': "Book Id is Required"}
        if request.data.get('Date') == '' or request.data.get('Date', None) is None:
            returndata = {'Result': result, 'MessageType': 0, 'Message': "Date is Required"}
        if returndata:
            return JsonResponse(returndata)
        book_id = request.data.get('book_id')
        Date = request.data.get('Date')
        print(Date)
        object = {
            'user_id':user,
            'book_id':books.objects.get(book_id=book_id),
            'date':Date
        }
        Userbooks.objects.create(**object)
        book = books.objects.get(book_id=book_id)
        bookcount = book.Book_count - 1
        book.Book_count = bookcount
        book.save()
        returndata = {'result': result, 'MessageType': 1, 'Message': "Book barrowed Successfully"}
        return JsonResponse(returndata)

class bokkslistView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        userlist =[]
        tokenheader = request.headers.get('Authorization')
        split = tokenheader.split(' ')
        token = split[1]
        user = Token.objects.get(key=token).user
        userbokks = Userbooks.objects.filter(user_id=user).all()
        for book in userbokks:
            data={
                'name':book.user_id.name,
                'book_name':book.book_id.book_name
            }
            userlist.append(data.copy())
        returndata = {'result': userlist, 'MessageType': 1}
        return JsonResponse(returndata)

