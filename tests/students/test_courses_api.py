from pprint import pprint

import pytest

import random
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient # The client with the goal  refers to the model
from model_bakery import baker # The app for generation content, for what would  be testing models
from students.models import *


@pytest.fixture(scope='package' ) #  the pytest.fixture creates attribute from repeatedly code
def api_client():
  def factory():
    return APIClient
  return factory


@pytest.fixture
def user():
  def factory():
      user = User.objects.create_user('admin')
      return user.id
  return factory

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


def post_studet_db():
  """
  TODO: This's fixture creating data-base from Student name
  :return: def factory for db generation when each calling
  """
  _mak = baker.make(
    "students.Student",
    name = get_name_random,
  )
  return _mak


def post_course_db():
  """
  TODO: This's fixture creating data-base from Student name
  :return: def factory for db generation when each calling
  """
  _mak = baker.make(
    "students.Course",
    name = get_courses_random,
    make_m2m=True
    )
  return _mak

@pytest.fixture(scope='session')
def get_id_first_course():
  def factory():
    _first_course = Course.objects.first()
    return _first_course.id
  return factory


@pytest.mark.django_db()
def test_example(
  studen=post_studet_db,
  courses=post_course_db,
  api_client = api_client,
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
  _studen = studen()
  _courses = courses()

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
  studen=post_studet_db,
  courses=post_course_db,
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

  _studen = studen()
  _courses = courses()

  api_client = APIClient()

  _ferst_cours = Course.objects.first()
  # Act

  response = api_client.post('/courses/', data={
    'user' : "%s" % (user_id,),
    'name' : "%s" % (_ferst_cours.name,),
    'student' : "%s" % (_ferst_cours.student,),
  })

  # Accert
  assert response.status_code == 201
  assert Course.objects.count != 0



@pytest.mark.django_db()
def test_filtr_by_name(
  studen=post_studet_db,
  courses=post_course_db,
  api_client=api_client,
  user=user,
  _course_id = get_id_first_course,
  ):
  """
  TODO: Checking filtering by name
  :param name_stude: this's list the names-students
  :param title:
  :param api_client:
  :return:
  """
  # Arrange
  _studen = studen()
  _courses = courses()

  # Act
  # t = []
  # c = Course.objects.get(id=_course_id)
  # t.append([r for r in c])

  # if t != [] or t != [[]]:

  response_id_course = Course.objects.first()

  api_client = APIClient()
  params={'name' : "%s" % (response_id_course.name,)}
  response_page = api_client.get('/courses/', data=params)

  # Accert
  assert response_page.status_code == 200
  data = response_page.json()
  assert len(data[0]) != 0
  assert data

  # else:
  #   assert 2 == 1


@pytest.mark.django_db()
def test_filtr_by_id(
  studen=post_studet_db,
  courses=post_course_db,
  _course_id = get_id_first_course,
  ):
  """
  TODO: Checking filtering by id
  :param name_stude: this's list the names-students
  :param title:
  :param api_client:
  :return:
  """

  # Arrange
  _studen = studen()
  _courses = courses()

  # Act
  _api_client = APIClient()


  params={'id' : '%s/' % (_course_id, )}
  response_page = _api_client.get('/courses/', data=params)


  assert response_page.status_code == 200
  data = response_page.json()
  assert len(data[0]) != 0
  assert data


@pytest.mark.django_db()
def test_post(
  name = get_name_random,
  title = get_courses_random,
  _course_id = get_id_first_course,
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
    'name' : "%s" % (name,),

  }


  api_client = APIClient()

  # Act

  response_st = api_client.post('/student/', data=params_student)


  params_courses = {
    'name': "%s" % (title,),
    'student': "%s" % (_course_id,),
  }
  response_cour = api_client.post('/courses/', data=params_courses)

  # Accert
  assert response_st.status_code == 201
  assert Student.objects.count != 0
  assert response_cour.status_code == 201
  assert Course.objects.count != 0


@pytest.mark.django_db()
def test_post_put(
  # Arrange
  studen=post_studet_db,
  courses=post_course_db,
  name = get_name_random,
  title = get_courses_random,
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
  _studen = studen()
  _courses = courses()
  _course = Course.objects.first()

  response_put  = api_client.put(f'/courses/{_course.id}/', data={
    'id' : "%s" %(_course.id,),
    'name' : "%s" % (title,),
    'student' : "%s" % (name,),
  })


  # Accert

  assert Course.objects.count != 0
  assert response_put.status_code == 200


@pytest.mark.django_db()
def test_delete(
  # Arrange
  studen=post_studet_db,
  courses=post_course_db,
  _course_id = get_id_first_course
):

  # Arrange
  _student = studen()
  _courses = courses()

  # _title =

  api_client = APIClient()
  respons_delete = api_client.delete('/courses/%s' % (_course_id,))
  # Accert
  assert respons_delete.status_code == 301

