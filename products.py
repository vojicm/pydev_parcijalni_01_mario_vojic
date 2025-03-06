


class Product:
    def __init__(self,
                 name: str,
                 price : float,
                 description=''):
        self.name = name
        self.price = price
        self.description = description

    def __repr__(self) -> str:
        return f'Naziv: {self.name}, Price: {self.price}, Destriptio: {self.name}'