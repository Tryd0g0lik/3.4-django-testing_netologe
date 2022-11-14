# from django.contrib.auth import get_user_model
import pytest
import random
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient # The client with the goal  refers to the model
from model_bakery import baker # The app for generation content, for what would  be testing models
# import students.models
from students.models import *
from students.serializers import StudentSerializer


@pytest.fixture #  the pytest.fixture creates attribute from repeatedly code
def api_client():
    return APIClient()

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
) # Run the module 'model_bakery'


def get_name_random():
  # -----------------
  # The list of students name
  # -----------------
  name = random.choice(
    ["Suraj", "Василенко",
     "Добрынин", "Magdum",
     "Avadhut", "More",
     "Rohit", "Chile",
     "Кнорриг", "Мухин", ]
    )
  return name

def get_courses_random():
  # -----------------
  # The list of courses titles
  # -----------------
  name = random.choice(
    [
      "Государственное и муниципальное управление",
      "Государственная служба РФ",
      "Теория и практика государственного управления",
      "Теория, практика и искусство управления",
      "Бизнес-элита и государственная власть: кто владеет\n"
      " Россией на стыке веков",
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
  """
  # -----------------
  # Tha app for testing app
  TODO: The function tests getting data for db
  :param name_stude: this's list the names-students
  :param title:
  :param api_client:
  :return: must be the cod 200
  """

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
  # Arrange
  name_stude = get_name_random,
  title = get_courses_random,
  api_client = api_client,
  user_id = user
  ):
  """
    # -----------------
    # The app for testing
    TODO: test creates data for a db
    :param name_stune it's firstname student
    :param title it's course title
    :params api_client it's client (type the browser, app) then accessing to db
    :return must be return the 201 code
    # -----------------
  """
  api_client = APIClient()

  # Act

  response = api_client.post('/courses/', data={
    'user' : user_id,
    'name' : title,
    'student' : name_stude,
  })

  # Accert
  assert response.status_code == 201
  assert Course.objects.count != 0


id_course = 2
@pytest.mark.django_db()
def test_filtr_list_courses(
  name_stude : list = get_name_random,
  title : list = get_courses_random,
  api_client = api_client,
  id_course : int = id_course,
  ):
  """
  :param name_stude: this's list the names-students
  :param title:
  :param api_client:
  :return:
  """

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
  # title_courseId = Course.objects.get(id = id_course)
  # name_student = Student.objects.get(course_id = id_course)
  # id_student = Course.objects.get(id = id_course)
  # response_name_student = Student.objects.get('id').all()
  # response_student =StudentSerializer(response_name_student)
  # print("1: ", api_client(response_name_student, response_student))
  response_id_course = Course.objects.filter(id = 1).first()
  response_page = api_client.get(f'api/v1/courses/%s/' % (response_id_course, ))
  #
  # response = api_client.get(response_page, response_name_student)
  # print(f"response_page: {response_name_student}")

  r = {"f": '220'}
  # Accert
  # assert r
  assert response_page.status_code == 200
  data = response_page.json()
  assert len(data[0]) != 0
  assert data