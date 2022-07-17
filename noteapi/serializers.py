from dataclasses import fields
from rest_framework import serializers

from .models import Notes,User


class Noteserialiser(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=['id','title','description','tag','date','user'] 
        


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','password','date_joined']
        
        extra_kwargs={'write_only':True}

    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)

        if(password is not None):
            instance.set_password(password) 
        instance.save()
        return instance      
