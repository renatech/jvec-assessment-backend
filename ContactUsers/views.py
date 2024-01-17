from .models import Contacts

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import permissions

from .serializer import UserLoginSerializer, UserRegistrationSerializer, ContactSerializer


class GetLoggedInUsername(APIView):
    def get(self, request):
        username = request.user.username
        return Response({'username': username})


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view.

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token,created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            # print("my errors are ", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view.

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token,created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ContactView(APIView):
    def get(self, request, contact_id=None):
        if contact_id:
            contact = Contacts.objects.get(pk=contact_id)
            serializer = ContactSerializer(contact)
        else:
            contacts = Contacts.objects.all()
            serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, contact_id):
        contact = Contacts.objects.get(pk=contact_id)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, contact_id):
        contact = Contacts.objects.get(pk=contact_id)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
