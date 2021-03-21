from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum


class DateFields(models.Model):
    """ Базовая модель с полями 'дата создания' и 'дата обновления' """
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        abstract = True


class Product(DateFields):
    """ Модель товаров """
    name = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class ProductReview(DateFields):
    """ Отзыв по товару """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
     )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.author} - {self.product}'


class Order(DateFields):
    """ Модель заказов """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE)
    products = models.ManyToManyField(
        'Product',
        verbose_name='Товары',
        related_name='order',
        through='OrderProduct',
        through_fields=('order', 'product'),
    )
    status = models.CharField(
        max_length=100,
        choices=(
            ('NEW', 'Новый'),
            ('IN_PROGRESS', 'В работе'),
            ('DONE', 'Выполнен')
        ),
        default='NEW'
    )
    count = models.PositiveIntegerField(editable=False)
    total = models.FloatField(editable=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-create_date']

    def __str__(self):
        return f'{self.user} - ' \
               f'{self.orderproduct_set.aggregate(Sum("quantity"))["quantity__sum"] or 0}'


class OrderProduct(models.Model):
    """ Вспомогательная модель для связи многие ко мноигим товары - заказы """
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class ProductCollection(DateFields):
    """ Подборки товаров """
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    text = models.TextField()
    products = models.ManyToManyField('Product', related_name='product_collections')

    class Meta:
        verbose_name = 'Подборка товаров'
        verbose_name_plural = 'Подборки товаров'

    def __str__(self):
        return self.title
