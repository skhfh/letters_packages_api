import pytest
from rest_framework.test import APIClient

from packages.models import Client, Letter, Package, PostOffice


@pytest.mark.django_db
def test_create_letter(api_client, client_1, client_2, post_office_1,
                       post_office_2):
    """Тест создания письма через API (POST)."""
    url = '/api/letters/'
    data = {
        'sender': client_1.id,
        'recipient': client_2.id,
        'departure_office': post_office_1.id,
        'arrival_office': post_office_2.id,
        'category': 1,
        'weight': 100
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Letter.objects.count() == 1
    assert len(response.data) == 9
    assert response.data['sender'] == client_1.full_name
    assert response.data['recipient'] == client_2.full_name
    assert response.data['departure_office'] == post_office_1.address
    assert response.data['arrival_office'] == post_office_2.address
    assert response.data['departure_index'] == post_office_1.postal_index
    assert response.data['category'] == 'Письмо'
    assert response.data['weight'] == 100

