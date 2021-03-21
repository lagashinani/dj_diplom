from django.contrib.postgres.search import SearchVector

from rest_framework import viewsets

from api.models import Product, ProductReview, Order, ProductCollection
from api.serializers import ProductSerializer, ProductReviewSerializer, OrderSerializer, ProductCollectionSerializer
from api.permissions import ProductReviewPermissions, OrderPermissions, IsAdminUserOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        text_search = self.request.query_params.get('text_search')
        params = {
            'price__lte': max_price,
            'price__gte': min_price
        }
        if text_search is not None:
            queryset = Product.objects.annotate(
                search=SearchVector('name', 'description')
            ).filter(
                search=text_search,
                **{key: value for key, value in params.items() if value is not None}
            )
        else:
            queryset = Product.objects.filter(
                **{key: value for key, value in params.items() if value is not None}
            )
        return queryset


class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [ProductReviewPermissions]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        author_id = self.request.query_params.get('author_id')
        create_date = self.request.query_params.get('create_date')
        product_id = self.request.query_params.get('product_id')
        params = {
            'author_id': author_id,
            'create_date__date': create_date,
            'product_id': product_id
        }
        queryset = ProductReview.objects.filter(
            **{key: value for key, value in params.items() if value is not None}
        )
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [OrderPermissions]
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        status = self.request.query_params.get('status')
        min_total_price = self.request.query_params.get('min_total_price')
        max_total_price = self.request.query_params.get('max_total_price')
        create_date_after = self.request.query_params.get('create_date_after')
        create_date_before = self.request.query_params.get('create_date_before')
        update_date_after = self.request.query_params.get('update_date_after')
        update_date_before = self.request.query_params.get('update_date_before')
        products = self.request.query_params.get('products')
        params = {
            'status': status,
            'create_date__date__gte': create_date_after,
            'create_date__date__lte': create_date_before,
            'update_date__date__gte': update_date_after,
            'update_date__date__lte': update_date_before,
            'products__in': products.split(',') if products else products,
            'total__lte': max_total_price,
            'total__gte': min_total_price
        }
        if self.request.user.is_staff:
            queryset = Order.objects.filter(
                **{key: value for key, value in params.items() if value is not None}
            )
        else:
            queryset = Order.objects.filter(
                user=self.request.user,
                **{key: value for key, value in params.items() if value is not None}
            )
        return queryset


class ProductCollectionViewSet(viewsets.ModelViewSet):
    queryset = ProductCollection.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductCollectionSerializer
