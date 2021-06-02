from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from rest_framework.parsers import JSONParser
import io

from .models import Person, Pet

from .serializers import PersonSerializer, PetSerializer


@require_GET
def index(request):
    return JsonResponse({"endpoints": [
        "people/",
        "pets/"
    ]})


@require_http_methods(['GET', 'POST', 'PUT'])
@csrf_exempt
def people(request):
    if request.method == 'GET':
        people_query = Person.objects.all()
        people_list = []
        for p in people_query:
            person_and_pets = model_to_dict(p)
            person_and_pets['pets'] = [model_to_dict(pet) for pet in p.get_pets()]
            people_list.append(person_and_pets)

        return JsonResponse({"people": people_list})

    elif request.method == 'POST':
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        serializer = PersonSerializer(data=data)
        serializer.is_valid()
        person = serializer.save()

        return JsonResponse(model_to_dict(person))

    elif request.method == 'PUT':
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        person = Person.objects.get(pk=data['id'])

        serializer = PersonSerializer(person, data=data, partial=True)
        serializer.is_valid()
        validated_data = serializer.validated_data
        person = serializer.update(person, validated_data)

        return JsonResponse(model_to_dict(person))


@require_http_methods(['GET', 'PUT'])
def person_detail(request, person_id):
    if request.method == 'GET':
        try:
            person = Person.objects.get(pk=person_id)
        except Person.DoesNotExist:
            raise Http404("Person does not exist")

        person_dict = model_to_dict(person)
        person_dict['pets'] = [model_to_dict(pet) for pet in person.get_pets()]

        return JsonResponse({"person": person_dict})

    elif request.method == 'PUT':
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        person = Person.objects.get(pk=person_id)

        serializer = PersonSerializer(person, data=data, partial=True)
        serializer.is_valid()
        validated_data = serializer.validated_data
        person = serializer.update(person, validated_data)

        return JsonResponse(model_to_dict(person))


@require_http_methods(['GET', 'POST', 'PUT'])
@csrf_exempt
def pets(request):
    if request.method == 'GET':
        pets_query = Pet.objects.all()
        pets_list = []
        for pet in pets_query:
            pet_dict = model_to_dict(pet)
            pet_dict['owner'] = model_to_dict(pet.owner)
            pets_list.append(pet_dict)

        return JsonResponse({"pets": pets_list})

    elif request.method == 'POST':
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        serializer = PetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        pet = serializer.save()
        pet_dict = model_to_dict(pet)
        pet_dict['owner'] = model_to_dict(pet.owner)

        return JsonResponse(pet_dict)

    elif request.method == 'PUT':
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        pet = Pet.objects.get(pk=data['id'])

        serializer = PetSerializer(pet, data=data, partial=True)
        serializer.is_valid()
        validated_data = serializer.validated_data
        pet = serializer.update(pet, validated_data)
        pet_dict = model_to_dict(pet)
        pet_dict['owner'] = model_to_dict(pet.owner)

        return JsonResponse(pet_dict)


@require_http_methods(['GET', 'PUT'])
def pet_detail(request, pet_id):
    if request.method == 'GET':
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            raise Http404("Pet does not exist")

        pet_dict = model_to_dict(pet)
        pet_dict['owner'] = model_to_dict(pet.owner)

        return JsonResponse({"pet": pet_dict})

    elif request.method == 'PUT':
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        pet = Pet.objects.get(pk=pet_id)

        serializer = PetSerializer(pet, data=data, partial=True)
        serializer.is_valid()
        validated_data = serializer.validated_data
        pet = serializer.update(pet, validated_data)
        pet_dict = model_to_dict(pet)
        pet_dict['owner'] = model_to_dict(pet.owner)

        return JsonResponse(pet_dict)
