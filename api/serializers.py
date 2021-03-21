from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from api.models import Product, ProductReview, Order, OrderProduct, ProductCollection


class ProductSerializer(ModelSerializer):
    """ Сериалайзер для товаров """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class ProductReviewSerializer(ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['author', 'product', 'text', 'rating']
        read_only_fields = ['author']

    def create(self, validated_data):
        reviews_count = ProductReview.objects.filter(author=validated_data['author']).\
            filter(product=validated_data['product']).count()
        if reviews_count >= 1:
            raise ValidationError({"ProductReview": "Количество отзывов > 1"})
        else:
            return super().create(validated_data)


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'quantity', 'product']


class OrderSerializer(ModelSerializer):
    orderproducts = OrderProductSerializer(source='orderproduct_set', many=True)

    def create(self, validated_data):
        orderproducts_data = validated_data.pop('orderproduct_set')
        validated_data['count'] = 0
        validated_data['total'] = 0
        for item in orderproducts_data:
            price = Product.objects.get(id=item['product'].id).price
            validated_data['total'] += price * item['quantity']
            validated_data['count'] += item['quantity']
        order = Order.objects.create(**validated_data)
        OrderProduct.objects.bulk_create(
            [OrderProduct(order=order, **orderproduct_data) for orderproduct_data in orderproducts_data]
        )
        return order

    def update(self, instance, validated_data):
        orderproducts_data = validated_data.pop('orderproduct_set')
        instance.orderproduct_set.all().delete()

        count = 0
        total = 0
        for item in orderproducts_data:
            price = Product.objects.get(id=item['product'].id).price
            total += price * item['quantity']
            count += item['quantity']

        instance.count = count
        instance.total = total

        if 'status' in validated_data:
            instance.status = validated_data.pop('status')

        instance.save()
        OrderProduct.objects.bulk_create(
            [OrderProduct(order=instance, **orderproduct_data) for orderproduct_data in orderproducts_data]
        )
        return instance

    class Meta:
        model = Order
        read_only_fields = ['create_date', 'update_date']
        fields = ['orderproducts', 'status', 'total', 'count', 'create_date', 'update_date']


class ProductCollectionSerializer(ModelSerializer):
    def create(self, validated_data):
        products = validated_data.pop('products')
        product_collection = ProductCollection.objects.create(**validated_data)
        product_collection.products.add(*products)
        return product_collection

    def update(self, instance, validated_data):
        if 'products' in validated_data:
            products = validated_data.pop('products')
            instance.products.clear()
            instance.products.add(*products)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = ProductCollection
        fields = ['title', 'text', 'products']



