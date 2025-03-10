import products as pr
import costumers as cs




def main():
    products = []
    costumers_list = []

    laptop = pr.Product(
        'Laptop',
        800.00,
        '15-inch display, 8GB RAM, 256GB SSD'
    )
    products.append(laptop)

    smartphone = pr.Product(
        'Smartphone',
        500.00,
        '6-inch display, 128GB storage'
    )
    products.append(smartphone)

    print(products)
    print(smartphone)
    print(laptop)

    came_adriatic = cs.Costumer(
        'CAME Adriatic d.o.o.',
        'info@came.hr',
        '123456'
    )

    costumers_list.append(came_adriatic)

    print (costumers_list)
    print(came_adriatic)

if __name__ == '__main__':
    main()


