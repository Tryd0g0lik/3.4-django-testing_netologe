from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_example():
    #Arrange
    clients = APIClient()

    #Act
    response = clients.get('/courses/')

    # Accert
    assert response.status_code == 200
    data = response.json()
    assert  len(data) == 0
    # assert True
