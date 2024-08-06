from rest_framework import serializers
from .models import Notice, NoticeImage
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model, login as auth_login
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status

# from django.contrib.auth.models import User

UserModel = get_user_model()

class NoticeImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = NoticeImage
        fields = ["id", "notice","image"]

class NoticeSerializer(serializers.ModelSerializer):
    images = NoticeImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length = 1000000,allow_empty_file=False, use_url=False),
                                            write_only=True)
    class Meta:
        model = Notice
        fields = ["id", "title", "description", "images", "uploaded_images"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        notice = Notice.objects.create(**validated_data)

        for image in uploaded_images:
            NoticeImage.objects.create(notice=notice, image=image)

        return notice

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(password = clean_data['password'])
        user_obj.username = clean_data['username']
        # user.is_staff = True
        user_obj.save()
        return user_obj

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 255)
    password = serializers.CharField(
        label=_("Password"),
        style={'input-type': 'password'},
        max_length = 255,
        write_only = True
    )
# class LoginAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response({'detail': 'Form validation failed'}, status=status.HTTP_400_BAD_REQUEST)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'password')

    def validate(self, clean_data):
        username = clean_data.get('username')
        password  = clean_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                message = _('Invalid cerdintials')
                raise serializers.ValidationError(message, code= 'authorization')
            return user
        else:
            message = _('Please enter your cerdintials')
            raise serializers.ValidationError(message, code= 'authorization')
        
        # data ['user'] = user
        # return data
