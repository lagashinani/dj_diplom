from django.contrib import admin

from api.models import Order, OrderProduct, \
    ProductCollection, Product, ProductReview


class RelationshipInline(admin.TabularInline):
    model = OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass
