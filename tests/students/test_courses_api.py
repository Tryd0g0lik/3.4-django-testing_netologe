# from django.contrib.auth import get_user_model
import pytest
import random
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient
from model_bakery import baker
# import students.models
from students.models import *

@pytest.fixture
def api_client():
    return APIClient()

# fixture для фабрики курсов
@pytest.fixture
def stude():
    return baker.make(Course)

@pytest.fixture
def user():
    user = User.objects.create_user('admin')
    return user.id

@pytest.mark.django_db(
  databases='netology_django_testing',
  serialized_rollback=True,
)


def get_name_random():
  name = random.choice(
    ["Suraj", "Василенко",
     "Добрынин", "Magdum",
     "Avadhut", "More",
     "Rohit", "Chile",
     "Кнорриг", "Мухин", ]
    )
  return name

def get_courses_random():
  name = random.choice(
    [
      "Государственное и муниципальное управление",
      "Государственная служба РФ",
      "Теория и практика государственного управления",
      "Теория, практика и искусство управления",
      "Бизнес-элита и государственная власть: кто владеет Россией на стыке веков",
      "Публичная власть",
      "Государственное управление",
      "Государственная политика и управление",
    ]
  )
  return name


@pytest.mark.django_db()
def test_example(
  name_stude = get_name_random,
  title = get_courses_random,
  api_client = api_client
  ):

  # Arrange
  baker.make(
    "students.Student",
    name = name_stude,
 )

  baker.make(
    "students.Course",
     name = title,
    )

  # Act
  api_client = APIClient()

  response = api_client.get('/courses/')

  # Accert
  assert response.status_code == 200
  data = response.json()
  assert len(data[0]) != 0
  assert data


@pytest.mark.django_db()
def test_example_post(
  name_stude = get_name_random,
  title = get_courses_random,
  api_client = api_client,
  user_id = user
  ):
  api_client = APIClient()

  response = api_client.post('/courses/', data={
    'user' : user_id,
    'name' : title,
    'student' : name_stude,
  })

  # Accert
  assert response.status_code == 201
  assert Course.objects.count != 0

# @pytest.mark.django_db()
# def test_example_put(
#   name_stude=get_name_random,
#   title=get_courses_random,
#   api_client=api_client,
#   user_id=user
# ):
#   # Arrange
#   name_studes = baker.make(
#     "students.Student",
#     name=name_stude,
#   )
#
#   titles = baker.make(
#     "students.Course",
#     name=title,
#   )
#
#   api_client = APIClient()
#
#   student = api_client.put(
#     '/student/', data={
#       'user': user_id,
#       'name': name_studes,
#     }
#   )
#   cours = api_client.post(
#     '/courses/', data={
#     'user': user_id,
#     'name': titles,
#     'student': name_studes.id,
#     }
#   )
#
#   old_data = student.get(pk=0)
#   response = api_client.put(
#     '/student/', data={
#       old_data : 'PUT_request',
#     }
#   )
#
#
#
#   # Accert
#   assert response.status_code == 204
#   assert print(response)
#   # assert Course.objects.count != 0