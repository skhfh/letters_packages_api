import pytest
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from packages.models import Package


@pytest.mark.django_db
def test_create_package(
        url_packages, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: создание посылки через API (POST)."""
    data = {
        'sender': client_1.id,
        'recipient': client_2.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_2.id,
        'category': 1,
        'cost': 100
    }

    response = api_client.post(url_packages, data, format='json')
    assert response.status_code == HTTP_201_CREATED
    assert Package.objects.count() == 1
    assert len(response.data) == 10
    assert response.data['sender'] == client_1.full_name
    assert response.data['recipient'] == client_2.full_name
    assert response.data['departure_office'] == post_office_1.address
    assert response.data['arrival_office'] == post_office_2.address
    assert response.data['departure_index'] == post_office_1.postal_index
    assert response.data['phone_number'] == client_2.phone_number
    assert response.data['category'] == 'Мелкий пакет'
    assert response.data['cost'] == 100


@pytest.mark.django_db
def test_create_package_wrong_category(
        url_packages, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: создание посылки с типом посылки (category) вне вариантов выбора
    должно вернуть ошибку валидации."""
    data = {
        'sender': client_1.id,
        'recipient': client_2.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_2.id,
        'category': 20,
        'cost': 100
    }

    response = api_client.post(url_packages, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert 'category' in response.data


@pytest.mark.django_db
def test_create_package_wrong_cost(
        url_packages, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: создание посылки с отрицательной стоимостью
    должно вернуть ошибку валидации."""
    data = {
        'sender': client_1.id,
        'recipient': client_2.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_2.id,
        'category': 3,
        'cost': -100
    }

    response = api_client.post(url_packages, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert 'cost' in response.data


@pytest.mark.django_db
def test_create_package_same_sender_and_recipient(
        url_packages, api_client, client_1, post_office_1, post_office_2,
):
    """Тест: создание посылки с одним и тем же отправителем и получателем
    должно вернуть ошибку валидации."""
    data = {
        'sender': client_1.id,
        'recipient': client_1.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_2.id,
        'category': 3,
        'cost': 250
    }

    response = api_client.post(url_packages, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert 'Отправитель и получатель должны быть разные' in str(response.data)


@pytest.mark.django_db
def test_create_package_same_departure_office_and_arrival_office(
        url_packages, api_client, client_1, client_2, post_office_1,
):
    """Тест: создание посылки с одинаковыми пунктами отправления и получения
    должно вернуть ошибку валидации."""
    data = {
        'sender': client_1.id,
        'recipient': client_2.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_1.id,
        'category': 3,
        'cost': 250
    }

    response = api_client.post(url_packages, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert ('Пункты отправления и получения должны быть разные'
            in str(response.data))


@pytest.mark.django_db
def test_create_package_without_required_fields(
        url_packages, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: создание посылки без передачи всех требуемых аргументов."""
    data = {}

    response = api_client.post(url_packages, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    expected_fields = {'category',
                       'recipient',
                       'departure_office',
                       'arrival_office',
                       'category',
                       'cost'}
    assert expected_fields.issubset(response.data.keys())


@pytest.mark.django_db
def test_get_list_package(
        url_packages, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: получение списка посылок (GET)."""
    Package.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        cost=123
    )
    Package.objects.create(
        sender=client_2,
        recipient=client_1,
        departure_office=post_office_2,
        arrival_office=post_office_1,
        category=1,
        cost=55
    )

    response = api_client.get(url_packages)

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_one_obj_package(
        url_packages, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: получение конкретной посылки (GET)."""
    letter = Package.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        cost=123
    )

    url = f'{url_packages}{letter.id}/'
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 10
    assert response.data['sender'] == client_1.full_name
    assert response.data['recipient'] == client_2.full_name
    assert response.data['departure_office'] == post_office_1.address
    assert response.data['arrival_office'] == post_office_2.address
    assert response.data['departure_index'] == post_office_1.postal_index
    assert response.data['phone_number'] == client_2.phone_number
    assert response.data['category'] == letter.get_category_display()
    assert response.data['cost'] == letter.cost


@pytest.mark.django_db
def test_get_non_existing_package(url_packages, api_client):
    """Тест: запрос несуществующей посылки должен вернуть 404."""
    url = f'{url_packages}777/'
    response = api_client.get(url)

    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_put_update_package(
        url_packages, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: полное изменение конкретной посылки (PUT)."""
    letter = Package.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        cost=123
    )

    url = f'{url_packages}{letter.id}/'
    new_data = {
        'sender': client_2.id,
        'recipient': client_1.id,
        'departure_office': post_office_2.id,
        'arrival_office': post_office_1.id,
        'category': 4,
        'cost': 25
    }
    response = api_client.put(url, new_data, format='json')
    letter.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert letter.sender == client_2
    assert letter.recipient == client_1
    assert letter.departure_office == post_office_2
    assert letter.arrival_office == post_office_1
    assert letter.category == new_data['category']
    assert letter.cost == new_data['cost']


@pytest.mark.django_db
def test_patch_update_package(
        url_packages, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: частичное обновление конкретной посылки (PATCH)."""
    letter = Package.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        cost=123
    )

    url = f'{url_packages}{letter.id}/'
    patch_data = {'category': 5}
    response = api_client.patch(url, patch_data, format='json')
    letter.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert letter.category == patch_data['category']


@pytest.mark.django_db
def test_delete_package(
        url_packages, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: удаление конкретной посылки (DELETE)."""
    letter = Package.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        cost=123
    )

    url = f'{url_packages}{letter.id}/'
    response = api_client.delete(url)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert not Package.objects.filter(id=letter.id).exists()
