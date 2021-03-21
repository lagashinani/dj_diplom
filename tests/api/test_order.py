import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from api.models import Order, Product, OrderProduct
import datetime as dt


@pytest.mark.django_db
def test_create_order_by_authenticated_client(
        product_factory,
        create_order_by_authenticated_user
):
    """ Тест на создание заказа и создание позиций заказа  """
    product_factory(_quantity=3)
    create_order_by_authenticated_user


@pytest.mark.django_db
def test_get_list_of_orders_by_admin(
        product_factory,
        admin_client,
        create_order_by_authenticated_user
):
    """ Тест на вывод списка заказов """
    product_factory(_quantity=3)
    create_order_by_authenticated_user
    url = reverse("orders-list")
    resp = admin_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_get_own_list_of_orders_by_authenticated_user(
        product_factory,
        authenticated_client,
        create_order_by_authenticated_user
):
    """ Тест на получение своего заказа пользователем"""
    product_factory(_quantity=3)
    order, user = create_order_by_authenticated_user
    order_info = Order.objects.get(user=user)
    url = reverse("orders-detail", args=(order_info.id,))
    resp = authenticated_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_order_filter_by_total_price(
        product_factory,
        create_order_by_authenticated_user,
        admin_client
):
    """ Тест фильтра по итоговой цене """
    product_factory(_quantity=3)
    order, user = create_order_by_authenticated_user
    order_info = Order.objects.get(user=user)
    min_total_price = 10
    max_total_price = 1200
    params = f'min_total_price={min_total_price}&max_total_price={max_total_price}'
    url = reverse("orders-list") + '?' + params
    resp = admin_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert item['total'] == order_info.total


@pytest.mark.django_db
def test_order_filter_by_create_date(
        product_factory,
        create_order_by_authenticated_user,
        admin_client,
):
    """ Тест фильтра по дате создания """
    product_factory(_quantity=3)
    order, user = create_order_by_authenticated_user
    order_info = Order.objects.get(user=user)
    create_date_after = '2021-01-18'
    created_date_before = '2021-02-09'
    params = f'create_date_after={create_date_after}&created_date_before={created_date_before}'
    url = reverse("orders-list") + '?' + params
    resp = admin_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        data_from_response = item['create_date'].replace('T', ' ').split('.')[0]
        data_from_db = str(order_info.create_date).split('.')[0]
        assert data_from_response == data_from_db


@pytest.mark.django_db
def test_order_filter_by_update_date(
        product_factory,
        create_order_by_authenticated_user,
        admin_client,
):
    """ Тест фильтра по дате обновления """
    product_factory(_quantity=3)
    order, user = create_order_by_authenticated_user
    order_info = Order.objects.get(user=user)
    now = dt.date.today()
    delta = dt.timedelta(hours=48)
    two_days_ago = now - delta
    two_days_further = now + delta
    params = f'updated_date_after={two_days_ago}&updated_date_before={two_days_further}'
    url = reverse("orders-list") + '?' + params
    resp = admin_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        data_from_response = item['update_date'].replace('T', ' ').split('.')[0]
        data_from_db = str(order_info.update_date).split('.')[0]
        assert data_from_response == data_from_db
