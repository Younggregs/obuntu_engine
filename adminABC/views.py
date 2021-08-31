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
from .models import Account, Lga, SenatorialZone, AdminUser, SuperUserAdmin, PollingUnit, Ward, DemoAccount, Post, Comment, Like, PostUpdate
from .serializers import DataSerializer, AccountSerializer, NewAccountSerializer, LgaSerializer, ErrorCheckSerializer, SuccessCodeSerializer, AdminSerializer, UserSerializer, LocationSerializer, WardSerializer, PollingUnitSerializer, LoginSerializer, UserDataSerializer, PostSerializer, CommentSerializer, LikeSerializer, UserSearchSerializer, UpdateSerializer

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
        internalId = user.username

        account = Account.objects.get(internalId=internalId)
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









def createInternalId(pu, pollingUnit):

    status = True
    x = 1
    while status:

        count = Account.objects.filter(pollingUnit = pollingUnit).count()
        puBuffer = pu.split('/')
        pu = puBuffer[0] + '-' + puBuffer[1] + '-' + puBuffer[2] + '-' + puBuffer[3]
        internalId = pu + '-' + str(count + x)

        try: 
            account = Account.objects.get(internalId = internalId)
        except:
            status = False

        x = x + 1

    return internalId




def createInternalIdDemo(pu, pollingUnit):

    status = True
    x = 1
    while status:

        count = Account.objects.filter(pollingUnit = pollingUnit).count()
        # puBuffer = pu.split('/')
        # pu = puBuffer[0] + '-' + puBuffer[1] + '-' + puBuffer[2] + '-' + puBuffer[3]
        internalId = pu + '-' + str(count + x)

        try: 
            account = DemoAccount.objects.get(internalId = internalId)
        except:
            status = False

        x = x + 1

    return internalId




class DataEntry(APIView):

    def get(self, request):

        if True:
            data = Account.objects.order_by().values_list('pollingUnit').distinct()
            # failedList = PollingUnit.objects.exclude(id__in = data)
            successList = PollingUnit.objects.filter(id__in = data)

            bucket = []
            for item in successList:
                unit = PollingUnit.objects.get(id = item.id)
                ward = Ward.objects.get(id = unit.ward_id)
                lga = Lga.objects.get(id = ward.lga_id)

                register = {
                    'lga': lga.name,
                    'ward': ward.name,
                    'pollingUnit': unit.name
                }

                bucket.append(register)

            serializer = DataSerializer(bucket, many = True)
            return Response(serializer.data)

        else:
            pass

        return Response('Failure!')





class Unboard(APIView):

    def get(self, request):

        # try:
        #     Account.objects.all().delete()
        #     return Response('Success!')
        # except:
        #     pass

        return Response('Failure!')



class Onboard(APIView):

    def get(self, request):

        url = PROJECT_ROOT + '/sheet2.csv'
        # Account.objects.all().delete()
        with open(url) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            x = 0
            failedRegister = []
            for row in csv_reader:

                p = row[7].lower()
                if x != 0 and len(p) > 5: 
                    sn = row[0].lower()
                    firstname  = row[1].lower()
                    middlename = row[2].lower()
                    lastname = row[3].lower()
                    phone = row[4].lower()
                    gender = row[5].lower()
                    membership = row[6].lower()
                    pu = row[7].lower()
                    votercard = row[8].lower()
                    age = row[9].lower()

                    if len(phone) > 8:
                        phone = '0' + str(phone)

                    try:

                        try:
                            pollingUnit = PollingUnit.objects.get(delimitation = str(pu))
                            wardObject = Ward.objects.get(id = pollingUnit.ward_id)
                            lgaObject = Lga.objects.get(id = wardObject.lga_id)

                            internalId = createInternalId(pu, pollingUnit.id)

                            userAccount = Account()
                            userAccount.internalId = internalId
                            userAccount.firstname = firstname
                            userAccount.middlename = middlename
                            userAccount.lastname = lastname
                            userAccount.age = age
                            userAccount.votercard = votercard
                            userAccount.phone = phone
                            userAccount.gender = gender
                            userAccount.password = 'password'
                            userAccount.lga = lgaObject
                            userAccount.ward = wardObject
                            userAccount.pollingUnit = pollingUnit
                            userAccount.save()

                            # user = User()
                            # user.username = userAccount.internalId
                            # user.password = 'password'
                            # user.name = firstname + ' ' +  middlename + ' ' + lastname
                            # user.save()

                        except:
                            
                            failedRegister.append({'pu': pu})

                    
                    except:
                        pass

                else:
                    pass

                x = x + 1

        code = x
        success = {
            'code' : code
        }

        serializer = SuccessCodeSerializer(success, many = False)
        return Response(serializer.data)
       
       

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



class PollingUnitView(APIView):

    def get(self, request, ward):

        pollingList = PollingUnit.objects.filter(ward=ward)

        serializer = PollingUnitSerializer(pollingList, many=True)
        return Response(serializer.data)


    def post(self, request, lga):
        pass





class IsSuperUser(APIView):

    def get(self, request):

        try:
            account = getAccount(request)
            return Response(account.isSuperUser)
        except:
            pass

        return Response(False)

    def post(self, request):
        pass

    




class MemberCountView(APIView):

    def get(self, request):

        count = Account.objects.all().count()
        success = {
                'code' : count
        }

        serializer = SuccessCodeSerializer(success, many = False)
        return Response(serializer.data)

    def post(self, request):
        pass





class Signup(APIView):

    def get(self, request):
        pass

    def post(self, request):
        
        if True:
            phone = request.POST.get("phone","")

            try:
                accountExist = Account.objects.get(phone=phone)

                error_message = 'Account with this phone number already exist'
                err = {
                    'error_message' : error_message
                }
                serializer = ErrorCheckSerializer( err, many=False)
                return Response(serializer.data)
            except:
                pass

            registrationNumber = request.POST.get("registrationNumber","")

            try:
                accountExist = Account.objects.get(registrationNumber=registrationNumber)

                error_message = 'Account with this registration number already exist'
                err = {
                    'error_message' : error_message
                }
                serializer = ErrorCheckSerializer( err, many=False)
                return Response(serializer.data)
            except:
                pass

            # notificationToken = request.POST.get("notificationToken", "")
            firstname = request.POST.get("firstname","")
            middlename = request.POST.get("middlename","")
            lastname = request.POST.get("lastname","")
            age = request.POST.get("age","")
            votercard = request.POST.get("votercard","")
            password = request.POST.get("password","")
            gender = request.POST.get("gender","")
            isOldMember = request.POST.get("isOldMember","")
            registrationNumber = request.POST.get("registrationNumber","")
            lga = request.POST.get("lga","")
            ward = request.POST.get("ward", "")
            pollingUnit = request.POST.get("pollingUnit", "")

            lgaObject = Lga.objects.get(id = lga)
            wardObject = Ward.objects.get(id = ward)
            pollingUnitObject = PollingUnit.objects.get(id = pollingUnit)

            raw_password = password
            password = make_password(password)

            userAccount = Account()
            userAccount.firstname = firstname
            userAccount.middlename = middlename
            userAccount.lastname = lastname
            userAccount.age = age
            userAccount.votercard = votercard
            userAccount.phone = phone
            userAccount.gender = gender
            userAccount.password = password
            userAccount.isOldMember = isOldMember
            if isOldMember == 1:
                userAccount.registrationNumber = registrationNumber
            else:
                lName = lgaObject.name
                n = random.randint(200000,500000)
                reg = "PL/" + lgaObject.code + "/" + pollingUnit + "/" + str(n)
                userAccount.registrationNumber = reg.upper()

            userAccount.lga = lgaObject
            userAccount.ward = wardObject
            userAccount.pollingUnit = pollingUnitObject
            internalId = createInternalId(pollingUnitObject.delimitation, pollingUnit)
            userAccount.internalId = internalId
            userAccount.save()

            user = User()
            user.username = userAccount.internalId
            user.password = password
            user.firstname = firstname
            user.lastname = lastname
            user.save()

            code = userAccount.internalId

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

        try:
            username = request.POST.get("username","")
            password = request.POST.get("password","")

            registrationNumber = 1

            try:
                account = Account.objects.get(phone = username)
                registrationNumber = account.internalId
            except:
                pass

            try:
                account = Account.objects.get(internalId = username)
                internalId = account.internalId
            except:
                pass

            
            if internalId != 1:

                try:
                    User.objects.get(username = internalId)
                    account = Account.objects.get(internalId = internalId)
                    
                    status = authenticateLogin(request, internalId, password)
                    
                    if status : 

                        code = account.internalId
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
                error_message = 'Registration number/ Phone do not exist'
                err = {
                    'error_message' : error_message
                }
                serializer = ErrorCheckSerializer( err, many=False)
                return Response(serializer.data)

        
        except:
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
            'firstname': account.firstname,
            'middlename': account.middlename,
            'lastname': account.lastname,
            'image': account.image,
            'lga': lga_name,
            'pollingUnit': pollingUnit,
            'senatorialzone': senatorial,
            'ward': wardName,
            'gender': account.gender, 
            'age': account.age,
            'internalId': account.internalId
        }

        serializer = UserDataSerializer(bucket, many=False)
        return Response(serializer.data)



    def post(self, request):
        pass








class UserView(APIView):

    def get(self, request):

        userList = Account.objects.all()[:50]

        bucket = []
        for admin in userList:

            lga = Lga.objects.get(id = admin.lga_id)
            lga_name = lga.name

            senatorial = SenatorialZone.objects.get(id = lga.senatorialzone_id)
            senatorialzone = senatorial.name

            polling = PollingUnit.objects.get(id = admin.pollingUnit_id)
            pollingUnit = polling.name

            ward = Ward.objects.get(id = polling.ward_id)
            wardName = ward.name

            buffer = {
                'id': admin.id,
                'registrationNumber': admin.registrationNumber,
                'firstname': admin.firstname,
                'middlename': admin.middlename,
                'lastname': admin.lastname,
                'image': admin.image,
                'lga': lga_name,
                'pollingUnit': pollingUnit,
                'senatorialzone': senatorial,
                'ward': wardName,
                'gender': admin.gender,
                'age': admin.age,
                'internalId': admin.internalId
            }

            bucket.append(buffer)

        serializer = UserDataSerializer(bucket, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass






class FilterByLga(APIView):

    def get(self, request):
        pass

    def post(self, request):

        lga = request.POST.get("lga", "")
        userList = Account.objects.filter(lga = lga)

        bucket = []
        x = 1
        for admin in userList:

            lga = Lga.objects.get(id = admin.lga_id)
            lga_name = lga.name

            senatorial = SenatorialZone.objects.get(id = lga.senatorialzone_id)
            senatorialzone = senatorial.name

            polling = PollingUnit.objects.get(id = admin.pollingUnit_id)
            pollingUnit = polling.name

            ward = Ward.objects.get(id = polling.ward_id)
            wardName = ward.name

            buffer = {
                'id': x,
                'registrationNumber': admin.registrationNumber,
                'firstname': admin.firstname,
                'middlename': admin.middlename,
                'lastname': admin.lastname,
                'image': admin.image,
                'lga': lga_name,
                'pollingUnit': pollingUnit,
                'senatorialzone': senatorial,
                'ward': wardName,
                'gender': admin.gender,
                'age': admin.age,
                'internalId': admin.internalId
            }

            bucket.append(buffer)

            x = x + 1

        serializer = UserDataSerializer(bucket, many=True)
        return Response(serializer.data)







class FilterByWard(APIView):

    def get(self, request):
        pass

    def post(self, request):

        ward = request.POST.get("ward", "")
        userList = Account.objects.filter(ward = ward)

        bucket = []
        x = 1
        for admin in userList:

            lga = Lga.objects.get(id = admin.lga_id)
            lga_name = lga.name

            senatorial = SenatorialZone.objects.get(id = lga.senatorialzone_id)
            senatorialzone = senatorial.name

            polling = PollingUnit.objects.get(id = admin.pollingUnit_id)
            pollingUnit = polling.name

            ward = Ward.objects.get(id = polling.ward_id)
            wardName = ward.name

            buffer = {
                'id': x,
                'registrationNumber': admin.registrationNumber,
                'firstname': admin.firstname,
                'middlename': admin.middlename,
                'lastname': admin.lastname,
                'image': admin.image,
                'lga': lga_name,
                'pollingUnit': pollingUnit,
                'senatorialzone': senatorial,
                'ward': wardName,
                'gender': admin.gender,
                'age': admin.age,
                'internalId': admin.internalId
            }

            bucket.append(buffer)

            x = x + 1

        serializer = UserDataSerializer(bucket, many=True)
        return Response(serializer.data)





class FilterByPoll(APIView):

    def get(self, request):
        pass

    def post(self, request):

        pollingUnit = request.POST.get("pollingUnit", "")
        userList = Account.objects.filter(pollingUnit = pollingUnit)

        bucket = []
        x = 1
        for admin in userList:

            lga = Lga.objects.get(id = admin.lga_id)
            lga_name = lga.name

            senatorial = SenatorialZone.objects.get(id = lga.senatorialzone_id)
            senatorialzone = senatorial.name

            polling = PollingUnit.objects.get(id = admin.pollingUnit_id)
            pollingUnit = polling.name

            ward = Ward.objects.get(id = polling.ward_id)
            wardName = ward.name

            buffer = {
                'id': x,
                'registrationNumber': admin.registrationNumber,
                'firstname': admin.firstname,
                'middlename': admin.middlename,
                'lastname': admin.lastname,
                'image': admin.image,
                'lga': lga_name,
                'pollingUnit': pollingUnit,
                'senatorialzone': senatorial,
                'ward': wardName,
                'gender': admin.gender,
                'age': admin.age,
                'internalId': admin.internalId
            }

            bucket.append(buffer)

            x = x + 1

        serializer = UserDataSerializer(bucket, many=True)
        return Response(serializer.data)







class SearchByName(APIView):

    def get(self, request):
        pass

    def post(self, request):

        name = request.POST.get("name", "")
        userList = Account.objects.filter(firstname__icontains = name) | Account.objects.filter(middlename__icontains = name)  | Account.objects.filter(lastname__icontains = name)

        bucket = []
        x = 1
        for admin in userList:

            lga = Lga.objects.get(id = admin.lga_id)
            lga_name = lga.name

            senatorial = SenatorialZone.objects.get(id = lga.senatorialzone_id)
            senatorialzone = senatorial.name

            polling = PollingUnit.objects.get(id = admin.pollingUnit_id)
            pollingUnit = polling.name

            ward = Ward.objects.get(id = polling.ward_id)
            wardName = ward.name

            buffer = {
                'id': x,
                'registrationNumber': admin.registrationNumber,
                'firstname': admin.firstname,
                'middlename': admin.middlename,
                'lastname': admin.lastname,
                'image': admin.image,
                'lga': lga_name,
                'pollingUnit': pollingUnit,
                'senatorialzone': senatorial,
                'ward': wardName,
                'gender': admin.gender,
                'age': admin.age,
                'internalId': admin.internalId
            }

            bucket.append(buffer)

            x = x + 1

        serializer = UserDataSerializer(bucket, many=True)
        return Response(serializer.data)








# Demo account

def getDemoAccount(request):

    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        registrationNumber = user.username

        account = DemoAccount.objects.get(registrationNumber=registrationNumber)
        return account

    else:
        
        return -1






class DemoSignup(APIView):

    def get(self, request):
        pass

    def post(self, request):
        
        try:
            phone = request.POST.get("phone","")

            try:
                accountExist = DemoAccount.objects.get(phone=phone)

                error_message = 'Account with this phone number already exist'
                err = {
                    'error_message' : error_message
                }
                serializer = ErrorCheckSerializer( err, many=False)
                return Response(serializer.data)
            except:
                pass

            registrationNumber = request.POST.get("registrationNumber","")

            try:
                accountExist = DemoAccount.objects.get(registrationNumber=registrationNumber)

                error_message = 'Account with this registration number already exist'
                err = {
                    'error_message' : error_message
                }
                serializer = ErrorCheckSerializer( err, many=False)
                return Response(serializer.data)
            except:
                pass

            # notificationToken = request.POST.get("notificationToken", "")
            firstname = request.POST.get("firstname","")
            middlename = request.POST.get("middlename","")
            lastname = request.POST.get("lastname","")
            age = request.POST.get("age","")
            votercard = request.POST.get("votercard","")
            password = request.POST.get("password","")
            gender = request.POST.get("gender","")
            isOldMember = request.POST.get("isOldMember","")
            registrationNumber = request.POST.get("registrationNumber","")
            lga = request.POST.get("lga","")
            ward = request.POST.get("ward", "")
            pollingUnit = request.POST.get("pollingUnit", "")

            lgaObject = Lga.objects.get(id = lga)
            wardObject = Ward.objects.get(id = ward)
            pollingUnitObject = PollingUnit.objects.get(id = pollingUnit)

            raw_password = password
            password = make_password(password)

            userAccount = DemoAccount()
            userAccount.firstname = firstname
            userAccount.middlename = middlename
            userAccount.lastname = lastname
            userAccount.age = age
            userAccount.votercard = votercard
            userAccount.phone = phone
            userAccount.gender = gender
            userAccount.password = password
            userAccount.isOldMember = isOldMember
            if isOldMember == 1:
                userAccount.registrationNumber = registrationNumber
            else:
                lName = lgaObject.name
                n = random.randint(200000,500000)
                reg = "PL/" + lgaObject.code + "/" + pollingUnit + "/" + str(n)
                userAccount.registrationNumber = reg.upper()

            userAccount.lga = lgaObject
            userAccount.ward = wardObject
            userAccount.pollingUnit = pollingUnitObject
            internalId = createInternalIdDemo(pollingUnitObject.delimitation, pollingUnit)
            userAccount.internalId = internalId
            userAccount.save()

            user = User()
            user.username = userAccount.internalId
            user.password = password
            user.name = firstname + ' ' +  middlename + ' ' + lastname
            user.save()

            code = userAccount.internalId

            success = {
                'code' : code
            }

            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)















class DemoSignin(APIView):

    def get(self,request):
        pass

    def post(self,request):

        try:
            username = request.POST.get("username","")
            password = request.POST.get("password","")

            registrationNumber = 1

            try:
                account = DemoAccount.objects.get(phone = username)
                internalId = account.registrationNumber
            except:
                pass

            try:
                account = DemoAccount.objects.get(internalId = username)
                internalId = account.internalId
            except:
                pass

            
            if internalId != 1:

                try:
                    User.objects.get(username = internalId)
                    account = DemoAccount.objects.get(internalId = internalId)
                    
                    status = authenticateLogin(request, internalId, password)
                    
                    if status : 

                        code = account.internalId
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
                error_message = 'Registration/Phone number do not exist'
                err = {
                    'error_message' : error_message
                }
                serializer = ErrorCheckSerializer( err, many=False)
                return Response(serializer.data)

        
        except:
            pass
    
        error_message = 'Sorry could not complete process, reload page and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)






class PostView(APIView):

    def get(self, request):
        
        postList = Post.objects.all()

        bucket = []
        for post in postList:

            account = DemoAccount.objects.get(id = post.account_id)
            #updated = PostUpdate.objects.get(post = post.id)

            comments = Comment.objects.filter(post_id = post.id)
            likes = Like.objects.filter(post_id = post.id)


            commentBucket = []
            for comment in comments:

                commenter = DemoAccount.objects.get(id = comment.account_id)

                buffer = {
                    'comment_id': comment.id,
                    'text': comment.text,
                    'date': comment.date,
                    'user_id': commenter.id,
                    'user_name': commenter.name,
                    'username': commenter.username,
                    'isVerified': commenter.isVerified,
                    'user_image': commenter.image
                }

                commentBucket.append(buffer)


            buffer = {
                'post_id': post.id,
                'title': post.title,
                'body': post.body,
                'image': post.image,
                'updated': post.date,
                'date': post.date,
                'user_id': account.id,
                'user_name': account.firstname + ' ' + account.middlename + ' ' + account.lastname,
                'user_image': account.image,
                'isVerified': account.isVerified,
                'office': account.office,
                'comments': commentBucket,
                'likes': likes
            }

            bucket.append(buffer)

        
        serializer = PostSerializer(bucket, many=True)
        return Response(serializer.data)


    def post(self, request):
        
        if True:
            # account = getDemoAccount(request)
            account = DemoAccount.objects.get(id = 8)
            title = request.POST.get("title","")
            body = request.POST.get("body","")
            image = request.FILES.get("image",False)

            post = Post()
            post.account = account
            post.title = title
            if image:
                post.image = image
            post.body = body
            post.save()

            bucket = {
                'post_id': post.id,
                'title': post.title,
                'body': post.body,
                'image': post.image,
                'updated': post.date,
                'date': post.date,
                'user_id': account.id,
                'user_name': account.firstname + ' ' + account.middlename + ' ' + account.lastname,
                'user_image': account.image,
                'isVerified': account.isVerified,
                'office': account.office,
                'comments': [],
                'likes': []
            }
            
            serializer = PostSerializer(bucket, many=False)
            return Response(serializer.data)

        else:
            pass


        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)















class UpdatePost(APIView):

    def get(self, request, id):
        
        try:
            account = getDemoAccount(request)
            post = Post.objects.get(id = id)
            post.delete()

            code = 11
            success = {
                'code' : code
            }

            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)

        
        except:
            pass

        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)


    def post(self, request, id):
        
        try:
            # account = getDemoAccount(request)
            account = DemoAccount.objects.get(id = 8)
            title = request.POST.get("title", False)
            body = request.POST.get("body", False)
            image = request.FILES.get("image", False)

            post = Post.objects.get(id = id)
            post.account = account
            if title:
                post.title = title
            if image:
                post.image = image
            if body:
                post.body = body
            post.save()

            comments = Comment.objects.filter(id = post.id)
            likes = Like.objects.filter(id = post.id)

            register = {
                'post_id': post.id,
                'title': post.title,
                'body': post.body,
                'image': post.image,
                'updated': post.date,
                'date': post.date,
                'user_id': account.id,
                'user_name': account.firstname + ' ' + account.middlename + ' ' + account.lastname,
                'user_image': account.image,
                'isVerified': account.isVerified,
                'office': account.office,
                'comments': comments,
                'likes': likes
            }

            serializer = PostSerializer(register, many=False)
            return Response(serializer.data)

        except:
            pass


        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)






class LikePost(APIView):

    def get(self, request, id):
        
        try:
            # account = getDemoAccount(request)
            account = DemoAccount.objects.get(id = 8)
            post = Post.objects.get(id = id)
            try:
                like = Like.objects.get(post_id = id, account=account)
                like.delete()

                code = 7
                success = {
                    'code' : code
                }

                serializer = SuccessCodeSerializer(success, many = False)
                return Response(serializer.data)

            except:
                pass

            like = Like()
            like.account = account
            like.post = post
            like.save()

            code = 11
            success = {
                'code' : code
            }

            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)
        
        except:
            pass

        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    
    def post(self, request, id):

        try:
            likeList = Like.objects.filter(id = id).count()

            success = {
                'code' : likeList
            }

            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Could not fetch likes'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)








class CommentView(APIView):
    
    def get(self, request, id):
        
        try:
            commentList = Comment.objects.filter(post = id)

            bucket = []
            for comment in commentList:

                account = DemoAccount.objects.get(id = comment.account_id)
                #updated = PostUpdate.objects.get(post = post.id)

                buffer = {
                    'comment_id': comment.id,
                    'text': comment.text,
                    'date': comment.date,
                    'user_id': account.id,
                    'user_name': account.firstname + ' ' + account.middlename + ' ' + account.lastname,
                    'username': account.username,
                    'isVerified': account.isVerified,
                    'user_image': account.image
                }

                bucket.append(buffer)

        
            serializer = CommentSerializer(bucket, many=True)
            return Response(serializer.data)

        except:
            pass


        error_message = 'Sorry could not fetch comments'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

        

    
    def post(self, request, id):
        
        if True:
            # account = getDemoAccount(request)
            account = DemoAccount.objects.get(id = 8)
            post = Post.objects.get(id = id)

            text = request.POST.get("text","")

            comment = Comment()
            comment.account = account
            comment.post = post
            comment.text = text
            comment.save()

            commentList = Comment.objects.filter(post = id)

            bucket = []
            for comment in commentList:

                commenter = DemoAccount.objects.get(id = comment.account_id)
                #updated = PostUpdate.objects.get(post = post.id)

                buffer = {
                    'comment_id': comment.id,
                    'text': comment.text,
                    'date': comment.date,
                    'user_id': commenter.id,
                    'user_name': commenter.firstname + ' ' + commenter.middlename + ' ' + commenter.lastname,
                    'office': commenter.office,
                    'isVerified': commenter.isVerified,
                    'user_image': commenter.image
                }

                bucket.append(buffer)

        
            serializer = CommentSerializer(bucket, many=True)
            return Response(serializer.data)

        else:
            pass


        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)






class RemoveComment(APIView):

    def get(self, request, id):
        
        try: 
            # account = getDemoAccount(request)
            account = DemoAccount.objects.get(id = 8)
            comment = Comment.objects.get(id = id, account=account)
            comment.delete()

            code = 11
            success = {
                'code' : code
            }

            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)

        except:
            pass


        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)
        

    def post(self, request, id):
        pass





class DemoUserSearch(APIView):

    def get(self, request):
        
        if True:
            # account = getDemoAccount(request)
            account = DemoAccount.objects.get(id = 8)
            userList = DemoAccount.objects.exclude(id = account.id)

            bucket = []
            for user in userList:
                
                buffer = {
                    'id': user.id,
                    'name': user.firstname + ' ' + user.middlename + ' ' + user.lastname,
                    'office': user.office,
                    'image': user.image,
                    'isVerified': user.isVerified
                }

                bucket.append(buffer)

            serializer = UserSearchSerializer(bucket, many=True)
            return Response(serializer.data)


        else:
            pass

        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)


    def post(self, request):
        pass






class DemoUpdateAccount(APIView):

    def get(self, request):
        
        try:
            # userAccount = getDemoAccount(request)
            userAccount = DemoAccount.objects.get(id = 8)

            lgaObject = Lga.objects.get(id = userAccount.lga_id)
            pollingUnitObject = PollingUnit.objects.get(id = userAccount.pollingUnit_id)

            buffer = {
                'lga': lgaObject.name,
                'pollingUnit': pollingUnitObject.name,
                'firstname': userAccount.firstname,
                'middlename': userAccount.middlename,
                'lastname': userAccount.lastname,
                'office': userAccount.office,
                'image': userAccount.image,
                'gender': userAccount.gender,
            }

            serializer = UpdateSerializer(buffer, many=False)
            return Response(serializer.data)
        
        except:
            pass

            
        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)



    def post(self, request):
        
        try:
            firstname = request.POST.get("firstname", False)
            middlename = request.POST.get("middlename", False)
            lastname = request.POST.get("lastname", False)
            image = request.FILES.get("image", False)
            gender = request.POST.get("gender", False)
            
            # userAccount = getDemoAccount(request)
            userAccount = DemoAccount.objects.get(id = 8)
            if firstname:
                userAccount.firstname = firstname
            if middlename:
                userAccount.middlename = middlename
            if lastname:
                userAccount.lastname = lastname
            if image:
                userAccount.image = image
            userAccount.save()

            lgaObject = Lga.objects.get(id = userAccount.lga_id)
            pollingUnitObject = PollingUnit.objects.get(id = userAccount.pollingUnit_id)

            buffer = {
                'lga': lgaObject.name,
                'pollingUnit': pollingUnitObject.name,
                'firstname': userAccount.firstname,
                'middlename': userAccount.middlename,
                'lastname': userAccount.lastname,
                'office': userAccount.office,
                'image': userAccount.image,
                'gender': userAccount.gender,
            }

            serializer = UpdateSerializer(buffer, many=False)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)
