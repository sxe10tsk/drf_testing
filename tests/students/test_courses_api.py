import pytest
from rest_framework.test import APIClient
from students.models import Student, Course
from model_bakery import baker


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_course(client, course_factory):
    courses = course_factory()
    url = f'/courses/{courses.id}/'

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses.name


@pytest.mark.django_db
def test_course_list(client, course_factory):
    courses = course_factory(_quantity=10)
    url = f'/courses/'

    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, k in enumerate(data):
        assert k['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    courses = course_factory(_quantity=10)
    url = f'/courses/?id={courses[5].id}'

    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == courses[5].id
    assert data[0]['name'] == courses[5].name


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)
    url = f'/courses/?name={courses[5].name}'

    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == courses[5].id
    assert data[0]['name'] == courses[5].name


@pytest.mark.django_db
def test_course_creation(client):
    url = f'/courses/'
    post_data = {'name': 'Scientology'}

    response = client.post(url, data=post_data)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Scientology'
    assert Course.objects.filter(id=data["id"], name="Scientology").exists()


@pytest.mark.django_db
def test_course_update(client, course_factory):
    courses = course_factory()
    url = f'/courses/{courses.id}/'

    response = client.patch(url, data={'name': 'art'})

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'art'
    assert Course.objects.filter(id=data["id"], name="art").exists()


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    courses = course_factory()
    url = f'/courses/{courses.id}/'

    response = client.delete(url)

    assert response.status_code == 204


