from rest_framework import serializers
from .models import Account, Lga, Ward, PollingUnit, Like, Video, VideoCategory


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id','name','username', 'email', 'image', 'about']


class NewAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['phone','name','password']


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['phone','password','notificationToken']


class UserSearchSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    username = serializers.CharField()
    image = serializers.CharField()
    about = serializers.CharField()
    isFollowing = serializers.BooleanField()
    


class UpdateSerializer(serializers.Serializer):
    lga = serializers.CharField()
    pollingUnit = serializers.CharField()
    name = serializers.CharField()
    username = serializers.CharField()
    image = serializers.CharField()
    gender = serializers.CharField()
    hasVotersCard = serializers.BooleanField()
    email = serializers.CharField()
    about = serializers.CharField()



class AdminSerializer(serializers.Serializer):
    isSuperUser = serializers.BooleanField()
    phone = serializers.CharField()
    name = serializers.CharField()
    lga = serializers.CharField()
    signedUsers = serializers.IntegerField()



class UserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    name = serializers.CharField()
    lga = serializers.CharField()


class LocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    users = serializers.CharField()


class ErrorCheckSerializer(serializers.Serializer):
    error_message = serializers.CharField()



class SuccessCodeSerializer(serializers.Serializer):
    code = serializers.CharField()



class LgaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lga
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ward
        fields = '__all__'


class PollingUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollingUnit
        fields = '__all__'



class CommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    username = serializers.CharField()
    user_image = serializers.CharField()
    text = serializers.CharField()
    date = serializers.CharField()



class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['account_id']



class PostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    user_image = serializers.CharField()
    username = serializers.CharField()
    title = serializers.CharField()
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    body = serializers.CharField()
    image = serializers.CharField()
    updated = serializers.CharField()
    date = serializers.CharField()





class VideoCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoCategory
        fields = '__all__'




class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'



class ChatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    message = serializers.CharField()
    sender = AccountSerializer()
    receiver = AccountSerializer()
    time = serializers.CharField()



class UserFollowSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    username = serializers.CharField()
    image = serializers.CharField()
    about = serializers.CharField()
    following = AccountSerializer(many=True)
    followers = AccountSerializer(many=True)
