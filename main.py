import json
from typing import List


OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"


def load_data(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []


def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers: List, products: List, customers: List):
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    # Omogućite unos kupca

    list_customers = customers
    for i, customer in enumerate (list_customers):
        print (f'{i+1}. Name: {customer['name']} - Email: {customer['email']} - vat ID: {customer['vat_id']}')
    

    offer_number = len(offers) + 1
    id_customer = int(input ('Odaberite kupca po imenu: '))-1
    costumer = list_customers[id_customer]['name']
    date = input ('Unesite datum u formi "2024-11-01": ')

    print ('\nPopis proizvoda \n')

    for i, product in enumerate (products):
        print (f'{i+1}. ID: {product['id']} - Name: {product['name']} - Opis: {product['description']} - Cijena: {product['price']}')
            
    add_product = []

    while True:

        product_id = int(input ('Unesite id proizvoda kojeg zelite dodati kosaricu (za kraj upisite 0): '))-1
        if product_id == -1:
            break

        product = products[product_id]

        quantity = int(input ('Unesite kolicinu : '))

        item_total = product['price']*quantity
        sub_total = 0

        add_product.append({
            "id": product_id,
            "product_name": product['name'],
            "description": product['description'],
            "price": product['price'],
            "quantity": quantity,
            "item_total": item_total
        })
        sub_total += item_total 

   # Izračunajte sub_total, tax i total 
    tax = sub_total * 0.25
    total = sub_total + tax


    # Dodajte novu ponudu u listu offers
    
    offers.append({
        "offer_number": offer_number,
        "customer": costumer,
        "date": date,
        "items": add_product,
        "sub_total": sub_total,
        "tax": tax,
        "total": total
    })

    save_data(OFFERS_FILE, offers)



# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products:List):
    """
    Allows the user to add a new product or modify an existing product.
    """
    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke
    print (f'\nUPRAVLJANJE PRIZVODIMA:\n')
    print (f'1. Dodavanje novog proizvoda')
    print (f'2. Izmjena podataka proizvoda')
    print()
    list_products = products
    choice = int(input ('Unesite odabir (1 ili 2): '))
    match choice:
        case 1:
            add_product = {}
            add_product ['id'] = len(list_products) + 1
            add_product ['name'] = input('Unesite naziv proizvoda: ')
            add_product ['description'] = input('Unesite opis proizvoda: ')
            add_product ['price'] = float(input('Unesite cijenu proizvoda: '))

            list_products.append(add_product)
            save_data (PRODUCTS_FILE, list_products)
            print (f'\nUspjesno ste dodali proizvod\n')
        case 2:
            print ('Odaberite proizvod iz liste koji zelite izmjeniti: ')
            print()
            for i, product in enumerate (list_products):
                print (f'{i+1}. ID: {product['id']} - Name: {product['name']} - Opis: {product['description']} - Cijena: {product['price']}')
            
            product_id = int(input ('Unesite ID proizvoda kojeg zelite promjeniti: '))

            list_products [product_id-1]['name'] = input('Izmjenite naziv proizvoda: ')
            list_products [product_id-1]['description'] = input('Izmjenite opis proizvoda: ')
            list_products [product_id-1]['price'] = float(input('Izmjenite cijenu proizvoda: '))

            save_data (PRODUCTS_FILE, list_products)

            print ('Uspjesno ste izmjenili proizvod')
            

# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers:List):
    """
    Allows the user to add a new customer or view all customers.
    """
    # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a  DONE
    # Za pregled: prikaži listu svih kupaca  DONE
    print (f'\nUPRAVLJANJE KORISNICIMA:\n')
    print (f'1. Dodavanje novog korisnika')
    print (f'2. Ispis svih korisnika')
    print()
    list_customers = customers
    choice = int(input ('Unesite odabir (1 ili 2): '))
    match choice:
        case 1:
            add_customer = {}
            add_customer ['name'] = input('Unesite ime pravne osobe kupca: ')
            add_customer ['email'] = input('Unesite e-mail pravne osobe kupca: ')
            add_customer ['vat_id'] = input('Unesite vat_id pravne osobe kupca: ')

            list_customers.append(add_customer)
            save_data (CUSTOMERS_FILE, list_customers)
            print (f'\nUspjesno ste dodali korisnika\n')
        case 2:
            for i, customer in enumerate (list_customers):
                print (f'{i+1}. Name: {customer['name']} - Email: {customer['email']} - vat ID: {customer['vat_id']}')



# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers:List):
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    # Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
    # Prikaz relevantnih ponuda na temelju izbora
    print (f'\nUPRAVLJANJE PONUDAMA:\n')
    print (f'1. Prikaz svih ponuda')
    print (f'2. Prikaz ponuda po mjesecu')
    print (f'3. Prikaz ponude po ID')
    print()
    offers_list = offers
    choice = int(input ('Unesite odabir (npr. 1 ili 2): '))
    match choice:
        case 1:
            for offer in offers_list:
                print_offer(offer)
        case 2:
            datum = input('Unesite datum ponude koju zelite pregledati (u formatu: "2024-11-02"): ')
            for offer in offers:
                if offer['date'] == datum:
                    print_offer(offer)
        case 3:
            ponuda_br = int (input('Unesite broj ponude koju zelite pregledati: '))
            for i, offer in enumerate (offers_list):
                if i == ponuda_br-1:
                    print_offer(offer)



# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer):

    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")


def main():
    # Učitavanje podataka iz JSON datoteka
    offers = load_data(OFFERS_FILE)
    products = load_data(PRODUCTS_FILE)
    customers = load_data(CUSTOMERS_FILE)

    while True:
        print("\nOffers Calculator izbornik:")
        print("1. Kreiraj novu ponudu")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje korisnicima")
        print("4. Prikaz ponuda")
        print("5. Izlaz")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            create_new_offer(offers, products, customers)
        elif choice == "2":
            manage_products(products)
        elif choice == "3":
            manage_customers(customers)
        elif choice == "4":
            display_offers(offers)
        elif choice == "5":
            # Pohrana podataka prilikom izlaza
            save_data(OFFERS_FILE, offers)
            save_data(PRODUCTS_FILE, products)
            save_data(CUSTOMERS_FILE, customers)
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
    main()
