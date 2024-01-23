from urllib import response
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .models import book
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)


        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # token['waga'] = “baga”
        # ...


        return token




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class bookSerializer(serializers.ModelSerializer):
    class Meta:
        model = book
        fields = '__all__'
# Create your views here.

@api_view(['GET'])
def index(req):
    return Response('hello')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secret(req):
    return Response('secret')


@api_view(['GET','POST','DELETE','PUT','PATCH'])
def books(req,id=-1):
    if req.method =='GET':
        if id > -1:
            try:
                temp_task=book.objects.get(id=id)
                return Response (bookSerializer(temp_task,many=False).data)
            except book.DoesNotExist:
                return Response ("not found")
        all_tasks=bookSerializer(book.objects.all(),many=True).data
        return Response ( all_tasks)
    if req.method =='POST':
        tsk_serializer = bookSerializer(data=req.data)
        if tsk_serializer.is_valid():
            tsk_serializer.save()
            return Response ("post...")
        else:
            return Response (tsk_serializer.errors)
    if req.method =='DELETE':
        try:
            temp_task=book.objects.get(id=id)
        except book.DoesNotExist:
            return Response ("not found")    
       
        temp_task.delete()
        return Response ("del...")
    if req.method =='PUT':
        try:
            temp_task=book.objects.get(id=id)
        except book.DoesNotExist:
            return Response ("not found")
        print ("here")
        ser = bookSerializer(data=req.data)
        print(ser)
        old_task = book.objects.get(id=id)
        print(old_task)
        res = ser.update(old_task, req.data) 
        print(res)
        return Response("done")
