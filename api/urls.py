from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register(r'products', views.ProductViewSet, 'products')
router.register(r'product-reviews', views.ProductReviewViewSet, 'productreviews')
router.register(r'orders', views.OrderViewSet, 'orders')
router.register(r'product-collections', views.ProductCollectionViewSet, 'productcollections')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
