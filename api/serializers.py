from rest_framework import serializers
from django.db import models

from .models import Person, Pet


class PersonSerializer(serializers.ModelSerializer):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    age = models.IntegerField(default=0)

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        Person.objects.filter(pk=instance.id).update(**validated_data)

        return Person.objects.get(pk=instance.id)

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'age')


class PetSerializer(serializers.ModelSerializer):
    name = models.CharField(max_length=32)
    age = models.IntegerField(default=0)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

    def create(self, validated_data):
        return Pet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        Pet.objects.filter(pk=instance.id).update(**validated_data)

        return Pet.objects.get(pk=instance.id)

    class Meta:
        model = Pet
        fields = ('name', 'age', 'owner')
