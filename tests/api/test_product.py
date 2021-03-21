import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_204_NO_CONTENT

from api.models import Product


@pytest.mark.django_db
def test_create_product_by_authenticated_client(client, django_user_model):
    """ Тест на невозможность создания товара пользователем """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("products-list")
    product = {"name": "Печенье", "price": 50, "description": "Тестовая коробка печенья"}
    response = client.post(url, product)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_product_by_admin(admin_client):
    """ Тест на создание товара админом """
    url = reverse("products-list")
    product = {"name": "Печенье", "price": 50, "description": "Тестовая коробка печенья"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_update_product_by_admin(admin_client, product_factory):
    """ Тест на изменение товара в списке """
    product = product_factory(_quantity=3)
    new_product_name = {
        "name": "Обновлённый продукт", "price": 150, "description": "Новый, обновлённый продукт"
    }
    product_info = Product.objects.get(name=product[0])
    url = reverse("products-detail", args=(product_info.id,))
    resp = admin_client.put(url, data=new_product_name, content_type='application/json')
    new_product = Product.objects.get(name=new_product_name['name'])
    assert resp.status_code == HTTP_200_OK
    assert new_product.price == 150
    assert new_product.name == new_product_name['name']
    assert new_product.description == new_product_name['description']


@pytest.mark.django_db
def test_destroy_product_by_admin(admin_client, product_factory):
    """ Тест на удаление продукта из списка """
    product = product_factory(_quantity=3)
    product = Product.objects.get(name=product[0])
    url = reverse("products-detail", args=(product.id,))
    resp = admin_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_products_list(client, product_factory):
    """ Тест на получение списка продуктов пользователем """
    product_factory(_quantity=3)
    url = reverse("products-list")
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_products_retrieve(client, product_factory):
    """ Тест получения информации о конкретном продукте """
    product = product_factory(_quantity=3)
    product = Product.objects.get(name=product[0])
    url = reverse("products-detail", args=(product.id,))
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert product.name == resp_json['name']


@pytest.mark.django_db
def test_price_filter(client, product_factory):
    """ Тест фильтра по цене """
    product_factory(_quantity=3)
    min_price = 5
    max_price = 110
    params = f'min_price={min_price}&max_price={max_price}'
    url = reverse("products-list") + '?' + params
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert min_price < float(item['price'])
        assert max_price > float(item['price'])


@pytest.mark.django_db
def test_for_insistence_in_product(client, product_factory):
    """ Тест по содержимому в названии/описании """
    product_factory(_quantity=3)
    name_part = 'бочка'
    params = f'text_search={name_part}'
    url = reverse("products-list") + '?' + params
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert name_part in item['name'] or name_part in item['description']

