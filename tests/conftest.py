import pytest
from rest_framework.reverse import reverse
from model_bakery import baker
from django.contrib.auth.models import User
from rest_framework.status import HTTP_201_CREATED

from api.models import Product, Order


@pytest.fixture
def authenticated_client(client, django_user_model):
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    return client


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        product = baker.make('api.Product', **kwargs)
        return product
    return factory


@pytest.fixture
def create_productreview_by_authenticated_user(product_factory, authenticated_client):
    product = product_factory(_quantity=3)
    url = reverse("productreviews-list")
    product_info = Product.objects.get(name=product[0])
    productreview = {'text': 'Хорошая бочка печенья', 'rating': 4, 'product': product_info.id}
    response = authenticated_client.post(url, data=productreview, content_type='application/json')
    assert response.status_code == HTTP_201_CREATED
    return product_info, productreview


@pytest.fixture
def create_order_by_authenticated_user(authenticated_client, product_factory):
    url = reverse("orders-list")
    user = User.objects.get(username='foo')
    product = product_factory(_quantity=3)
    product_info1 = Product.objects.get(name=product[0])
    product_info2 = Product.objects.get(name=product[1])
    product_info3 = Product.objects.get(name=product[2])
    orderproduct1 = {'product': product_info1.id, 'quantity': 100}
    orderproduct2 = {'product': product_info2.id, 'quantity': 1}
    orderproduct3 = {'product': product_info3.id, 'quantity': 5}
    order = {
        'orderproducts': [
            orderproduct1,
            orderproduct2,
            orderproduct3
        ]
    }
    resp = authenticated_client.post(
        url,
        data=order,
        content_type='application/json'
    )
    assert resp.status_code == HTTP_201_CREATED
    return order, user


@pytest.fixture
def create_product_collections_by_admin(authenticated_client, create_order_by_authenticated_user,
                                        product_factory, admin_client):
    product_factory(_quantity=4)
    product = Product.objects.all()
    url = reverse("productcollections-list")
    collection = {
        "title": "Для ужина",
        "text": "Вкусный ужин",
        "products": [
            product[0].id,
            product[3].id
        ]
    }
    collection1 = {
        "title": "Для чая",
        "text": "Печенье, варенье и т.д.",
        "products": [
            product[1].id,
            product[2].id
        ]
    }
    response = admin_client.post(url, data=collection, content_type='application/json')
    response1 = admin_client.post(url, data=collection1, content_type='application/json')
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    return collection, collection1
