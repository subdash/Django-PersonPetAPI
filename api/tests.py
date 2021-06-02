from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework.parsers import JSONParser
import io
import json

from .serializers import PersonSerializer, PetSerializer


def get_person_data():
    person_data = {
        "first_name": "Jesse",
        "last_name": "Sublett",
        "age": 67
    }

    return person_data


def get_pet_data(person_id):
    pet_data = {
        "name": "Iggy",
        "age": 5,
        "owner": person_id
    }

    return pet_data


def create_person(with_pets=False):
    serializer = PersonSerializer(data=get_person_data())
    serializer.is_valid()
    person = serializer.save()

    if with_pets:
        serializer = PetSerializer(
            data=get_pet_data(person.id)
        )
        serializer.is_valid()
        serializer.save()

    return person


def create_pet(owner_id):
    serializer = PetSerializer(data=get_pet_data(owner_id))
    serializer.is_valid()
    pet = serializer.save()

    return pet


###############################################################################
# /people/
###############################################################################
class PeopleTests(TestCase):
    def test_get_200_status_code(self):
        response = self.client.get(reverse('api:people'))
        self.assertIs(response.status_code, 200)

    def test_get_json_response_type(self):
        response = self.client.get(reverse('api:people'))
        self.assertIs(type(response), JsonResponse)

    def test_get_data_matches(self):
        person = create_person(with_pets=True)
        response = self.client.get(reverse('api:people'))
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        expected = {'people': [get_person_data()]}
        expected['people'][0]['id'] = person.id
        expected['people'][0]['pets'] = [get_pet_data(person.id)]
        expected['people'][0]['pets'][0]['id'] = \
            data['people'][0]['pets'][0]['id']

        self.assertEqual(data, expected)

    def test_post_200_status_code(self):
        response = self.client.post(reverse('api:people'),
                                    content_type='application/json',
                                    data=get_person_data())
        self.assertIs(response.status_code, 200)

    def test_post_json_response_type(self):
        response = self.client.post(reverse('api:people'),
                                    content_type='application/json',
                                    data=get_person_data())
        self.assertIs(type(response), JsonResponse)

    def test_post_data_matches(self):
        response = self.client.post(reverse('api:people'),
                                    content_type='application/json',
                                    data=get_person_data())
        expected = get_person_data()
        expected['id'] = json.loads(response.content.decode('utf-8'))['id']
        self.assertEqual(json.dumps(json.loads(response.content), sort_keys=True),
                         json.dumps(expected, sort_keys=True))

    def test_put_200_status_code(self):
        person = create_person()
        response = self.client.put(reverse('api:people'),
                                   content_type='application/json',
                                   data=model_to_dict(person))
        self.assertIs(response.status_code, 200)

    def test_put_json_response_type(self):
        person = create_person()
        response = self.client.put(reverse('api:people'),
                                   content_type='application/json',
                                   data=model_to_dict(person))
        self.assertIs(type(response), JsonResponse)

    def test_put_data_matches(self):
        person = create_person()
        person.first_name = "JESSE"
        response = self.client.put(reverse('api:people'),
                                   content_type='application/json',
                                   data=model_to_dict(person))
        expected = get_person_data()
        expected['first_name'] = "JESSE"
        expected['id'] = json.loads(response.content.decode('utf-8'))['id']
        self.assertEqual(json.dumps(json.loads(response.content), sort_keys=True),
                         json.dumps(expected, sort_keys=True))


###############################################################################
# /people/{id}/
###############################################################################
class PeopleDetailTests(TestCase):
    def test_get_200_status_code(self):
        person = create_person()
        response = self.client.get(f"/people/{person.id}/")
        self.assertEqual(response.status_code, 200)

    def test_get_301_status_code(self):
        person = create_person()
        response = self.client.get(f"/people/{person.id}")
        self.assertRedirects(response,
                             f"/people/{person.id}/",
                             status_code=301,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_get_404_status_code(self):
        response = self.client.get(f"/people/{9999}/")
        self.assertEqual(response.status_code, 404)

    def test_get_json_response_type(self):
        person = create_person()
        response = self.client.get(f"/people/{person.id}/")
        self.assertIs(type(response), JsonResponse)

    def test_get_data_matches(self):
        person = create_person()
        response = self.client.get(f"/people/{person.id}/")
        expected = {'person': get_person_data()}
        expected['person']['id'] = json.loads(response.content.decode('utf-8'))['person']['id']
        expected['person']['pets'] = []
        self.assertEqual(json.dumps(json.loads(response.content),
                                    sort_keys=True),
                         json.dumps(expected, sort_keys=True))

    def test_put_200_status_code(self):
        person = create_person()
        response = self.client.put(f"/people/{person.id}/",
                                   content_type='application/json',
                                   data=model_to_dict(person))
        self.assertIs(response.status_code, 200)

    def test_put_json_response_type(self):
        person = create_person()
        response = self.client.put(f"/people/{person.id}/",
                                   content_type='application/json',
                                   data=model_to_dict(person))
        self.assertIs(type(response), JsonResponse)

    def test_put_data_matches(self):
        person = create_person()
        person.first_name = "JESSE"
        response = self.client.put(f"/people/{person.id}/",
                                   content_type='application/json',
                                   data=model_to_dict(person))
        expected = get_person_data()
        expected['first_name'] = "JESSE"
        expected['id'] = json.loads(response.content.decode('utf-8'))['id']
        self.assertEqual(json.dumps(json.loads(response.content),
                                    sort_keys=True),
                         json.dumps(expected, sort_keys=True))


###############################################################################
# /pets/
###############################################################################
class PetTests(TestCase):
    def test_get_200_status_code(self):
        response = self.client.get(reverse('api:pets'))
        self.assertIs(response.status_code, 200)

    def test_get_json_response_type(self):
        response = self.client.get(reverse('api:pets'))
        self.assertIs(type(response), JsonResponse)

    def test_get_data_matches(self):
        person = create_person(with_pets=True)
        response = self.client.get(reverse('api:pets'))
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        pets = person.get_pets()
        pets_list = []
        for pet in pets:
            pet_dict = model_to_dict(pet)
            pet_dict['owner'] = model_to_dict(pet.owner)
            pets_list.append(pet_dict)

        expected = {'pets': pets_list}
        self.assertEqual(data, expected)

    def test_post_200_status_code(self):
        person = create_person(with_pets=True)
        expected = get_pet_data(person.id)
        response = self.client.post(reverse('api:pets'),
                                    content_type='application/json',
                                    data=expected)
        self.assertIs(response.status_code, 200)

    def test_post_json_response_type(self):
        person = create_person(with_pets=True)
        expected = get_pet_data(person.id)
        response = self.client.post(reverse('api:pets'),
                                    content_type='application/json',
                                    data=expected)
        self.assertIs(type(response), JsonResponse)

    def test_post_data_matches(self):
        person = create_person(with_pets=True)
        expected = get_pet_data(person.id)
        response = self.client.post(reverse('api:pets'),
                                    content_type='application/json',
                                    data=expected)
        expected['owner'] = model_to_dict(person)
        expected['id'] = json.loads(response.content.decode('utf-8'))['id']
        self.assertEqual(json.dumps(json.loads(response.content),
                                    sort_keys=True),
                         json.dumps(expected, sort_keys=True))

    def test_put_200_status_code(self):
        person = create_person(with_pets=True)
        pet = create_pet(person.id)
        expected = model_to_dict(pet)
        response = self.client.put(reverse('api:pets'),
                                   content_type='application/json',
                                   data=expected)
        self.assertIs(response.status_code, 200)

    def test_put_json_response_type(self):
        person = create_person(with_pets=True)
        pet = create_pet(person.id)
        expected = model_to_dict(pet)
        response = self.client.put(reverse('api:pets'),
                                   content_type='application/json',
                                   data=expected)
        self.assertIs(type(response), JsonResponse)

    def test_put_data_matches(self):
        person = create_person(with_pets=True)
        pet = create_pet(person.id)
        pet_dict = model_to_dict(pet)
        pet_dict['name'] = "Bingo"

        expected = model_to_dict(create_pet(person.id))
        expected['id'] = pet_dict['id']
        expected['name'] = "Bingo"
        expected['owner'] = model_to_dict(pet.owner)

        response = self.client.put(reverse('api:pets'),
                                   content_type='application/json',
                                   data=pet_dict)

        self.assertEqual(json.dumps(json.loads(response.content), sort_keys=True),
                         json.dumps(expected, sort_keys=True))


###############################################################################
# /pets/{id}/
###############################################################################
class PetDetailTests(TestCase):
    def test_get_200_status_code(self):
        person = create_person()
        pet = create_pet(person.id)
        response = self.client.get(f"/pets/{pet.id}/")
        self.assertEqual(response.status_code, 200)

    def test_get_301_status_code(self):
        person = create_person()
        pet = create_pet(person.id)
        response = self.client.get(f"/pets/{pet.id}")
        self.assertRedirects(response,
                             f"/pets/{pet.id}/",
                             status_code=301,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_get_404_status_code(self):
        response = self.client.get(f"/pets/{9999}/")
        self.assertEqual(response.status_code, 404)

    def test_get_json_response_type(self):
        person = create_person()
        pet = create_pet(person.id)
        response = self.client.get(f"/pets/{pet.id}/")
        self.assertIs(type(response), JsonResponse)

    def test_get_data_matches(self):
        person = create_person()
        pet = create_pet(person.id)
        response = self.client.get(f"/pets/{pet.id}/")
        expected = {"pet": get_pet_data(person.id)}
        expected['pet']['id'] = json.loads(response.content.decode('utf-8'))['pet']['id']
        expected['pet']['owner'] = model_to_dict(person)

        self.assertEqual(json.dumps(json.loads(response.content),
                                    sort_keys=True),
                         json.dumps(expected, sort_keys=True))

    def test_put_200_status_code(self):
        person = create_person()
        pet = create_pet(person.id)
        response = self.client.put(f"/pets/{pet.id}/",
                                   content_type='application/json',
                                   data=model_to_dict(pet))
        self.assertIs(response.status_code, 200)

    def test_put_json_response_type(self):
        person = create_person()
        pet = create_pet(person.id)
        response = self.client.put(f"/pets/{pet.id}/",
                                   content_type='application/json',
                                   data=model_to_dict(pet))
        self.assertIs(type(response), JsonResponse)

    def test_put_data_matches(self):
        person = create_person()
        pet = create_pet(person.id)
        response = self.client.put(f"/pets/",
                                   content_type='application/json',
                                   data=model_to_dict(pet))
        expected = get_pet_data(person.id)
        expected['id'] = json.loads(response.content.decode('utf-8'))['id']
        expected['owner'] = model_to_dict(person)

        self.assertEqual(json.dumps(json.loads(response.content),
                                    sort_keys=True),
                         json.dumps(expected, sort_keys=True))
