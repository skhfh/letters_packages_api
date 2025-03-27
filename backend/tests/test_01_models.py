import pytest
from django.core.exceptions import ValidationError

from packages.models import Client, PostOffice


@pytest.mark.django_db
def test_create_client_with_all_fields():
    """Тест: создание клиента со всеми корректными аргументами."""
    name = 'Name'
    lastname = 'Lastname'
    middle_name = 'Middle_name'
    phone_number = '+71234567890'

    client = Client.objects.create(name=name,
                                   lastname=lastname,
                                   middle_name=middle_name,
                                   phone_number=phone_number)

    assert Client.objects.count() == 1
    assert client.name == name
    assert client.lastname == lastname
    assert client.middle_name == middle_name
    assert client.phone_number == phone_number
    assert client.full_name == f'{lastname} {name} {middle_name}'
    assert str(client) == f'{lastname} {name} {middle_name}'


@pytest.mark.django_db
def test_create_client_without_middle_name():
    """Тест: создание клиента без отчества."""
    name = 'Name'
    lastname = 'Lastname'
    phone_number = '+71234567890'

    client = Client.objects.create(name=name,
                                   lastname=lastname,
                                   phone_number=phone_number)

    assert Client.objects.count() == 1
    assert client.name == name
    assert client.lastname == lastname
    assert client.middle_name is None
    assert client.phone_number == phone_number
    assert client.full_name == f'{lastname} {name}'
    assert str(client) == f'{lastname} {name}'


@pytest.mark.django_db
@pytest.mark.parametrize('invalid_phone_number', [
    '12345',
    'justtext',
    '+12345678901',
    '12345678901',
])
def test_create_client_with_wrong_phone_number(invalid_phone_number):
    """Тест: создание клиента с некорректным номером телефона
    должно вызывать ошибку валидации."""
    with pytest.raises(ValidationError) as error:
        client = Client(name='Name',
                        lastname='Lastname',
                        middle_name='Middle_name',
                        phone_number=invalid_phone_number)
        client.full_clean()

    assert 'phone_number' in str(error)


@pytest.mark.django_db
def test_create_post_office():
    """Тест: создание почтового пункта."""
    address = 'какой-то город, какая-то улица и дом 100'
    postal_index = '054985'

    post_office = PostOffice.objects.create(address=address,
                                            postal_index=postal_index)

    assert PostOffice.objects.count() == 1
    assert post_office.address == address
    assert post_office.postal_index == postal_index
    assert str(post_office) == address


@pytest.mark.django_db
@pytest.mark.parametrize('invalid_postal_index', [
    '12345',
    'justte',
    '1234567',
    '125d26',
])
def test_create_post_office_with_wrong_index(invalid_postal_index):
    """Тест: создание почтового пункта с некорректным индексом
    должно вызывать ошибку валидации."""
    with pytest.raises(ValidationError) as error:
        post_office = PostOffice(
            address='какой-то город, какая-то улица и дом 100',
            postal_index=invalid_postal_index
        )
        post_office.full_clean()

    assert 'postal_index' in str(error)
