# from django.contrib.auth import get_user_model
import pytest
import requests
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


@pytest.fixture
def content_for_testing():
  def testing(model: str, name: list, m2m: bool = False, **kwargs):
    """
    TODO: It's  creating the data for table of db and working test. When content line went the test, she will be
    deleted
    :param name: It's list of 'get_courses_random' def or 'get_name_random'
    :param model: The name model of app. It's type row.
    :param m2m: it's type relationship the many-to-many or not.
    :param kwargs:
    :return:
    """
    return baker.make(model=model,
                       name=name,
                       make_m2m=m2m
                       )
  return testing


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
    name=name_stude,
    make_m2m=True
  )
  print("333")
  baker.make(
    "students.Course",
    name=title,
  )

  # Act
  api_client = APIClient()

  response = api_client.get('/courses/')

  # Accert
  assert response.status_code == 200
  data = response.json()
  assert len(data[0]) != 0
  assert data

name_stude = None
title = None
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


name_stude = None
title = None
@pytest.mark.django_db()
def test_filtr_by_name(
  name_stude : list = get_name_random,
  title : list = get_courses_random,
  api_client = api_client,
  db_id = 1,
  db_content=content_for_testing
  ):
  """
  TODO: Checking filtering by name
  :param name_stude: this's list the names-students
  :param title: It's course name
  :param api_client: id's student id line of db
  :param id_course: it's course  id line of db
  :return:
  """

  # Arrange
  print("000")
  # db_content(
  #   model="students.Course",
  #   m2m=True,
  #   name=title,
  #   ) #  creating the data for table of db
  print("111")
  # db_content(
  #   model="students.Student",
  #   name=name_stude,
  #   )
  print("222")

  baker.make(
    "students.Student",
    name=name_stude,
    make_m2m=True
  )
  print("333")
  baker.make(
    "students.Course",
    name=title,
  )
  # Act
  print("444")
  api_client = APIClient()

  for r in Student.objects.all(): print("444-111", r.id, end=" ")
  print("555")
  params={'name' : '%s' % (r)}
  print("6666", params)
  response_page = api_client.get('/courses/', data=params)
  print("777")

  # Accert
  assert response_page.status_code == 200
  data = response_page.json()
  assert len(data[0]) != 0
  assert data

name_stude = None
title = None
@pytest.mark.django_db()
def test_filtr_by_id(
  name_stude : list = get_name_random,
  title : list = get_courses_random,
  api_client = api_client,
  id_course : int = 1,
  ):
  """
  TODO: Checking filtering by id
  :param name_stude: this's list the names-students
  :param title:
  :param api_client:
  :return:
  """

  # Arrange
  baker.make(
    "students.Student",
    name = name_stude,
    make_m2m=True
 )

  baker.make(
    "students.Course",
     name = title,
    )

  # Act
  api_client = APIClient()
  # response_id_course = Course.objects.filter(id  = 1)
  for r in Course.objects.all() : i = r.id

  print(f"i: {i}")
  params={'id' : '%s' % (i, )}
  print(f"params: {params}")
  response_page = api_client.get('/courses/%s/' % (i,))
  print(f"response_page: {response_page.json()}")

  assert response_page.status_code == 200
  data = response_page.json()
  assert len(data)
  assert data

name_stude = None
title = None
@pytest.mark.django_db()
def test_post(

  name_stude = get_name_random,
  title = get_courses_random,
  api_client = api_client,
  user_id = user
  ):
  """
    # -----------------
    # The app for testing
    TODO:
    :param name_stune it's firstname student
    :param title it's course title
    :params api_client it's client (type the browser, app) then accessing to db
    :return must be return the 201 code
    # -----------------
  """
  # Arrange
  params_student = {
    'name' : 'RRRRRRRR'

  }

  params_courses = {
    'name': 'fffffffffffffffffffff',
    'student': 0,
  }

  api_client = APIClient()

  # Act

  response_st = api_client.post('/student/', data=params_student)
  response_cour = api_client.post('/courses/', data=params_courses)

  # Accert
  assert response_st.status_code == 201
  assert Student.objects.count != 0
  assert response_cour.status_code == 201
  assert Course.objects.count != 0

name_stude = None
title = None
@pytest.mark.django_db()
def test_post_put(
  # Arrange
  name_stude = get_name_random,
  title = get_courses_random,
  api_client = api_client,
  user_id = user
  ):
  """
    # -----------------
    # The app for testing
    TODO: tests the POST request (with data-db from 'model_bakery')  \n
     and a PUT request by customising data without 'model_bakery'
    :param name_stune it's firstname student
    :param title it's course title
    :params api_client it's client (type the browser, app) then accessing to db
    :return must be return the 201, 200 code
    # -----------------
  """
  api_client = APIClient()

  # Act

  # Arrange
  baker.make(
    "students.Student",
    name=name_stude,
  )

  baker.make(
    "students.Course",
    name=title,
  )
  for r in Course.objects.filter() : i = r.id
  response_put  = api_client.put('/courses/%s/' % (i,), data={
    'name' : "YYYYYYYYYYYYYYYYYYYYYYYYY",
    'student' : "kiki",
  })


  # Accert

  assert Course.objects.count != 0
  assert response_put.status_code == 200

name_stude = None
title = None
@pytest.mark.django_db()
def test_delete(
  # Arrange
  name_stude=get_name_random,
  title=get_courses_random,

  id=1
):

  # Arrange
  baker.make(
    "students.Student",
    name=name_stude,

  )

  baker.make(
    "students.Course",
    name=title,
    make_m2m=True
  )
  api_client = APIClient()
  respons_delete = api_client.delete('/courses/%s' % (id,))
  # Accert
  assert respons_delete.status_code == 301

