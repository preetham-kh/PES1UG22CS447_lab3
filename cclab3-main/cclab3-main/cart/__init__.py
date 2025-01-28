import json
from cart import dao
from products import get_product, Product


class Cart:
    def _init_(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        contents = cart_detail['contents'] if 'contents' in cart_detail else '[]'  # Corrected line
        try:
            evaluated_contents = json.loads(contents)  # Safely parse JSON
            if isinstance(evaluated_contents, list):
                items.extend(evaluated_contents)
            else:
                print(f"Warning: Invalid format for contents: {contents}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for cart contents: {contents}, error: {e}")
            continue  # Skip malformed data

    return get_product(items) if items else []


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
