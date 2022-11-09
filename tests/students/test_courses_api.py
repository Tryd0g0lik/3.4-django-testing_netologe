# from django.contrib.auth import get_user_model
import pytest
import random
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient
from model_bakery import baker
# import students.models
from students.models import Course, Student, Faculty


@pytest.fixture
def api_client():
    return APIClient()


# fixture для фабрики курсов
@pytest.fixture
def stude():
    return baker.make(Course)


@pytest.fixture
def getUser():
    return User.objects.create_user('admin')


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
  username = getUser,
  api_client = api_client
  ):
#Arrange
  student = baker.make(
    "students.Student",
    name = name_stude,
    # _quantity = 3,
 )


  title_course = baker.make(
    "students.Course",
     name = title,
    )


  # Student.objects.create(
  #   # get_user=username ,
  #   name=student.name,
  # )

  # User.objects.filter(name = )

  # Course.objects.create(
  #   student = username,
  #   name = title_course.name,
  #   make_m2m=True
  # )

  # faculty = baker.make(
  #   "students.Faculty",
  #
  # )

  # Faculty.objects.create(
  # student = Student.student.id,
  # course = Course.course.id,
  # )

  #Act


  api_client = APIClient()

  # response = api_client.post(
  #   '/courses/',
  #   name=Student.name,
  # )
  response = api_client.get('/courses/')

  # Accert
  assert response.status_code == 200
  data = response.json()
  assert len(data[0]) != 0
  assert data
  # assert True

