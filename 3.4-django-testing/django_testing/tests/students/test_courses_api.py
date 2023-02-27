import pprint

import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_get_single_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.get('/courses/')
    data = response.json()
    assert len(data) == len(courses)
    assert courses[0].name == data[0]['name']


@pytest.mark.django_db
def test_get_list_of_sourses(client, course_factory):
    courses = course_factory(_quantity=10)
    #Проверка циклом что каждый из созданных курсов соотвествует результату выдачи из фильтра
    response = client.get('/courses/')
    data = response.json()
    pprint.pprint(data)
    for i in range(10):
        assert courses[i].name == data[i]['name']


@pytest.mark.django_db
def test_patch_courses(client, course_factory):
    # #Проверка patch запроса
    course = course_factory()
    patch_data = {
        'id': course.pk,
        'name': 'test_patch_data'
    }
    patch_response = client.patch(path=f'/courses/{patch_data["id"]}/', data=patch_data)
    assert patch_response.status_code == 200
    assert patch_data['name'] == Course.objects.get(id=patch_data['id']).name


#   #Проверка удаления курса
@pytest.mark.django_db
def test_remove_sourse(client, course_factory):
    count_courses = Course.objects.all().count()
    course = course_factory()
    del_response = client.delete(path=f'/courses/{course.pk}/')
    assert del_response.status_code == 204
    assert Course.objects.all().count() == count_courses


@pytest.mark.django_db
def test_get_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    #Для всех курсов из созданных, проводим проверку:
    #ФИльтруем по имени первого курса их списка и сравниваем полученный результат выдачи с переданным курсом
    for i in range(10):
        response = client.get(f'/courses/?name={courses[i].name}')
        data = response.json()
        assert data[0]['name'] == courses[i].name

@pytest.mark.django_db
def test_get_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    #Для всех курсов из созданных, проводим проверку:
    #ФИльтруем по id первого курса их списка и сравниваем полученный результат выдачи с переданным курсом
    for i in range(10):
        response = client.get(f'/courses/?id={courses[i].pk}')
        data = response.json()
        assert data[0]['name'] == courses[i].name


@pytest.mark.django_db
def test_create_course(client):
    data = {
        'name': 'first_course'
    }
    response = client.post(path='/courses/', data=data)
    assert response.status_code == 201
    #Создаем курс с нужными данными, затем извлекаем его по ключу name из базы данных
    assert data['name'] == Course.objects.get(name=data['name']).name