

from functools import partial
from django.shortcuts import render
from .models import Notes,User
from .serializers import Noteserialiser,Userserializer
# Create your views here.

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
import jwt
from datetime import datetime,date,timedelta
import json


     
class RegisterView(APIView):
    def post(self,request):
        serializer=Userserializer(data=request.data) 
        if(serializer.is_valid()):

            serializer.save()
        else:
            return Response({"error":"User with this email or password already exists"})    
        return Response({"ok":"Successfully Registered"})

class LoginView(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']

        user=User.objects.filter(email=email).first()

        if(user is None):
            return Response({"error":"No such user"})

        if(not user.check_password(password)):
            return Response({"error":"Invalid password"})

        payload={
            'id':user.id,
            'exp':datetime.utcnow() + timedelta(minutes=540),
            'iat':datetime.utcnow()
        }    
        
        token=jwt.encode(payload,'secret',algorithm='HS256')
        response=Response()
        
        response.data={
            'jwt':token,
            'id':user.id
        }
        return response
 
class UserView(APIView):
    def post(self,request):
        token=request.data["token"]
        uid=int(request.data["id"])
     
        print(type(token),request.data["id"])
        

        if(not token):
            raise AuthenticationFailed("UnAuthenticated")

        try:
            payload=jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("UnAuthenticated")        

        user=User.objects.filter(id=uid).first()
       # print(user)
        serializer=Userserializer(user)
        note=Notes.objects.filter(user=uid)  
        print(note) 
       
        s2=Noteserialiser(note,many=True)
      
        return Response(s2.data)      

class UserLogout(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.delete_cookie('id')
        response.data={
            'message':'succesfully logged out'
        }
        return response


class Addnote(APIView):
    def post(self,request):
       
        jdata=request.data    
        serializer=Noteserialiser(data=jdata)
        serializer.is_valid(raise_exception=True)


        serializer.save()
       
        user=User.objects.filter(id=request.data.get("user")).first()
       # print(user)
        
        note=Notes.objects.filter(user=user)  
        
       
        s2=Noteserialiser(note,many=True) 
        print(s2.data)
        return Response(s2.data)        


class Updatenote(APIView):
    def post(self,request,pk):
        uid=int(request.data["id"])

        if(not uid):
            raise AuthenticationFailed("Session expired ..plz log in again")        
        

        user=User.objects.filter(id=uid).first() 
        note=Notes.objects.filter(user=user)  
        
       
        s2=Noteserialiser(note,many=True)
        print(s2.data)
        return Response(s2.data)     


    def patch(self,request,pk,format=None):
        
        uid=int(request.data["id"])
        

        if(not uid):
            raise AuthenticationFailed("Session expired ..plz log in again")        


        
        user=User.objects.filter(id=uid).first() 
        serializer=Userserializer(user)
        note=Notes.objects.filter(user=user).get(id=pk) 
          
         
        serializer=Noteserialiser(note,data=request.data,partial=True)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        note=Notes.objects.filter(user=user)  
        
       
        s2=Noteserialiser(note,many=True) 
        print(s2.data)
        return Response(s2.data)   


class Deletenote(APIView):
    def delete(self,request,pk):
       

        uid=int(request.data["userid"])
        

        


        user=User.objects.filter(id=uid).first() 
        serializer=Userserializer(user)
        note=Notes.objects.filter(user=user).get(id=pk)
        if(note is None):
            raise AuthenticationFailed("No such note")
        print(note)
        note.delete()
        
        note=Notes.objects.filter(user=user)  
        
       
        s2=Noteserialiser(note,many=True) 
        print(s2.data)
        return Response(s2.data)   
    

class test(APIView):
    def get(self,request):
        user=User.objects.all()
        ser=Userserializer(user,many=True) 

        return Response(ser.data)          