from rest_framework import serializers

from .models import UserModel, CityModel


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = ['id', 'name']
        read_only_fields = ['id']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label='Логин', help_text='Введите логин или почту')
    password = serializers.CharField(label='Пароль', style={"input_type": "password"})


class UserCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'login', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'is_admin']
        read_only_fields = ['id', 'is_admin']


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'login', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class PrivateUsersListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = UserModel
        fields = ['id', 'login', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'city',
                  'additional_info', 'is_admin', 'password']
        read_only_fields = ['id']
        extra_kwargs = {'is_admin': {'write_only': True}, 'other_name': {'write_only': True},
                        'phone': {'write_only': True}, 'birthday': {'write_only': True},
                        'additional_info': {'write_only': True}, }

    def create(self, validated_data):
        user_password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(user_password)
        user.save()
        return user


class PrivateUsersRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'login', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'city',
                  'additional_info', 'is_admin', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']
