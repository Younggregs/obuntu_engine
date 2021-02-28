from rest_framework import serializers
from .models import Account, Lga


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'


class NewAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['phone','name','password']


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