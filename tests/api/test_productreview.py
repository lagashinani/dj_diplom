import pytest
from django.urls import reverse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT, \
    HTTP_401_UNAUTHORIZED

from api.models import Product, ProductReview


@pytest.mark.django_db
def test_create_productreview_by_authenticated_client(
        authenticated_client,
        product_factory,
        create_productreview_by_authenticated_user
):
    """ Тест создания отзыва авторизованным пользователем и проверка невозможности создания более одного отзыва"""
    url = reverse("productreviews-list")
    product_factory(_quantity=3)
    product_info, productreview1 = create_productreview_by_authenticated_user
    productreview2 = {'text': 'Отличная бочка варенья', 'rating': 5, 'product': product_info.id}
    resp = authenticated_client.post(url, data=productreview2, content_type='application/json')
    assert resp.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_productreview_by_not_authenticated_client(
        client,
        product_factory
):
    """ Тест невозможности создания отзыва неавторизованным пользователем """
    product = product_factory(_quantity=3)
    url = reverse("productreviews-list")
    product_info = Product.objects.get(name=product[0])
    productreview = {'text': 'Отлично', 'rating': 4, 'product': product_info.id}
    response = client.post(url, data=productreview, content_type='application/json')
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_productreview_by_authenticated_client(
        product_factory,
        authenticated_client,
        create_productreview_by_authenticated_user
):
    """ Тест обновления отзыва авторизованным пользователем"""
    product_factory(_quantity=3)
    product_info, productreview = create_productreview_by_authenticated_user
    new_productreview = {"text": "Пам пам пам", "rating": 2, "product": product_info.id}
    productreview_info = ProductReview.objects.get(text=productreview["text"])
    url = reverse("productreviews-detail", args=(productreview_info.id,))
    resp = authenticated_client.put(url, data=new_productreview, content_type='application/json')
    new_productreview_info = ProductReview.objects.get(text=new_productreview['text'])
    assert resp.status_code == HTTP_200_OK
    assert new_productreview_info.rating == 2


@pytest.mark.django_db
def test_destroy_review_by_authenticated_client(
        product_factory,
        create_productreview_by_authenticated_user,
        authenticated_client
):
    """ Тест удаления отзыва авторизованным пользователем """
    product_factory(_quantity=3)
    product_info, productreview = create_productreview_by_authenticated_user
    productreview_info = ProductReview.objects.get(text=productreview["text"])
    url = reverse("productreviews-detail", args=(productreview_info.id,))
    resp = authenticated_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_filter_productreview_by_product(
        product_factory,
        authenticated_client,
        create_productreview_by_authenticated_user
):
    """ Тест фильтра отзывов по продуктам """
    product_factory(_quantity=3)
    product_info, productreview = create_productreview_by_authenticated_user
    params = f'product={product_info.id}'
    url = reverse("productreviews-list") + '?' + params
    resp = authenticated_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert item['product'] == product_info.id
