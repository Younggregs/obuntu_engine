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
from django.db.models import Q
from .models import Account, Lga, SenatorialZone, AdminUser, SuperUserAdmin, PollingUnit, Ward
from .serializers import AccountSerializer, NewAccountSerializer, LgaSerializer, ErrorCheckSerializer, SuccessCodeSerializer, AdminSerializer, UserSerializer, LocationSerializer, WardSerializer, PollingUnitSerializer, LoginSerializer, UserDataSerializer

import pandas as pd
import os
import os.path  
import sys
import csv
import random


#Static root
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))


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









class RecordPollingUnits(APIView):

    def get(self, request):

        url = PROJECT_ROOT + '/polling-units.csv'

        with open(url) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            bucket = []

            for row in csv_reader:

                sn = row[0].lower()
                state  = row[1].lower()
                senatorialZone = row[2].lower()
                lga = row[3].lower()
                ward = row[4].lower()
                pu = row[5].lower()
                delimitation = row[6].lower()

                try:

                    wardObject = Ward.objects.get( name = ward)
                    
                    pollingUnit = PollingUnit()
                    pollingUnit.ward = wardObject
                    pollingUnit.name = pu
                    pollingUnit.delimitation = delimitation
                    pollingUnit.save()


                except:

                    try:
                        lgaObject = Lga.objects.get(name = lga)

                        wardObject = Ward()
                        wardObject.name = ward
                        wardObject.lga = lgaObject
                        wardObject.save()

                        pollingUnit = PollingUnit()
                        pollingUnit.ward = wardObject
                        pollingUnit.name = pu
                        pollingUnit.delimitation = delimitation
                        pollingUnit.save()

                    except:
                        pass

                crate = {
                    'lga': lga,
                    'ward': ward,
                    'pu': pu,
                    'delimitation': delimitation
                }

                bucket.append(crate)

        return Response(str(bucket))
       
       

    def post(self, request):
        pass





class LgaView(APIView):

    def get(self, request):

        lgas = Lga.objects.all()
        serializer = LgaSerializer(lgas, many=True)

        return Response(serializer.data)

    def post(self, request):
        pass




class WardView(APIView):

    def get(self, request, lga):

        wardList = Ward.objects.filter(lga=lga)

        serializer = WardSerializer(wardList, many=True)
        return Response(serializer.data)


    def post(self, request, lga):
        pass



class PolllingUnitView(APIView):

    def get(self, request, ward):

        pollingList = PollingUnit.objects.filter(ward=ward)

        serializer = PollingUnitSerializer(pollingList, many=True)
        return Response(serializer.data)


    def post(self, request, lga):
        pass




class Signup(APIView):

    def get(self, request):
        pass

    def post(self, request):
        
        if True:
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

            # notificationToken = request.POST.get("notificationToken", "")
            name = request.POST.get("name","")
            password = request.POST.get("password","")
            gender = request.POST.get("gender","")
            isOldMember = request.POST.get("isOldMember","")
            registrationNumber = request.POST.get("registrationNumber","")
            lga = request.POST.get("lga","")
            pollingUnit = request.POST.get("pollingUnit", "")

            lgaObject = Lga.objects.get(id = lga)
            pollingUnitObject = PollingUnit.objects.get(id = pollingUnit)

            raw_password = password
            password = make_password(password)
            
            user = User()
            user.username = phone
            user.password = password
            user.name = name
            user.save()

            un = name.strip()
            username = un[0:8]


            userAccount = Account()
            userAccount.name = name
            userAccount.phone = phone
            userAccount.gender = gender
            userAccount.password = password
            userAccount.isOldMember = isOldMember
            if isOldMember == 1:
                userAccount.registrationNumber = registrationNumber
            else:
                lName = lgaObject.name
                n = random.randint(200000,500000)
                reg = "PL/" + lName[0:3] + "/13/" + str(n)
                userAccount.registrationNumber = reg.upper()

            userAccount.username = username
            userAccount.lga = lgaObject
            userAccount.pollingUnit = pollingUnitObject
            userAccount.save()

            code = 11
            success = {
                'code' : code
            }

            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)

        else:
            pass

        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)















class Signin(APIView):

    def get(self,request):
        pass

    def post(self,request):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():

            phone = serializer.data['phone']
            password = serializer.data['password']

            try:
                User.objects.get(username = phone)
                account = Account.objects.get(phone = phone)
                
                status = authenticateLogin(request, phone, password)
                
                if status : 

                    code = 11
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
                pass

            error_message = 'Oops login details do not match'
            err = {
                'error_message' : error_message
            }

            serializer = ErrorCheckSerializer( err, many=False)
            return Response(serializer.data)
        
        else:
            pass
    
        error_message = 'Sorry could not complete process, reload page and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)






class UpdateAccount(APIView):

    def get(self, request):
        pass

    
    def post(self, request):
        
        profilePicture = request.FILES.get("profilePicture","")
        
        try: 
            account = getAccount(request)
            account.image = profilePicture
            account.save()

            code = account.image

            success = {
                'code' : code
            }

            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)

        except: 
            pass

        error_message = 'Ye! something broke, please try again '
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)









class FetchUser(APIView):

    def get(self, request):
        account = getAccount(request)
        # account = Account.objects.get(id = 1)

        lga = Lga.objects.get(id = account.lga_id)
        lga_name = lga.name

        senatorial = SenatorialZone.objects.get(id = lga.senatorialzone_id)
        senatorialzone = senatorial.name

        polling = PollingUnit.objects.get(id = account.pollingUnit_id)
        pollingUnit = polling.name

        ward = Ward.objects.get(id = polling.ward_id)
        wardName = ward.name

        bucket = {
            'id': account.id,
            'registrationNumber': account.registrationNumber,
            'name': account.name,
            'image': account.image,
            'lga': lga_name,
            'pollingUnit': pollingUnit,
            'senatorialzone': senatorial,
            'ward': wardName,
            'gender': account.gender
        }

        serializer = UserDataSerializer(bucket, many=False)
        return Response(serializer.data)



    def post(self, request):
        pass








class UserView(APIView):

    def get(self, request):

        userList = Account.objects.all()

        bucket = []
        for admin in userList:

            lga = Lga.objects.get(id = admin.lga_id)
            lga_name = lga.name

            buffer = {
                'name': admin.name,
                'registrationNumber':  admin.registrationNumber,
                'lga': lga_name,
            }

            bucket.append(buffer)

        serializer = UserSerializer(bucket, many=True)
        return Response(serializer.data)