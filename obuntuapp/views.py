# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import EmailMessage, send_mail
from django.core import serializers
from .models import Account, Lga, SenatorialZone, AdminUser, SuperUserAdmin
from .serializers import AccountSerializer, NewAccountSerializer, LgaSerializer, ErrorCheckSerializer, SuccessCodeSerializer, AdminSerializer, UserSerializer, LocationSerializer






def authenticateLogin(request, username, password):

    success = False

    try: 
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            success = True
    except: 
        pass

    return success














def getAccount(request):

    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        phone = user.username

        account = Account.objects.get(phone=phone)
        return account

    else:
        
        return -1





class Login(APIView):

    def get(self,request):
        
        account = Account.objects.all()
        serializer = AccountSerializer(account, many=True)

        return Response(serializer.data)



    def post(self,request):

        serializer = NewAccountSerializer(data=request.data)
        if serializer.is_valid():

            name = serializer.data['name']
            phone = serializer.data['phone']
            password = serializer.data['password']

            try:

                User.objects.get(username = phone)
                Account.objects.get(phone = phone)
                
                status = authenticateLogin(request, phone, password)
                
                if status : 
                    code = phone
                    success = {
                        'code' : code
                    }

                    serializer = SuccessCodeSerializer(success, many = False)
                    return Response(serializer.data)

                else:

                    error_message = 'Oops login details do not match'
                    err = {
                        'error_message' : error_message
                    }

                    serializer = ErrorCheckSerializer( err, many=False)
                    return Response(serializer.data)

            except:
                
                if str(name) == 'admin':
                    error_message = 'Login details does not match a registered admin'
                    err = {
                        'error_message' : error_message
                    }
                    serializer = ErrorCheckSerializer( err, many=False)

                    return Response(serializer.data)


            
            raw_password = password
            password = make_password(password)
            

            user = User()
            user.username = phone
            user.password = password
            user.name = name
            user.save()

            account = Account()
            account.name = name
            account.phone = phone
            account.password = password
            account.save()

            code = phone

            success = {
                'code' : code
            }

            serializer = SuccessCodeSerializer(success , many = False)

            return Response(serializer.data)
           
        
        else:
            pass
    
        error_message = 'Sorry could not complete process, reload page and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)




class LgaView(APIView):

    def get(self, request):

        lgas = Lga.objects.all()
        serializer = LgaSerializer(lgas, many=True)

        return Response(serializer.data)

    def post(self, request):
        pass




class AdminView(APIView):

    def get(self, request):

        adminList = Account.objects.filter(isAdmin=True)

        bucket = []
        for admin in adminList:

            name = admin.name
            phone = admin.phone
            isSuperUser = admin.isSuperUser

            lga = Lga.objects.get(id = admin.lga_id)
            lga_name = lga.name

            signedUsers = AdminUser.objects.filter(admin=admin.id).count()

            buffer = {
                'name': name,
                'phone': phone,
                'isSuperUser': isSuperUser,
                'lga': lga_name,
                'signedUsers': signedUsers
            }

            bucket.append(buffer)

        serializer = AdminSerializer(bucket, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        account = getAccount(request)

        try:
            isSuperUser = Account.objects.get(id=account.id, isSuperUser=True)
            phone = request.POST.get("phone","")

            try:
                accountExist = Account.objects.get(phone=phone)

                error_message = 'Account with this phone id already exist'
                err = {
                    'error_message' : error_message
                }
                serializer = ErrorCheckSerializer( err, many=False)
                return Response(serializer.data)
            except:
                pass

            name = request.POST.get("name","")
            password = request.POST.get("password","")
            lga = request.POST.get("lga","")

            lgaObject = Lga.objects.get(id = lga)

            raw_password = password
            password = make_password(password)
            
            user = User()
            user.username = phone
            user.password = password
            user.name = name
            user.save()

            admin = Account()
            admin.name = name
            admin.phone = phone
            admin.password = password
            admin.lga = lgaObject
            admin.isAdmin = True
            admin.save()

            superUserAdmin = SuperUserAdmin()
            superUserAdmin.admin = admin.id
            superUserAdmin.superUser = account
            superUserAdmin.save()

            adminList = Account.objects.filter(isAdmin=True)
            bucket = []
            for admin in adminList:

                name = admin.name
                phone = admin.phone
                isSuperUser = admin.isSuperUser

                lga = Lga.objects.get(id = admin.lga_id)
                lga_name = lga.name

                signedUsers = AdminUser.objects.filter(admin=admin.id).count()

                buffer = {
                    'name': name,
                    'phone': phone,
                    'isSuperUser': isSuperUser,
                    'lga': lga_name,
                    'signedUsers': signedUsers
                }

                bucket.append(buffer)

            serializer = AdminSerializer(bucket, many=True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'You are not authorised to carry out this task'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)










class UserView(APIView):

    def get(self, request):

        userList = Account.objects.all()

        bucket = []
        for admin in userList:

            name = admin.name
            phone = admin.phone

            lga = Lga.objects.get(id = admin.lga_id)
            lga_name = lga.name

            buffer = {
                'name': name,
                'phone': phone,
                'lga': lga_name,
            }

            bucket.append(buffer)

        serializer = UserSerializer(bucket, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        account = getAccount(request)

        try:
            isAdmin = Account.objects.get(id=account.id, isAdmin=True)
            phone = request.POST.get("phone","")

            try:
                accountExist = Account.objects.get(phone=phone)

                error_message = 'Account with this phone id already exist'
                err = {
                    'error_message' : error_message
                }
                serializer = ErrorCheckSerializer( err, many=False)
                return Response(serializer.data)
            except:
                pass

            name = request.POST.get("name","")
            password = request.POST.get("password","")
            lga = request.POST.get("lga","")

            lgaObject = Lga.objects.get(id = lga)

            raw_password = password
            password = make_password(password)
            
            user = User()
            user.username = phone
            user.password = password
            user.name = name
            user.save()

            user = Account()
            user.name = name
            user.phone = phone
            user.password = password
            user.lga = lgaObject
            user.save()

            adminUser = AdminUser()
            adminUser.user = user.id
            adminUser.admin = account
            adminUser.save()

            userList = Account.objects.all()
            bucket = []
            for admin in userList:

                name = admin.name
                phone = admin.phone

                lga = Lga.objects.get(id = admin.lga_id)
                lga_name = lga.name

                buffer = {
                    'name': name,
                    'phone': phone,
                    'lga': lga_name,
                }

                bucket.append(buffer)

            serializer = UserSerializer(bucket, many=True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'You are not authorised to carry out this task'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)







class LocationView(APIView):

    def get(self, request):

        lgaList = Lga.objects.all()

        bucket = []
        for lga in lgaList:

            locationUsers = Account.objects.filter(lga = lga).count()
            lga_name = lga.name

            buffer = {
                'name': lga_name,
                'users': locationUsers,
            }

            bucket.append(buffer)

        serializer = LocationSerializer(bucket, many=True)
        return Response(serializer.data)