from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    age = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} " + \
               f"(Age: {self.age})"

    def get_pets(self):
        pets = Pet.objects.filter(owner_id=self.id)
        return pets


class Pet(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField(default=0)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Age: {self.age})"
