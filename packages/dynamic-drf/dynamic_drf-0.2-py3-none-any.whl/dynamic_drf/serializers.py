from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model



User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()    

    def validate(self,attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(email=email,password=password)
        if not user :
            raise serializers.ValidationError("User with such credentials doesn't exits")
        token = self.get_token(user)
        response = {
            "refresh":str(token),
            "access":str(token.access_token)
        }
        return response
        
    @classmethod
    def get_token(cls,user):
        return super().get_token(user)




