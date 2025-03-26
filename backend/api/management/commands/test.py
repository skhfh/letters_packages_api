import csv




with open('C:/Dev/letters_packages_api/backend/static/data/clients.csv', 'r', encoding='utf-8') as file:
    try:
        rows = csv.DictReader(file, delimiter=';')
        records = [print(row) for row in rows]
    except Exception as e:
        print(e)

