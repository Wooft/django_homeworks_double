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
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/courses/')
    data = response.json()
    assert len(data) == len(courses)
    assert courses[1].name == data[1]['name']
    #Проверка циклом что каждый из созданных курсов соотвествует результату выдачи из фильтра
    for i in range(10):
        res_filter = client.get(f'/courses/?id={i+1}')
        filter_data = res_filter.json()
        assert courses[i].name == filter_data[0]['name']
    #Проверка patch запроса
    patch_data = {
        'id': 1,
        'name': 'New_course'
    }
    patch_response = client.patch(path='/courses/1/', data=patch_data)
    assert patch_response.status_code == 200
    assert patch_data['name'] == Course.objects.get(id=1).name
    #Проверка удаления курса
    assert Course.objects.all().count() == 10
    response = client.delete('/courses/1/')
    assert response.status_code == 204
    assert Course.objects.all().count() == 9
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
def test_create_course(client):
    data = {
        'name': 'first_course'
    }
    response = client.post(path='/courses/', data=data)
    assert response.status_code == 201
    #Создаем курс с нужными данными, затем извлекаем его по ключу name из базы данных
    assert data['name'] == Course.objects.get(name=data['name']).name