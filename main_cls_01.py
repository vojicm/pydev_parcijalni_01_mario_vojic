import products as pr


def main():
    products = []

    laptop = pr.Product(
        'Laptop',
        800.00,
        '15-inch display, 8GB RAM, 256GB SSD')
    products.append(laptop)
    print(laptop)

    smartphone = pr.Product(
        'Smartphone',
        500.00,
        '6-inch display, 128GB storage'
    )
    products.append(smartphone)
    print(smartphone)

    print(products)



if __name__ == '__main__':
    main()