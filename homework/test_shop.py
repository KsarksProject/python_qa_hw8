import pytest
from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


@pytest.fixture
def product1():
    return Product("notebook", 200, "This is a notebook", 500)


@pytest.fixture
def product2():
    return Product("pen", 50, "This is a pen", 1000)


class TestProducts:
    """
    Тесты для класса Product
    """

    def test_product_check_quantity(self, product):
        # Проверяем, что доступное количество достаточно
        assert product.check_quantity(500) is True
        # Проверяем, что запрашиваемое количество превышает доступное
        assert product.check_quantity(1500) is False

    def test_product_buy(self, product):
        # Покупаем товар в допустимом количестве
        initial_quantity = product.quantity
        product.buy(500)
        assert product.quantity == initial_quantity - 500

    def test_product_buy_more_than_available(self, product):
        # Попытка купить больше, чем есть в наличии, должна вызывать ValueError
        with pytest.raises(ValueError, match="Недостаточно товара book."):
            product.buy(1500)


class TestCart:
    """
    Тесты для класса Cart
    """

    def test_add_product(self, cart, product1):
        # Добавляем продукт в корзину
        cart.add_product(product1, 2)
        assert cart.products[product1] == 2

        # Добавляем тот же продукт еще раз
        cart.add_product(product1, 3)
        assert cart.products[product1] == 5

    def test_remove_product(self, cart, product1):
        cart.add_product(product1, 5)

        # Удаляем часть продукта
        cart.remove_product(product1, 3)
        assert cart.products[product1] == 2

        # Удаляем продукт полностью
        cart.remove_product(product1)
        assert product1 not in cart.products

    def test_clear(self, cart, product1, product2):
        cart.add_product(product1, 2)
        cart.add_product(product2, 3)

        # Очищаем корзину
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product1, product2):
        cart.add_product(product1, 2)  # Цена: 200 * 2 = 400
        cart.add_product(product2, 3)  # Цена: 50 * 3 = 150

        # Проверяем общую стоимость
        assert cart.get_total_price() == 550

    def test_buy(self, cart, product1, product2):
        cart.add_product(product1, 2)
        cart.add_product(product2, 3)

        # Выполняем покупку
        cart.buy()

        # Проверяем, что продукты были куплены
        assert product1.quantity == 498
        assert product2.quantity == 997

        # Корзина должна быть очищена после покупки
        assert len(cart.products) == 0

    def test_buy_with_insufficient_stock(self, cart, product1):
        cart.add_product(product1, 600)

        # Покупка должна вызвать ValueError из-за недостатка товара
        with pytest.raises(ValueError, match="Недостаточно товара notebook на складе для покупки 600 единиц."):
            cart.buy()
