# Дипломный проект по курсу «Django: создание функциональных веб-приложений»

## Разворачивание проекта

- Скачайте/клонируйте проект. Создайте виртуальное окружение (либо в дальнейшем пользуйтесь глобальным)
- В дирректории главного приложения dj_diplom создайте файл "local_settings.py" и впишите туда данные для подключения к базе данных. Также может потребоваться там прописать ALLOWED_HOSTS.
- Установите зависимости <code>pip install requirements.txt</code>
- Сделайте миграции <code>python manage.py migrate</code>
- Запустить проект <code>python manage.py runserver</code>

Для запуска тестов воспользуйтесь <code>pytest</code>

## Описание API

Сущности:

### Товар

url: `/api/v1/products/`

Создавать товары могут только админы. Смотреть могут все пользователи.

Есть возможность фильтровать товары по цене и содержимому из названия / описания.

Параметры для фильтров: 

<code>min_price</code> - минимальная цена

<code>max_price</code> - максимальная цена

<code>text_search</code> - фрагмент текста для поиска из описания/названия

### Отзыв к товару

url: `/api/v1/product-reviews/`

Оставлять отзыв к товару могут только авторизованные пользователи. 1 пользователь не может оставлять более 1го отзыва.

Отзыв можно фильтровать по ID пользователя, дате создания и ID товара.

Пользователь может обновлять и удалять только свой собственный отзыв.

Параметры для фильтров: 

<code>author_id</code> - id автора отзыва

<code>create_date</code> - дата создания

<code>product_id</code> - id товара

### Заказы

url: `/api/v1/orders/`

Создавать заказы могут только авторизованные пользователи. Админы могут получать все заказы, остальное пользователи только свои.

Заказы можно фильтровать по статусу / общей сумме / дате создания / дате обновления и продуктам из позиций.

Менять статус заказа могут только админы.

Параметры для фильтров: 

<code>status</code> - статус заказа

<code>min_total_price</code> - минимальная сумма заказа

<code>max_total_price</code> - максимальная сумма заказа

<code>create_date_after</code> - дата создания, после 

<code>create_date_before</code> - дата создания, до 

<code>update_date_after</code> - дата обновления, после

<code>update_date_before</code> - дата обновления, до 

<code>products</code> - id продуктов, через запятую

### Подборки

url: `/api/v1/product-collections/`

Создавать подборки могут только админы, остальные пользователи могут только их смотреть.




