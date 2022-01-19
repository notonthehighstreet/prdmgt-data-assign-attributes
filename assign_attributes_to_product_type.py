import argparse, time, csv, uuid

parser = argparse.ArgumentParser(description = 'Assign Attributes to Product Types in PIM')
parser.add_argument('-input_file', type=str, default='attribute_data.csv', help='Attributes to assign to Product Types')
args = parser.parse_args()

def checkNotEmpty(data):
    if not data:
        print("Missing Data")
        quit()

def checkProductTypeExists(product_type_ids):
    first_product_type_id = product_type_ids.pop()

    with open("product-type-exists-{}.sql".format(time.strftime('%Y%m%d')), "w") as output_file:
        output_file.write("SELECT id FROM (SELECT '{}' AS id \n".format(first_product_type_id))

        for product_type_id in product_type_ids:
            output_file.write("UNION SELECT '{}'\n".format(product_type_id))

        output_file.write(") AS p\n")
        output_file.write("LEFT JOIN product_types pt ON pt.product_type_id = id\n")
        output_file.write("WHERE pt.product_type_id IS NULL\n")
        output_file.close()

def checkAttributeExists(attribute_ids):
    first_attribute_id = attribute_ids.pop()

    with open("attribute-exists-{}.sql".format(time.strftime('%Y%m%d')), "w") as output_file:
        output_file.write("SELECT id FROM (SELECT '{}' AS id \n".format(first_attribute_id))

        for attribute_id in attribute_ids:
            output_file.write("UNION SELECT '{}'\n".format(attribute_id))

        output_file.write(") AS a\n")
        output_file.write("LEFT JOIN attributes at ON at.attribute_id = id\n")
        output_file.write("WHERE at.attribute_id IS NULL\n")
        output_file.close()

def assignAttributes(product_type_id, attribute_id):
    attribute_sql = "INSERT IGNORE INTO product_type_attributes (product_type_id, attribute_id) VALUES ('{}', '{}');\n".format(product_type_id, attribute_id)

    return attribute_sql


with open(args.input_file, "r") as input_file:
    reader = csv.reader(input_file)

    # skip header row
    next(reader)
    names = []
    product_type_ids = []
    attribute_ids = []

    with open("attribute-insert-{}.sql".format(time.strftime('%Y%m%d')), "w") as output_file:
        for row in reader:
            col = 0

            for data in row:
                # We only care about the first 2 columns in the data set
                if col < 2:
                    checkNotEmpty(data)
                col += 1

            product_type_id = row[0]
            attribute_id = row[1]

            product_type_ids.append(product_type_id)
            attribute_ids.append(attribute_id)

            output_file.write(assignAttributes(product_type_id, attribute_id))

        output_file.close()

    checkProductTypeExists(product_type_ids)
    checkAttributeExists(attribute_ids)

    input_file.close()
