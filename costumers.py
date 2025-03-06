


class Costumer:
    def __init__(self, name, email, vat_id):
        self.name = name
        self.email = email
        self.vat_id = vat_id

    def __repr__(self):
        return f'Naziv: {self.name}, Email: {self.email}, Vat_ID: {self.vat_id}'