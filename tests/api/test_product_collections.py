import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from api.models import ProductCollection


@pytest.mark.django_db
def test_add_products_to_product_collections_by_admin(
        admin_client,
        client,
        create_product_collections_by_admin
):
    """ Тест добавления товаров в подборки админом """
    product_collections = create_product_collections_by_admin
    """ Изменение информации о подборке админом """
    new_text = {'title': 'Товары к чаю', 'text': 'Что может быть лучше чая?'}
    collection_info = ProductCollection.objects.get(title='Для чая')
    url = reverse("productcollections-detail", args=(collection_info.id,))
    resp = admin_client.patch(url, data=new_text, content_type='application/json')
    new_collection = ProductCollection.objects.get(title=new_text['title'])
    assert resp.status_code == HTTP_200_OK
    assert new_collection.text == "Что может быть лучше чая?"
    """ Получение списка подборок пользователем """
    url = reverse("productcollections-list")
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK
