import pytest
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from packages.models import Letter


@pytest.mark.django_db
def test_create_letter(
        url_letters, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: создание письма через API (POST)."""
    data = {
        'sender': client_1.id,
        'recipient': client_2.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_2.id,
        'category': 1,
        'weight': 100
    }

    response = api_client.post(url_letters, data, format='json')
    assert response.status_code == HTTP_201_CREATED
    assert Letter.objects.count() == 1
    assert len(response.data) == 9
    assert response.data['sender'] == client_1.full_name
    assert response.data['recipient'] == client_2.full_name
    assert response.data['departure_office'] == post_office_1.address
    assert response.data['arrival_office'] == post_office_2.address
    assert response.data['departure_index'] == post_office_1.postal_index
    assert response.data['category'] == 'Письмо'
    assert response.data['weight'] == 100


@pytest.mark.django_db
def test_create_letter_wrong_category(
        url_letters, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: создание письма с типом письма (category) вне вариантов выбора
    должно вернуть ошибку валидации."""
    data = {
        'sender': client_1.id,
        'recipient': client_2.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_2.id,
        'category': 10,
        'weight': 100
    }

    response = api_client.post(url_letters, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert 'category' in response.data


@pytest.mark.django_db
def test_create_letter_wrong_weight(
        url_letters, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: создание письма с отрицательным весом
    должно вернуть ошибку валидации."""
    data = {
        'sender': client_1.id,
        'recipient': client_2.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_2.id,
        'category': 3,
        'weight': -100
    }

    response = api_client.post(url_letters, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert 'weight' in response.data


@pytest.mark.django_db
def test_create_letter_same_sender_and_recipient(
        url_letters, api_client, client_1, post_office_1, post_office_2,
):
    """Тест: создание письма с одним и тем же отправителем и получателем
    должно вернуть ошибку валидации."""
    data = {
        'sender': client_1.id,
        'recipient': client_1.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_2.id,
        'category': 3,
        'weight': 250
    }

    response = api_client.post(url_letters, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert 'Отправитель и получатель должны быть разные' in str(response.data)


@pytest.mark.django_db
def test_create_letter_same_departure_office_and_arrival_office(
        url_letters, api_client, client_1, client_2, post_office_1,
):
    """Тест: создание письма с одинаковыми пунктами отправления и получения
    должно вернуть ошибку валидации."""
    data = {
        'sender': client_1.id,
        'recipient': client_2.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_1.id,
        'category': 3,
        'weight': 250
    }

    response = api_client.post(url_letters, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert ('Пункты отправления и получения должны быть разные'
            in str(response.data))


@pytest.mark.django_db
def test_create_letter_without_required_fields(
        url_letters, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: создание письма без передачи всех требуемых аргументов."""
    data = {}

    response = api_client.post(url_letters, data, format='json')

    assert response.status_code == HTTP_400_BAD_REQUEST
    expected_fields = {'category',
                       'recipient',
                       'departure_office',
                       'arrival_office',
                       'category',
                       'weight'}
    assert expected_fields.issubset(response.data.keys())


@pytest.mark.django_db
def test_get_list_letter(
        url_letters, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: получение списка писем (GET)."""
    Letter.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        weight=123
    )
    Letter.objects.create(
        sender=client_2,
        recipient=client_1,
        departure_office=post_office_2,
        arrival_office=post_office_1,
        category=1,
        weight=55
    )

    response = api_client.get(url_letters)

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_one_obj_letter(
        url_letters, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: получение конкретного письма (GET)."""
    letter = Letter.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        weight=123
    )

    url = f'{url_letters}{letter.id}/'
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 9
    assert response.data['sender'] == client_1.full_name
    assert response.data['recipient'] == client_2.full_name
    assert response.data['departure_office'] == post_office_1.address
    assert response.data['arrival_office'] == post_office_2.address
    assert response.data['departure_index'] == post_office_1.postal_index
    assert response.data['category'] == letter.get_category_display()
    assert response.data['weight'] == letter.weight


@pytest.mark.django_db
def test_get_non_existing_letter(url_letters, api_client):
    """Тест: запрос несуществующего письма должен вернуть 404."""
    url = f'{url_letters}777/'
    response = api_client.get(url)

    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_put_update_letter(
        url_letters, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: полное изменение конкретного письма (PUT)."""
    letter = Letter.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        weight=123
    )

    url = f'{url_letters}{letter.id}/'
    new_data = {
        'sender': client_2.id,
        'recipient': client_1.id,
        'departure_office': post_office_2.id,
        'arrival_office': post_office_1.id,
        'category': 4,
        'weight': 25
    }
    response = api_client.put(url, new_data, format='json')
    letter.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert letter.sender == client_2
    assert letter.recipient == client_1
    assert letter.departure_office == post_office_2
    assert letter.arrival_office == post_office_1
    assert letter.category == new_data['category']
    assert letter.weight == new_data['weight']


@pytest.mark.django_db
def test_patch_update_letter(
        url_letters, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: частичное обновление конкретного письма (PATCH)."""
    letter = Letter.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        weight=123
    )

    url = f'{url_letters}{letter.id}/'
    patch_data = {'category': 4}
    response = api_client.patch(url, patch_data, format='json')
    letter.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert letter.category == patch_data['category']


@pytest.mark.django_db
def test_delete_letter(
        url_letters, api_client, client_1, client_2, post_office_1,
        post_office_2,
):
    """Тест: удаление конкретного письма (DELETE)."""
    letter = Letter.objects.create(
        sender=client_1,
        recipient=client_2,
        departure_office=post_office_1,
        arrival_office=post_office_2,
        category=2,
        weight=123
    )

    url = f'{url_letters}{letter.id}/'
    response = api_client.delete(url)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert not Letter.objects.filter(id=letter.id).exists()
