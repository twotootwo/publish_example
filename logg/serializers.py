# from django.contrib.auth import authenticate
# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers
# from rest_framework.authtoken.admin import User
#
# from rest_framework.authtoken.models import Token
# from rest_framework.validators import UniqueValidator


#
# # 회원가입
# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         validators=[validate_password],
#     )
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password2', 'email')
#
#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match."}
#             )
#         return data
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],  # 아이디
#             email=validated_data['email'],  # 이메일
#         )
#         user.set_password(validated_data['password'])  # 비밀번호
#         user.save()
#         token = Token.objects.create(user=user)
#         return user
#
#
# # 로그인
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True, write_only=True)
#
#     def validate(self, data):
#         user = authenticate(**data)
#         if user:
#             token = Token.objects.get(user=user)
#             return token
#         raise serializers.ValidationError(
#             {"error": "Unable to log in with provided credentials."}
#         )
#
#
# # 프로필
# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields = ("nickname", "position", "subjects", "image")
#
#
# # class UserSerializer(serializers.ModelSerializer):
# #     email = serializers.EmailField(required=True)
# #
# #     class Meta:
# #         model = User
# #         fields = ("id", "username","password","email")
# #         extra_kwargs = {
# #             "password": {"write_only": True}
# #         }
# #
# #     def create(self, validated_data):
# #         user = User.objects.create_user(
# #             username=validated_data['username'],
# #             password=validated_data['password'],
# #             email = validated_data['email']
# #         )
# #         Token.objects.create(user=user)
# #         return user
