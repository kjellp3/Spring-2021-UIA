import csv
def main():
    customers, products, orders = dict(), dict(), dict()
    [customers.update({row['id']: {'name':row['name'], 'address': row['address'], 'total':0}}) for row in csv.DictReader(open('customers.csv'))]
    [products.update({row['id']: {row['name']: row['price']}}) for row in csv.DictReader (open('products.csv'))]
    [orders.update({row['id']:{'customerid':row['customerid'], 'productid':row['productid'], 'amount':row['amount']}}) for row in csv.DictReader (open('orders.csv'))]
    [customers[order['customerid']].update({'total': customers [order['customerid']]['total']+int("".join(products[order['productid']].values()))*int(order['amount'])}) for order in orders.values()]
    [(print(f'Customer: {customer["name"]}, {customer["address"]}'),) for customer in customers.values()]

    [[print(f'Product: {name}, {price}') for name, price in product.items()] for product in products.values()]

    [products[lists['productid']].update({'soldTotal':int(lists['amount']) + int(products[lists['productid']].setdefault('soldTotal',0))}) for lists in orders.values()]


    [items.update({'grossIncome': int(items[list(items.keys())[0]]) * items['soldTotal']}) for items in products.values()]


    [print(f'{list(item.keys())[0]} amount: {item["soldTotal"]}') for item in products.values()]

    [print(f'{list(item.keys())[0]} gross income: {item["grossIncome"]}') for item in products.values()]

    [(print(f'{customer["name"]} money spent: {customer["total"]}'),) for customer in customers.values()]
if __name__=='__main__':
    main()

