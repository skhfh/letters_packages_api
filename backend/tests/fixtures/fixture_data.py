import pytest

from packages.models import Client, PostOffice


@pytest.fixture
def url_letters():
    return '/api/letters/'


@pytest.fixture
def url_packages():
    return '/api/packages/'


@pytest.fixture
def client_1():
    return Client.objects.create(name='name_1',
                                 lastname='lastname_1',
                                 middle_name='middle_name_1',
                                 phone_number='+71111111111',)


@pytest.fixture
def client_2():
    return Client.objects.create(name='name_2',
                                 lastname='lastname_2',
                                 middle_name='middle_name_2',
                                 phone_number='+72222222222',)


@pytest.fixture
def post_office_1():
    return PostOffice.objects.create(address='address_1',
                                     postal_index='postal_index_1',)


@pytest.fixture
def post_office_2():
    return PostOffice.objects.create(address='address_2',
                                     postal_index='postal_index_2',)
