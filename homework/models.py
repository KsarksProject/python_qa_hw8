class Product:
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity: int) -> bool:
        return self.quantity >= quantity

    def buy(self, quantity: int):
        if not self.check_quantity(quantity):
            raise ValueError(f"Недостаточно товара {self.name}. Доступно: {self.quantity}, запрошено: {quantity}.")
        self.quantity -= quantity

    def __hash__(self):
        return hash((self.name, self.description))


class Cart:
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        if product not in self.products:
            return

        if remove_count is None or remove_count >= self.products[product]:
            del self.products[product]
        else:
            self.products[product] -= remove_count

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        return sum(product.price * count for product, count in self.products.items())

    def buy(self):
        for product, count in self.products.items():
            if not product.check_quantity(count):
                raise ValueError(f"Недостаточно товара {product.name} на складе для покупки {count} единиц.")

        # Если товаров хватает, выполняем покупку
        for product, count in self.products.items():
            product.buy(count)

        # Очищаем корзину после успешной покупки
        self.clear()
