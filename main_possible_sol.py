import json

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


def compute_totals(items, tax_rate=0.25):
    """
    Given a list of items (each containing `item_total`),
    compute and return sub_total, tax, and total.
    """
    sub_total = sum(item["item_total"] for item in items)
    tax = round(sub_total * tax_rate, 2)
    total = round(sub_total + tax, 2)
    return sub_total, tax, total


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers, products, customers):
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    print("\n--- Kreiranje nove ponude ---")

    # 1. Odabir kupca
    if not customers:
        print("Nema kupaca u bazi. Dodajte kupce prije kreiranja ponude.")
        return

    print("Popis dostupnih kupaca:")
    for index, customer in enumerate(customers, start=1):
        print(f"{index}. {customer['name']} (Email: {customer['email']}, VAT ID: {customer['vat_id']})")

    selected_customer = None
    while True:
        choice = input("Unesite broj ispred kupca (ili 'cancel' za odustajanje): ")
        if choice.lower() == 'cancel':
            print("Odustali ste od kreiranja ponude.")
            return
        try:
            choice_index = int(choice)
            if 1 <= choice_index <= len(customers):
                selected_customer = customers[choice_index - 1]["name"]
                break
            else:
                print("Nepostojeći indeks. Pokušajte ponovo.")
        except ValueError:
            print("Pogrešan unos. Pokušajte ponovo.")

    # 2. Unos datuma
    date = input("Unesite datum ponude (npr. 2024-11-10): ")
    if not date.strip():
        print("Datum nije unesen. Ponuda neće biti kreirana.")
        return

    # 3. Dodavanje proizvoda u stavke
    cart_items = []
    while True:
        print("\nPopis dostupnih proizvoda:")
        for p in products:
            print(f"ID: {p['id']} => {p['name']} (Cijena: ${p['price']})")

        product_id_input = input("Unesite ID proizvoda koji želite dodati (ili 'cancel' za završetak dodavanja): ")
        if product_id_input.lower() == 'cancel':
            break

        # Provjera ispravnosti ID-a
        try:
            product_id = int(product_id_input)
        except ValueError:
            print("Pogrešan unos. Unesite broj ili 'cancel'.")
            continue

        # Pronađi proizvod
        product = next((p for p in products if p["id"] == product_id), None)
        if not product:
            print("Proizvod s tim ID-om ne postoji.")
            continue

        # Unos količine
        quantity_input = input(f"Unesite količinu za '{product['name']}': ")
        try:
            quantity = int(quantity_input)
            if quantity < 1:
                print("Količina mora biti veća od 0.")
                continue
        except ValueError:
            print("Neispravan unos količine.")
            continue

        # Dodavanje stavke u listu
        item_total = product["price"] * quantity
        cart_items.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "description": product["description"],
            "price": product["price"],
            "quantity": quantity,
            "item_total": round(item_total, 2)
        })
        print(f"Proizvod '{product['name']}' dodan u ponudu.")

    if not cart_items:
        print("Niste dodali nijedan proizvod. Ponuda neće biti kreirana.")
        return

    # 4. Izračun ukupnih vrijednosti
    sub_total, tax, total = compute_totals(cart_items, tax_rate=0.25)

    # 5. Generiranje novog offer_number
    if offers:
        max_offer_number = max(offer["offer_number"] for offer in offers)
    else:
        max_offer_number = 0
    new_offer_number = max_offer_number + 1

    # 6. Kreiranje i dodavanje ponude
    new_offer = {
        "offer_number": new_offer_number,
        "customer": selected_customer,
        "date": date,
        "items": cart_items,
        "sub_total": round(sub_total, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
    }

    offers.append(new_offer)
    print(f"Nova ponuda kreirana uspješno (Offer #{new_offer_number})!")


# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products):
    """
    Allows the user to add a new product or modify an existing product.
    """
    print("\n--- Upravljanje proizvodima ---")
    while True:
        print("\nOdaberite opciju:")
        print("1. Dodaj novi proizvod")
        print("2. Izmijeni postojeći proizvod")
        print("0. Povratak na glavni izbornik")
        choice = input("Vaš odabir: ")

        if choice == "1":
            # Dodavanje novog proizvoda
            print("\n--- Dodavanje novog proizvoda ---")
            name = input("Unesite naziv proizvoda: ").strip()
            description = input("Unesite opis proizvoda: ").strip()
            try:
                price = float(input("Unesite cijenu proizvoda: "))
            except ValueError:
                print("Neispravan unos cijene. Proizvod nije kreiran.")
                continue

            if products:
                max_id = max(p["id"] for p in products)
            else:
                max_id = 0
            new_id = max_id + 1

            new_product = {
                "id": new_id,
                "name": name,
                "description": description,
                "price": price
            }
            products.append(new_product)
            print(f"Proizvod '{name}' uspješno dodan s ID-om {new_id}.")

        elif choice == "2":
            # Izmjena postojećeg proizvoda
            if not products:
                print("Nema proizvoda u bazi.")
                continue

            print("\nPopis proizvoda:")
            for p in products:
                print(f"ID: {p['id']} => {p['name']} (Cijena: ${p['price']})")

            try:
                edit_id = int(input("Unesite ID proizvoda koji želite izmijeniti: "))
            except ValueError:
                print("Pogrešan unos.")
                continue

            product_to_edit = next((p for p in products if p["id"] == edit_id), None)
            if not product_to_edit:
                print("Proizvod s tim ID-om ne postoji.")
                continue

            print(f"Trenutni naziv: {product_to_edit['name']}")
            new_name = input("Unesite novi naziv (ili pritisnite Enter za preskakanje): ").strip()
            if new_name:
                product_to_edit["name"] = new_name

            print(f"Trenutni opis: {product_to_edit['description']}")
            new_description = input("Unesite novi opis (ili Enter za preskakanje): ").strip()
            if new_description:
                product_to_edit["description"] = new_description

            print(f"Trenutna cijena: {product_to_edit['price']}")
            new_price_input = input("Unesite novu cijenu (ili Enter za preskakanje): ").strip()
            if new_price_input:
                try:
                    new_price = float(new_price_input)
                    product_to_edit["price"] = new_price
                except ValueError:
                    print("Neispravan unos cijene. Cijena nije izmijenjena.")

            print(f"Proizvod (ID: {edit_id}) uspješno ažuriran.")

        elif choice == "0":
            # Povratak na glavni izbornik
            break
        else:
            print("Nepoznata opcija. Pokušajte ponovo.")


# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers):
    """
    Allows the user to add a new customer or view all customers.
    """
    print("\n--- Upravljanje kupcima ---")
    while True:
        print("\nOdaberite opciju:")
        print("1. Dodaj novog kupca")
        print("2. Pregled svih kupaca")
        print("0. Povratak na glavni izbornik")
        choice = input("Vaš odabir: ")

        if choice == "1":
            # Dodavanje novog kupca
            print("\n--- Dodavanje novog kupca ---")
            name = input("Unesite ime (naziv) kupca: ").strip()
            email = input("Unesite email kupca: ").strip()
            vat_id = input("Unesite VAT ID kupca: ").strip()

            if not name:
                print("Naziv kupca je obvezan. Kupac nije dodan.")
                continue

            new_customer = {
                "name": name,
                "email": email,
                "vat_id": vat_id
            }
            customers.append(new_customer)
            print(f"Kupac '{name}' uspješno dodan.")

        elif choice == "2":
            # Pregled svih kupaca
            if not customers:
                print("Nema kupaca u bazi.")
                continue
            print("\n--- Popis svih kupaca ---")
            for idx, c in enumerate(customers, start=1):
                print(f"{idx}. {c['name']} | Email: {c['email']} | VAT ID: {c['vat_id']}")
        elif choice == "0":
            # Povratak na glavni izbornik
            break
        else:
            print("Nepoznata opcija. Pokušajte ponovo.")


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers):
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    print("\n--- Prikaz ponuda ---")
    while True:
        print("\nOdaberite opciju:")
        print("1. Prikaži sve ponude")
        print("2. Prikaži ponude po mjesecu (YYYY-MM)")
        print("3. Prikaži ponudu prema Offer Number (ID-u ponude)")
        print("0. Povratak na glavni izbornik")
        choice = input("Vaš odabir: ")

        if choice == "1":
            # Prikaz svih ponuda
            if not offers:
                print("Nema ponuda u bazi.")
                continue
            for offer in offers:
                print_offer(offer)

        elif choice == "2":
            # Prikaz ponuda po mjesecu
            if not offers:
                print("Nema ponuda u bazi.")
                continue
            month_input = input("Unesite mjesec u formatu YYYY-MM: ")
            found_any = False
            for offer in offers:
                # offer['date'] assumed to be "YYYY-MM-DD"
                if offer["date"].startswith(month_input):
                    print_offer(offer)
                    found_any = True
            if not found_any:
                print(f"Nema ponuda za mjesec {month_input}.")

        elif choice == "3":
            # Prikaz jedne ponude
            if not offers:
                print("Nema ponuda u bazi.")
                continue
            try:
                offer_number = int(input("Unesite Offer Number (ID ponude): "))
            except ValueError:
                print("Neispravan unos.")
                continue

            offer_to_print = next((o for o in offers if o["offer_number"] == offer_number), None)
            if offer_to_print:
                print_offer(offer_to_print)
            else:
                print(f"Ponuda s ID brojem {offer_number} ne postoji.")

        elif choice == "0":
            break
        else:
            print("Nepoznata opcija. Pokušajte ponovo.")


# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer):
    """Display details of a single offer."""
    print(f"\nPonuda br: {offer['offer_number']}, Kupac: {offer['customer']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Količina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno (neto): ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno (bruto): ${offer['total']}")


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
            print("Hvala na korištenju. Doviđenja!")
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
    main()