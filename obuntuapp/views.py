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
from .models import Account, Lga, SenatorialZone, AdminUser, SuperUserAdmin, PollingUnit, Ward, Post, Comment, Like, PostUpdate, Follow, Video, VideoCategory, Chat
from .serializers import AccountSerializer, NewAccountSerializer, LgaSerializer, ErrorCheckSerializer, SuccessCodeSerializer, AdminSerializer, UserSerializer, LocationSerializer, WardSerializer, PollingUnitSerializer, PostSerializer, CommentSerializer, LikeSerializer, UpdateSerializer, UserSearchSerializer, LoginSerializer, VideoSerializer, VideoCategorySerializer, ChatSerializer, UserFollowSerializer

import pandas as pd
import os
import os.path  
import sys
import csv

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





class Login(APIView):

    def get(self,request):
         
        account = Account.objects.all()
        bucket = []
        for user in account:

            following = Follow.objects.filter(following = user)
            followingRegister = []
            for f in following:
                account = Account.objects.get(id = f.account)
                followingRegister.append(account)

            followers = Follow.objects.filter(account = user.id)
            followersRegister = []
            for f in followers:
                account = Account.objects.get(id = f.following_id)
                followersRegister.append(account)

            buffer = {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'hasVotersCard': user.hasVotersCard,
                'email': user.email,
                'gender': user.gender,
                'image': user.image,
                'about': user.about,
                'following': followersRegister,
                'followers': followingRegister
            }

            bucket.append(buffer)

        serializer = UserFollowSerializer(bucket, many=True)
        return Response(serializer.data)

        






        




    def post(self,request):

        serializer = NewAccountSerializer(data=request.data)
        if serializer.is_valid():

            name = serializer.data['name']
            phone = serializer.data['phone']
            password = serializer.data['password']

            try:

                User.objects.get(username = phone)
                account = Account.objects.get(phone = phone)
                
                status = authenticateLogin(request, phone, password)
                
                if status : 
                    serializer = AccountSerializer(account, many=False)
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

            serializer = AccountSerializer(account, many=False)
            return Response(serializer.data)
        
        else:
            pass
    
        error_message = 'Sorry could not complete process, reload page and try again'
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

            notificationToken = serializer.data['notificationToken']
            phone = serializer.data['phone']
            password = serializer.data['password']

            try:
                User.objects.get(username = phone)
                account = Account.objects.get(phone = phone)
                
                status = authenticateLogin(request, phone, password)
                
                if status : 
                    account.notificationToken = notificationToken
                    account.save()

                    serializer = AccountSerializer(account, many=False)
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















class Signup(APIView):

    def get(self, request):
        pass

    def post(self, request):
        
        try:
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

            notificationToken = request.POST.get("notificationToken", "")
            name = request.POST.get("name","")
            password = request.POST.get("password","")
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

            userAccount = Account()
            userAccount.name = name
            userAccount.phone = phone
            userAccount.password = password
            userAccount.notificationToken = notificationToken
            userAccount.username = name
            userAccount.lga = lgaObject
            userAccount.pollingUnit = pollingUnitObject
            userAccount.save()

            serializer = AccountSerializer(userAccount, many=False)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)
















class UpdateAccount(APIView):

    def get(self, request):
        
        try:
            userAccount = getAccount(request)

            lgaObject = Lga.objects.get(id = userAccount.lga_id)
            pollingUnitObject = PollingUnit.objects.get(id = userAccount.pollingUnit_id)

            buffer = {
                'lga': lgaObject.name,
                'pollingUnit': pollingUnitObject.name,
                'name': userAccount.name,
                'username': userAccount.username,
                'image': userAccount.image,
                'email': userAccount.email,
                'about': userAccount.about,
                'gender': userAccount.gender,
                'hasVotersCard': userAccount.hasVotersCard
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
            name = request.POST.get("name", False)
            image = request.FILES.get("image", False)
            email = request.POST.get("email", False)
            about = request.POST.get("about", False)
            gender = request.POST.get("gender", False)
            hasVotersCard = request.POST.get("hasVotersCard", False)
            username = request.POST.get("username", False)
            lga = request.POST.get("lga", False)
            pollingUnit = request.POST.get("pollingUnit", False)

            
            userAccount = getAccount(request)
            #userAccount = Account.objects.get(id = 1)
            if name:
                userAccount.name = name
            if username:
                userAccount.username = username
            if lga:
                lgaObject = Lga.objects.get(id = lga)
                userAccount.lga = lgaObject
            if pollingUnit:
                pollingUnitObject = PollingUnit.objects.get(id = pollingUnit)
                userAccount.pollingUnit = pollingUnitObject
            if email:
                userAccount.email = email
            if about:
                userAccount.about = about
            if gender:
                userAccount.gender = gender
            if image:
                userAccount.image = image
            if hasVotersCard:
                userAccount.hasVotersCard = hasVotersCard
            userAccount.save()

            lgaObject = Lga.objects.get(id = userAccount.lga_id)
            pollingUnitObject = PollingUnit.objects.get(id = userAccount.pollingUnit_id)

            buffer = {
                'lga': lgaObject.name,
                'pollingUnit': pollingUnitObject.name,
                'name': userAccount.name,
                'username': userAccount.username,
                'image': userAccount.image,
                'email': userAccount.email,
                'about': userAccount.about,
                'gender': userAccount.gender,
                'hasVotersCard': userAccount.hasVotersCard
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
            gender = request.POST.get("gender","")
            pollingUnit = request.POST.get("pollingUnit", "")
            hasVotersCard = request.POST.get("hasVotersCard", "")
            email = request.POST.get("email","")

            lgaObject = Lga.objects.get(id = lga)
            pollingUnitObject = PollingUnit.objects.get(id = pollingUnit)

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
            admin.email = email
            admin.gender = gender
            admin.hasVotersCard = hasVotersCard
            admin.lga = lgaObject
            admin.pollingUnit = pollingUnitObject
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

        try:
            account = getAccount(request)
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
            gender = request.POST.get("gender","")
            pollingUnit = request.POST.get("pollingUnit", "")
            hasVotersCard = request.POST.get("hasVotersCard", "")
            email = request.POST.get("email","")

            lgaObject = Lga.objects.get(id = lga)
            pollingUnitObject = PollingUnit.objects.get(id = pollingUnit)

            raw_password = password
            password = make_password(password)
            
            user = User()
            user.username = phone
            user.password = password
            user.name = name
            user.save()

            userAccount = Account()
            userAccount.name = name
            userAccount.phone = phone
            userAccount.password = password
            userAccount.email = email
            userAccount.gender = gender
            userAccount.hasVotersCard = hasVotersCard
            userAccount.lga = lgaObject
            userAccount.pollingUnit = pollingUnitObject
            userAccount.save()

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









class PostView(APIView):

    def get(self, request):
        
        postList = Post.objects.all()

        bucket = []
        for post in postList:

            account = Account.objects.get(id = post.account_id)
            #updated = PostUpdate.objects.get(post = post.id)

            comments = Comment.objects.filter(post_id = post.id)
            likes = Like.objects.filter(post_id = post.id)


            commentBucket = []
            for comment in comments:

                account = Account.objects.get(id = comment.account_id)

                buffer = {
                    'comment_id': comment.id,
                    'text': comment.text,
                    'date': comment.date,
                    'user_id': account.id,
                    'user_name': account.name,
                    'username': account.username,
                    'user_image': account.image
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
                'user_name': account.name,
                'username': account.username,
                'user_image': account.image,
                'comments': commentBucket,
                'likes': likes
            }

            bucket.append(buffer)

        
        serializer = PostSerializer(bucket, many=True)
        return Response(serializer.data)


    def post(self, request):
        
        try:
            account = getAccount(request)
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
                'user_name': account.name,
                'username': account.username,
                'user_image': account.image,
                'comments': [],
                'likes': []
            }
            
            serializer = PostSerializer(bucket, many=False)
            return Response(serializer.data)

        except:
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
            account = getAccount(request)
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
            account = getAccount(request)
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

            comments = Comment.objects.filter(id = post.id).count()
            likes = Like.objects.filter(id = post.id).count()

            register = {
                'post_id': post.id,
                'title': post.title,
                'body': post.body,
                'image': post.image,
                'updated': post.date,
                'date': post.date,
                'user_id': account.id,
                'user_name': account.name,
                'username': account.username,
                'user_image': account.image,
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
            account = getAccount(request)
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

                account = Account.objects.get(id = comment.account_id)
                #updated = PostUpdate.objects.get(post = post.id)

                buffer = {
                    'comment_id': comment.id,
                    'text': comment.text,
                    'date': comment.date,
                    'user_id': account.id,
                    'user_name': account.name,
                    'username': account.username,
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
        
        try:
            account = getAccount(request)
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

                account = Account.objects.get(id = comment.account_id)
                #updated = PostUpdate.objects.get(post = post.id)

                buffer = {
                    'comment_id': comment.id,
                    'text': comment.text,
                    'date': comment.date,
                    'user_id': account.id,
                    'user_name': account.name,
                    'username': account.username,
                    'user_image': account.image
                }

                bucket.append(buffer)

        
            serializer = CommentSerializer(bucket, many=True)
            return Response(serializer.data)

        except:
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
            account = getAccount(request)
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




















class FollowView(APIView):

    def get(self, request, id):
        
        try:
            account = getAccount(request)
            following = Account.objects.get(id = id)
            try:
                follow = Follow.objects.get(account=account.id, following = following)
                follow.delete()

                code = 7
                success = {
                    'code' : code
                }

                serializer = SuccessCodeSerializer(success, many = False)
                return Response(serializer.data)

            except:
                pass

            follow = Follow()
            follow.account = account.id
            follow.following = following
            follow.save()

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













class UserSearch(APIView):

    def get(self, request):
        
        try:
            account = getAccount(request)
            userList = Account.objects.all()

            bucket = []
            for user in userList:
                
                follow = False
                try:
                    follow = Follow.objects.get(following_id=user.id, account = account.id)
                    follow = True
                except:
                    pass

                buffer = {
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'image': user.image,
                    'about': user.about,
                    'isFollowing': follow
                }

                bucket.append(buffer)

            serializer = UserSearchSerializer(bucket, many=True)
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
        pass











class VideoCategoryView(APIView):

    def get(self, request):

        categories = VideoCategory.objects.all()
        serializer = VideoCategorySerializer(categories, many=True)

        return Response(serializer.data)

    def post(self, request):
        pass







class ChatView(APIView):

    def get(self, request, id):
        
        try:
            account = getAccount(request)
            #account = Account.objects.get(id = 1)
            chat = Chat.objects.filter(Q(sender = account) | Q(receiver = account.id))

            bucket = []
            for item in chat:
                receiver = Account.objects.get(id = item.receiver)

                buffer = {
                    'id': item.id,
                    'time': item.date,
                    'message': item.message,
                    'sender': item.sender,
                    'reciever': receiver
                }

                bucket.append(buffer)

            
            serializer = ChatSerializer(bucket, many=True)
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
            account = getAccount(request)
            #account = Account.objects.get(id = 1)
            message = request.POST.get("message","")

            receiver = Account.objects.get(id = id)

            chat = Chat()
            chat.sender = account
            chat.receiver = id
            chat.message = message
            chat.save()

            buffer = {
                'id': chat.id,
                'time': chat.date,
                'message': chat.message,
                'sender': chat.sender,
                'reciever': receiver
            }

            serializer = ChatSerializer(buffer, many=False)
            return Response(serializer.data)

        
        except:
            pass

        error_message = 'Sorry something went wrong, retry'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)














class ChatListView(APIView):

    def get(self, request):
        
        if True:
            account = getAccount(request)
            #account = Account.objects.get(id = 1)
            chat = Chat.objects.filter(Q(sender = account) | Q(receiver = account.id))

            bucket = []
            for item in chat:
                
                
                try:
                    isSender = Chat.objects.get(sender = account)
                    user = Account.objects.get(id = item.sender_id)
                except:
                    user = Account.objects.get(id = item.receiver)
                
                if user.id == account.id:
                    pass
                else:
                    if user in bucket:
                        pass
                    else:
                        bucket.append(user)
            
            serializer = AccountSerializer(bucket, many=True)
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