from .models import Contacts

from rest_framework import serializers
from django.contrib.auth.models import User

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()

        if user is None:
            raise serializers.ValidationError("User does not exist.")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        data['user'] = user
        return data

class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        """
        Custom validation for checking if the username is unique.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def validate_email(self, value):
        """
        Custom validation for checking if the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate(self, data):
        """
        Additional validation if needed for the registration process.
        """
        # You can add more custom validation here based on your requirements.
        return data

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'first_name', 'last_name', 'phone_number']

    def create(self, validated_data):
        """
        Create and return a new contact instance, given the validated data.
        """
        return Contacts.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing contact instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
